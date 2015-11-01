import os
import numpy
import math
from PIL import Image
from multiprocessing import Process, Queue, JoinableQueue


class Camera:
    def __init__(self, eye=numpy.array([0.0, 0.0, 0.0]), center=numpy.array([0.0, 0.0, -1.0]),
                 up=numpy.array([0.0, 1.0, 0.0]), fovy=45.0, aspect=1.0):
        self.eye = eye
        self.at = center - eye
        self.up = up
        
        self.fovy = fovy
        self.aspect = aspect
        
        self.n = 0
        self.hh = 0
        self.hw = 0

        self.near = 0.001
        self.far = 1000.0
        
        self.right = numpy.cross(self.at, up)
        self.up = numpy.cross(self.right, self.at)
        
        radians = math.pi * (fovy * 0.5) / 180.0
        
        self.n = math.cos(radians)
        self.hh = math.sin(radians)
        self.hw = self.aspect * self.hh

        self.at = self.at / numpy.linalg.norm(self.at)
        self.up = self.up / numpy.linalg.norm(self.up)
        self.right = self.right / numpy.linalg.norm(self.right)

    def get_pixel_vector(self, x, y, width, height):
        x_pos = -self.hw + (2 * self.hw) * (x + 0.5) / width
        y_pos = -self.hh + (2 * self.hh) * (y + 0.5) / height
        pixel_vector = (self.at * self.n) + (self.right * x_pos) + (self.up * -y_pos)
        return pixel_vector

    def render_image(self, size, scene):
        width, height = size
        image = Image.new('RGB', size)
        pix = image.load()
        pixel_coordinates = JoinableQueue()
        rendered_pixels = Queue()
        for x in range(width):
            for y in range(height):
                pixel_coordinates.put((x, y))
        ps = []
        for i in range(4):
            p = Process(target=calc_pixel, name='t%d' % i, args=(pixel_coordinates, self, scene, width, height, rendered_pixels))
            p.daemon = True
            ps.append(p)

        for p in ps:
            p.start()

        pixel_coordinates.join()
        print('all pixels processed')
        while not rendered_pixels.empty():
            (x, y), color = rendered_pixels.get()
            pix[x, y] = color
        print('image rendered')
        image.save('image.png')


def calc_pixel(pixel_coordinates, camera, scene, width, height, rendered_pixels):
    try:
        while True:
            print(os.getpid())
            x, y = pixel_coordinates.get(timeout=1)
            pixel_vector = camera.get_pixel_vector(x, y, width, height)
            color = scene.trace(camera.eye, pixel_vector, camera.near, camera.far, camera.eye)
            rendered_pixels.put(((x, y), (color[0], color[1], color[2])))
            pixel_coordinates.task_done()
    except:
        print('error')
    print('end', os.getpid())
