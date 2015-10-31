import numpy
import Scene
import Camera
import Sphere
import Material
import Light
import Plane
import time


light = Light.Light(pos = numpy.array([10, 10, 10]))

material1 = Material.Material([255, 165, 0], [255, 165, 0], [255, 255, 255], 1, 1, 1, 60)
material2 = Material.Material([30, 144, 255], [30, 144, 255], [255, 255, 255], 1, 1, 1, 60)
material3 = Material.Material([127, 127, 127], [127, 127, 127], [0, 0, 0], 1, 1, 0, 60)


sphere1 = Sphere.Sphere(numpy.array([0.5, 2.2, -5.0]), 1.0, material1)
sphere2 = Sphere.Sphere(numpy.array([-0.5, 2.0, -5.0]), 1.2, material2)

plane1 = Plane.Plane(material = material3)

scene = Scene.Scene()

scene.objects.append(sphere1)
scene.objects.append(sphere2)
scene.objects.append(plane1)
scene.lights.append(light)
    
camera = Camera.Camera(eye = numpy.array([0, 4, 0]), center = numpy.array([0, 2, -5]))

t_start = time.time()
print("Start")

camera.render_image(400, 400, scene)

print("Finished", time.time() - t_start)

