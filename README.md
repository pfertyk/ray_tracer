# Ray Tracer

A simple program for generating 3D graphics using the [ray tracing algorithm](https://en.wikipedia.org/wiki/Ray_tracing_%28graphics%29). Rendered images can be saved as PNG files. The program's implementation is based mostly on [this publication](http://www.cs.utah.edu/~shirley/books/fcg2/rt.pdf).

## Requirements

This program requires Python 3.x and PIL library.

## Quick start

The easiest way to render a picture is to use ```Examples``` module:
```python
from raytracer.Examples import render_water_molecule

render_water_molecule()
```
This script generates an image (128x72 pixels) of a simplified water molecule and saves it as 'image.png'. To change the size of the image or the name of the file, the code can be modified as follows:

```python
from raytracer.Examples import render_water_molecule

render_water_molecule(image_size=(1280, 720), file_name='water_molecule.png')
```

Please note that generating an image of this size might take few minutes.

The ```Examples``` module offers 2 other methods: ```render_reflecting_sphere``` and ```render_infinity_mirror```. Custom scenes can also be created:

```python
from raytracer.Camera import Camera
from raytracer.Lights import Sun, Ambient
from raytracer.Materials import ORANGE_GLOSSY
from raytracer.Objects import Sphere
from raytracer.Scene import Scene

scene = Scene()
scene.objects.append(Sphere((0, 0, 0), 1, ORANGE_GLOSSY))
scene.lights.append(Sun())
scene.lights.append(Ambient())

camera = Camera()
camera.render_image(scene)
```

This ray tracer can render spheres, planes and circles. It uses 3 different light sources: ambient, sun and point. The lighting model includes specular reflections, as well as reflected light rays (for creating mirror surfaces).

## Samples

Images below have been generated using the functions from the ```Examples``` module mentioned earlier (image size set to 1280x720).

![image1](samples/water_molecule.png)
![image2](samples/reflecting_sphere.png)
![image2](samples/infinity_mirror.png)

## Tests

Several tests are provided for this program. Each test generates an image of a scene and compares it with an original image (stored in the tests directory). If any differences are detected, the generated image is saved to allow comparing it with the original.

Please keep in mind that these tests run much longer than standard unit tests.
