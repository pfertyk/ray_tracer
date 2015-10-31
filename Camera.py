import numpy
import math
from PIL import Image


class Camera:
    def __init__(self, eye = numpy.array([0.0, 0.0, 0.0]), center = numpy.array([0.0, 0.0, -1.0]), up = numpy.array([0.0, 1.0, 0.0]), fovy = 45.0, aspect = 1.0):
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
        xPos = -self.hw + (2 * self.hw) * (x + 0.5) / width
        yPos = -self.hh + (2 * self.hh) * (y + 0.5) / height
        
        pixelVector = (self.at * self.n) + (self.right * xPos) + (self.up * -yPos)
        
        return pixelVector
    
    def render_image(self, width, height, scene):
        
#         pixelVector = self.get_pixel_vector(120, 200, width, height)
#         color = scene.trace(self.eye, pixelVector, self.near, self.far)
        
        image = Image.new("RGB", (width, height))
        pix = image.load()
        
        for x in range(width):
            for y in range(height):
#                 pixelVector = self.get_pixel_vector(x, y, width, height)
#                 color = scene.trace(self.eye, pixelVector, self.near, self.far, self.eye)
#                 pix[x,y] = (color[0], color[1], color[2])
                #~ thread.start_new_thread(calc_pixel, (self, scene, x, y, width, height, pix))
                calc_pixel(self, scene, x, y, width, height, pix)
        image.save("image.png")
        

def calc_pixel(camera, scene, x, y, width, height, pix):
    pixelVector = camera.get_pixel_vector(x, y, width, height)
    color = scene.trace(camera.eye, pixelVector, camera.near, camera.far, camera.eye)
    pix[x,y] = (color[0], color[1], color[2])
