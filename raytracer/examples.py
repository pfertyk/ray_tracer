import time

from raytracer.Materials import ORANGE_GLOSSY, BLUE_GLOSSY, GRAY_MATTE, MIRROR_GLOSSY, GREEN_GLOSSY, RED_GLOSSY, \
    GRAY_GLOSSY, PURPLE_GLOSSY, YELLOW_MATTE
from raytracer.Scene import Scene
from raytracer.Camera import Camera
from raytracer.Objects import Sphere, Plane, Circle
from raytracer.Lights import Ambient, Sun, Lamp


def render_water_molecule():
    scene = Scene()
    scene.objects.append(Sphere((0, 0, 0), 0.5, ORANGE_GLOSSY))
    scene.objects.append(Sphere((0.124, 0.484, 0), 0.3, BLUE_GLOSSY))
    scene.objects.append(Sphere((-0.5, 0, 0), 0.3, BLUE_GLOSSY))
    scene.objects.append(Plane(position=(0, -0.7, 0), material=GRAY_MATTE))
    scene.lights.append(Sun())
    scene.lights.append(Ambient())

    camera = Camera((0, 0.4, 4), (0, 0, 0))
    t_start = time.time()
    print("Start")
    camera.render_image(scene)
    print("Finished", time.time() - t_start)


def render_reflecting_sphere():
    scene = Scene()
    scene.objects.append(Sphere((0, 0, 0), 0.5, MIRROR_GLOSSY))
    scene.objects.append(Sphere((1, 0, 0), 0.3, GREEN_GLOSSY))
    scene.objects.append(Sphere((-1, 0, -0), 0.3, RED_GLOSSY))
    scene.objects.append(Plane(position=(0, -0.7, 0), material=GRAY_GLOSSY))
    scene.lights.append(Lamp(position=(2, 5, 2), max_lighting_distance=128))
    scene.lights.append(Ambient())

    camera = Camera((0, 0.6, 4), (0, 0, 0))
    t_start = time.time()
    print("Start")
    camera.render_image(scene)
    print("Finished", time.time() - t_start)


def render_infinity_mirror():
    scene = Scene()
    scene.max_recursion_level = 7
    scene.objects.append(Sphere((0, 0, 0), 0.25, PURPLE_GLOSSY))
    scene.objects.append(Circle((4, 0, 0), (-1, 0, 0), 2, MIRROR_GLOSSY))
    scene.objects.append(Circle((4.001, 0, 0), (-1, 0, 0), 2.1, GRAY_MATTE))
    scene.objects.append(Circle((-4, 0, 0), (1, -0.05, 0.1), 2, MIRROR_GLOSSY))
    scene.objects.append(Circle((-4.001, 0, 0), (1, -0.05, 0.1), 2.1, GRAY_MATTE))
    scene.objects.append(Plane(position=(0, -1, 0), material=YELLOW_MATTE))
    scene.lights.append(Lamp(position=(1, 5, 2), max_lighting_distance=128))
    scene.lights.append(Ambient())

    camera = Camera((3, 0.4, 0), (0, 0, 0))
    t_start = time.time()
    print("Start")
    camera.render_image(scene, (1280, 720))
    print("Finished", time.time() - t_start)
