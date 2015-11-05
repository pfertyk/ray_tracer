from functools import partial
from multiprocessing.pool import Pool
import numpy as np
import math
from PIL import Image
from multiprocessing import Manager


class Camera:
    def __init__(self, position=(0, 0, 0), look_at=(0, 0, -1), up=(0, 1, 0), horizontal_angle=45):
        self.position = np.array(position)
        self.up = np.array(up)

        front = np.array(look_at) - self.position
        self.front = front / np.linalg.norm(front)
        right = np.cross(self.front, self.up)
        self.right = right / np.linalg.norm(right)
        up = np.cross(self.right, self.front)
        self.up = up / np.linalg.norm(up)
        self.image_plane_width = 2*(math.tan(math.radians(horizontal_angle/2)))

    def render_image(self, scene, size=(100, 100), file_name='image.png'):
        m = Manager()
        width, height = size
        rendered_pixels = m.list(range(width * height))
        pool = Pool()
        calc_pix = partial(self.calculate_pixel, scene=scene, width=width, height=height, pix=rendered_pixels)
        pool.map(calc_pix, ((x, y) for (x, y) in np.ndindex(size)))

        image = Image.new('RGB', size)
        image.putdata(rendered_pixels)
        if file_name:
            image.save(file_name)
        return image

    def calculate_pixel(self, pixel_coordinates, scene, width, height, pix):
        x, y = pixel_coordinates
        pixel_vector = self.get_pixel_vector(x, y, width, height)
        pixel_vector /= np.linalg.norm(pixel_vector)
        color = scene.trace_ray(self.position, pixel_vector)
        pix[y * height + x] = color

    def get_pixel_vector(self, x, y, width, height):
        image_plane_height = height * self.image_plane_width / width
        x_pos = ((x + 0.5) / width) * self.image_plane_width - 0.5*self.image_plane_width
        y_pos = ((y + 0.5) / height) * image_plane_height - 0.5*image_plane_height
        pixel_vector = self.front + self.right*x_pos + self.up*-y_pos
        pixel_vector /= np.linalg.norm(pixel_vector)
        return pixel_vector
