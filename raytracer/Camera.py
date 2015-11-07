from functools import partial
from multiprocessing.pool import Pool
import numpy as np
import math
from PIL import Image
from multiprocessing import Manager


class Camera:
    """
    Represents a camera.

    Camera can render a picture of a scene. One scene can be rendered using different cameras.
    That is why the camera is not one of normal scene objects. Instead, it is a separate object
    that can create an image of a scene, but is not rendered itself.
    """
    def __init__(self, position=(4, 4, 4), look_at=(0, 0, 0), up=(0, 1, 0), horizontal_angle=45):
        """
        :param position: position of the camera (eye)
        :param look_at: point that the camera is looking at
        :param up: vector representing the 'up' direction (might not be normalized)
        :param horizontal_angle: horizontal angle of view in degrees
        """
        self.position = np.array(position)
        self.up = np.array(up)

        front = look_at - self.position
        self.front = front / np.linalg.norm(front)
        right = np.cross(self.front, self.up)
        self.right = right / np.linalg.norm(right)
        up = np.cross(self.right, self.front)
        self.up = up / np.linalg.norm(up)
        self.image_plane_width = 2*(math.tan(math.radians(horizontal_angle/2)))

    def render_image(self, scene, image_size=(128, 72), file_name='image.png'):
        """
        Creates an image of a scene.

        Uses multiprocessing to improve performance. For big scenes or big images
        the computation time can be long. By default this method creates a png file
        with rendered image.
        :param scene: scene to render
        :param image_size: image size as a tuple (width, height)
        :param file_name: name of the output file (if None, no file will be generated)
        :return: generated image as PIL Image object
        """
        m = Manager()
        rendered_pixels = m.list(range(np.prod(image_size)))
        pool = Pool()
        pixel_color = partial(self.calculate_pixel_color, image_size=image_size, scene=scene, pixels=rendered_pixels)
        pool.map(pixel_color, ((x, y) for (x, y) in np.ndindex(image_size)))

        rendered_image = Image.new('RGB', image_size)
        rendered_image.putdata(rendered_pixels)
        if file_name:
            rendered_image.save(file_name)
        return rendered_image

    def calculate_pixel_color(self, pixel_coordinates, image_size, scene, pixels):
        """
        Calculates a color of one pixel on image plane and puts it in a pixel list.
        :param pixel_coordinates: pixel coordinates as a tuple (x, y)
        :param image_size: image size as a tuple (width, height)
        :param scene: scene to render
        :param pixels: a list of pixels, row by row, starting at top left corner, as tuples of 3 colors (R, G, B);
        """
        x, y = pixel_coordinates
        width, height = image_size
        pixel_vector = self.get_pixel_vector(x, y, width, height)
        color = scene.trace_ray(self.position, pixel_vector)
        pixels[y * width + x] = color

    def get_pixel_vector(self, x, y, width, height):
        """
        Creates a vector pointing from camera's position to a given pixel on image plane.

        The pixel with the coordinates (0, 0) is considered to be in a left top corner of the image.
        :param x: x index of a pixel (range 0 - width-1)
        :param y: y index of a pixel (range 0 - height-1)
        :param width: width of an image
        :param height: height of an image
        :return: a normalized vector representing a direction of light ray passing through given pixel
        """
        image_plane_height = height * self.image_plane_width / width
        pixel_pos_x = ((x + 0.5) / width) * self.image_plane_width - 0.5*self.image_plane_width
        pixel_pos_y = ((y + 0.5) / height) * image_plane_height - 0.5*image_plane_height
        pixel_vector = self.front + self.right*pixel_pos_x + self.up*-pixel_pos_y
        pixel_vector /= np.linalg.norm(pixel_vector)
        return pixel_vector
