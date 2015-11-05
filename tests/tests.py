import os
from unittest.case import TestCase

from PIL import Image

from raytracer.Camera import Camera
from raytracer.Lights import Sun, Ambient, Lamp
from raytracer.Materials import BLUE_GLOSSY, ORANGE_GLOSSY, GRAY_MATTE, GRAY_GLOSSY, ORANGE_MATTE, MIRROR_GLOSSY, \
    BLUE_MATTE
from raytracer.Objects import Sphere, Plane, Circle
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

    def test_circle_front_back(self):
        light1 = Lamp(position=(5, 5, 5))
        light2 = Ambient()
        circle1 = Circle(center=(0, 0, 0.5), front_material=GRAY_GLOSSY, back_material=BLUE_GLOSSY)
        circle2 = Circle(center=(0, 1, -0.5), normal=(0, -1, 0), front_material=GRAY_GLOSSY, back_material=BLUE_GLOSSY)
        plane1 = Plane(position=(0, -0.2, 0), material=ORANGE_MATTE)

        scene = Scene()
        scene.objects.append(circle1)
        scene.objects.append(circle2)
        scene.objects.append(plane1)
        scene.lights.append(light1)
        scene.lights.append(light2)

        camera = Camera((0, 3, 3), (0, 0, 0))
        rendered_image = camera.render_image(scene, (100, 100), file_name=None)
        self.compare_images(rendered_image, 'circle_front_back.png')

    def test_multiple_reflections(self):
        light1 = Lamp(position=(-5, 5, 5))
        light2 = Ambient()
        sphere1 = Sphere((-0.7, 0, 0.2), 1, MIRROR_GLOSSY)
        plane1 = Plane(position=(0, -2, 0), material=BLUE_GLOSSY)
        circle1 = Circle(center=(0.8, 0, -0.5), normal=(-1, 0, 1), radius=1.5, front_material=MIRROR_GLOSSY)

        scene = Scene()
        scene.objects.append(circle1)
        scene.objects.append(sphere1)
        scene.objects.append(plane1)
        scene.lights.append(light1)
        scene.lights.append(light2)

        camera = Camera((0, 3, 3), (0, 0, 0))
        rendered_image = camera.render_image(scene, (100, 100), file_name=None)
        self.compare_images(rendered_image, 'multiple_reflections.png')

    def test_matte_no_ambient(self):
        light1 = Lamp(position=(-5, 5, 5))
        sphere1 = Sphere((0, 0, 0), 1, BLUE_MATTE)
        plane1 = Plane(position=(0, -2, 0), material=GRAY_MATTE)

        scene = Scene()
        scene.objects.append(sphere1)
        scene.objects.append(plane1)
        scene.lights.append(light1)

        camera = Camera((0, 3, 3), (0, 0, 0))
        rendered_image = camera.render_image(scene, (100, 100), file_name=None)
        self.compare_images(rendered_image, 'matte_no_ambient.png')