import os
from unittest.case import TestCase

from PIL import Image

from raytracer.Camera import Camera
from raytracer.Lights import Sun, Ambient, Lamp
from raytracer.Materials import BLUE_GLOSSY, ORANGE_GLOSSY, GRAY_MATTE
from raytracer.Objects import Sphere, Plane
from raytracer.Scene import Scene


class RayTracingTests(TestCase):
    def compare_images(self, rendered_image, original_file_path):
        file_name, file_extension = os.path.splitext(original_file_path)
        incorrect_file_path = '{}_incorrect{}'.format(file_name, file_extension)
        if os.path.exists(incorrect_file_path):
            os.remove(incorrect_file_path)
        original_image = Image.open(original_file_path)
        images_are_equal = list(original_image.getdata()) == list(rendered_image.getdata())
        if not images_are_equal:
            rendered_image.save(incorrect_file_path)
            self.fail('Image {} not generated correctly'.format(original_file_path))

    def test_sun_specular(self):
        light1 = Sun(direction=(0, -2, 0))
        light2 = Ambient()
        sphere1 = Sphere((0, 0, 0), 1, ORANGE_GLOSSY)
        plane1 = Plane(position=(0, -2, 0), material=BLUE_GLOSSY)

        scene = Scene()
        scene.objects.append(sphere1)
        scene.objects.append(plane1)
        scene.lights.append(light1)
        scene.lights.append(light2)

        camera = Camera((0, 3, 3), (0, 0, 0))
        rendered_image = camera.render_image(scene, (100, 100), file_name=None)
        self.compare_images(rendered_image, 'sun_specular.png')

    def test_lamp_specular(self):
        light1 = Lamp(position=(5, 5, 5))
        light2 = Ambient()
        sphere1 = Sphere((0, 0, 0), 1, BLUE_GLOSSY)
        plane1 = Plane(position=(0, -2, 0), material=GRAY_MATTE)

        scene = Scene()
        scene.objects.append(sphere1)
        scene.objects.append(plane1)
        scene.lights.append(light1)
        scene.lights.append(light2)

        camera = Camera((0, 3, 3), (0, 0, 0))
        rendered_image = camera.render_image(scene, (100, 100), file_name=None)
        self.compare_images(rendered_image, 'lamp_specular.png')
