import time
import math
import numpy
from raytracer.Materials import ORANGE_GLOSSY, ORANGE_MATTE, BLUE_GLOSSY, MIRROR_GLOSSY, GRAY_GLOSSY, GRAY_MATTE, \
    BLUE_MATTE
from raytracer.Scene import Scene
from raytracer.Camera import Camera
from raytracer.Objects import Sphere, Plane, Circle
from raytracer.Lights import Lamp, Ambient, Sun

if __name__ == '__main__':
    light1 = Sun()
    light2 = Ambient()
    sphere1 = Sphere((0, 0, 0), 1, ORANGE_GLOSSY)
    plane1 = Plane(position=(0, -2, 0), material=BLUE_GLOSSY)

    scene = Scene()
    scene.objects.append(sphere1)
    scene.objects.append(plane1)
    scene.lights.append(light1)
    scene.lights.append(light2)

    camera = Camera((0, 3, 3), (0, 0, 0))
    t_start = time.time()
    print("Start")
    camera.render_image(scene, (1280, 720))
    print("Finished", time.time() - t_start)
