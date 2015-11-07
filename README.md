# Ray Tracer
A simple program for generating 3D graphics using the [ray tracing algorithm](https://en.wikipedia.org/wiki/Ray_tracing_%28graphics%29). Rendered images can be saved as PNG files. The program's implementation is based mostly on [this publication](http://www.cs.utah.edu/~shirley/books/fcg2/rt.pdf).

## Requirements
This program requires Python 3.x and PIL library.

## Quick start

```
from raytracer.Examples import render_water_molecule

render_water_molecule()
```

```
from raytracer.Examples import render_water_molecule

render_water_molecule(image_size=(1280, 720), file_name='water_molecule.png')
```

Please note that generating an image of this size might take few minutes.

```
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


## Samples

Sample images below have been generated using 3 scenes from the Examples module.

![image1](samples/water_molecule.png)

![image2](samples/reflecting_sphere.png)

![image2](samples/infinity_mirror.png)

## Tests
Several tests are provided for this program. Each test generates an image of a scene and compares it with an original image (stored in tests directory). If any differences are detected, the generated image is saved to allow comparing it with original.

Please keep in mind that these tests run much longer than standard unit tests.
