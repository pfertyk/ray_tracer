from collections import namedtuple

Material = namedtuple('Material', 'color specular_color phong_exponent reflection_factor')
Material.__new__.__defaults__ = ((127, 127, 127), (255, 255, 255), 60, 0)

ORANGE_GLOSSY = Material(color=(255, 165, 0))
ORANGE_MATTE = Material(color=(255, 165, 0), specular_color=(0, 0, 0))
BLUE_GLOSSY = Material(color=(30, 144, 255))
BLUE_MATTE = Material(color=(30, 144, 255), specular_color=(0, 0, 0))
GRAY_GLOSSY = Material()
GRAY_MATTE = Material(specular_color=(0, 0, 0))
MIRROR_GLOSSY = Material(color=(0, 0, 0), reflection_factor=1)
