from collections import namedtuple

Material = namedtuple('Material', 'color specular_color exponent reflection')
Material.__new__.__defaults__ = ((127, 127, 127), (255, 255, 255), 60, 0)

orange = Material(color=(255, 165, 0))
blue = Material(color=(30, 144, 255))
gray_matte = Material(specular_color=(0, 0, 0))
mirror = Material(color=(0, 0, 0), reflection=1)
