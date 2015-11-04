import time
from raytracer.Materials import ORANGE_GLOSSY, ORANGE_MATTE, BLUE_GLOSSY
from raytracer.Scene import Scene
from raytracer.Camera import Camera
from raytracer.Objects import Sphere, Plane, Circle
from raytracer.Lights import Lamp, Ambient, Sun

if __name__ == '__main__':
    light1 = Lamp(position=(-10, 10, -10))
    light1 = Sun(direction=(0, -2, 0))
    light2 = Ambient()

    sphere1 = Sphere((1.5, 2.2, -4.0), 0.4, ORANGE_GLOSSY)
    sphere2 = Sphere((-0.5, 2, -5.0), 1.2, ORANGE_GLOSSY)
    plane1 = Plane(material=BLUE_GLOSSY)
    circle1 = Circle(pos=(0, 0.1, -5.5), normal=(0, -1, 0), radius=2, front_material=ORANGE_MATTE)

    scene = Scene()

    # scene.objects.append(sphere1)
    # scene.objects.append(sphere2)
    scene.objects.append(plane1)
    scene.objects.append(circle1)

    scene.lights.append(light1)
    scene.lights.append(light2)

    camera = Camera(eye=(0, 4, 0), center=(0, 2, -5))

    t_start = time.time()
    print("Start")
    camera.render_image(scene, (200, 200))
    print("Finished", time.time() - t_start)
