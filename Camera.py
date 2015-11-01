from functools import partial
from multiprocessing.pool import Pool
import numpy
import math
from PIL import Image
from multiprocessing import Manager


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
        m = Manager()
        width, height = size
        rendered_pixels = m.list(range(width * height))
        pool = Pool()
        calc_pix = partial(self.calc_pixel, scene=scene, width=width, height=height, pix=rendered_pixels)
        pool.map(calc_pix, ((x, y) for x in range(width) for y in range(height)))

        image = Image.new('RGB', size)
        image.putdata(rendered_pixels)
        image.save('image.png')

    def calc_pixel(self, pixel_coordinates, scene, width, height, pix):
        x, y = pixel_coordinates
        pixel_vector = self.get_pixel_vector(x, y, width, height)
        color = scene.trace(self.eye, pixel_vector, self.near, self.far, self.eye)
        pix[y * height + x] = (color[0], color[1], color[2])
