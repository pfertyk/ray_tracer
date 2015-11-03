import time

from raytracer.Scene import Scene
from raytracer.Camera import Camera
from raytracer.SceneObjects import Sphere, Plane, orange_material, reflective_material
from raytracer.Lights import Light

if __name__ == '__main__':
    light = Light((-10, 10, 10))

    sphere1 = Sphere((1.5, 2.2, -4.0), 0.4, orange_material)
    sphere2 = Sphere((-0.5, 2, -5.0), 1.2, reflective_material)
    plane1 = Plane()

    scene = Scene()

    scene.objects.append(sphere1)
    scene.objects.append(sphere2)
    scene.objects.append(plane1)

    scene.lights.append(light)

    camera = Camera(eye=(0, 4, 0), center=(0, 2, -5))

    t_start = time.time()
    print("Start")
    camera.render_image(scene, (200, 200))
    print("Finished", time.time() - t_start)
