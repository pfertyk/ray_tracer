"""
Contains miscellaneous light sources.

Each light source must implement 3 methods:
- illuminates(point, scene): returns True if the light reaches given point on scene, False otherwise
- get_light_intensity_at(point): returns color of the light at given point ((0, 0, 0) represents no illumination)
- get_light_vector_at(point): returns vector representing the direction of light ray at given point (might be None, has\
 to be normalized)

Values returned by get_light_intensity_at and get_light_vector_at must be numpy arrays with 3 values (range 0 - 255).
"""
import numpy as np


class Point:
    """
    Represents a point light source.

    Light rays from this light source spread in all directions from light position (360 degree angle). Light intensity \
    fades with distance (inverse square falloff). Points located further than max_light_distance will not be \
    illuminated (light color at those points will be (0, 0, 0)). It can be used to represent lamps.
    :param color: represents light color (as a tuple of 3 values, range 0 - 255)
    :param position: represents light source position
    :param max_lighting_distance: distance of effective illumination from this light source
    """
    def __init__(self, color=(255, 255, 255), position=(0, 0, 0), max_lighting_distance=30):
        self.color = np.array(color)
        self.position = np.array(position)
        self.max_lighting_distance = max_lighting_distance

    def illuminates(self, point, scene):
        light_vector = self.position - point
        light_vector_len = np.linalg.norm(light_vector)
        return not scene.check_collision(point, light_vector / light_vector_len, far=light_vector_len)

    def get_light_intensity_at(self, point):
        distance = np.linalg.norm(point - self.position)
        if distance > self.max_lighting_distance:
            return np.array((0, 0, 0))
        else:
            factor = ((self.max_lighting_distance - distance) / self.max_lighting_distance)**2
            return self.color * factor

    def get_light_vector_at(self, point):
        light_vector = point - self.position
        light_vector /= np.linalg.norm(light_vector)
        return light_vector


class Ambient:
    """
    Represents ambient (scattered) light.

    This light does not have a source, therefore light vector will always be None. The light reaches every point on \
    scene and never fades (light intensity is constant). This light can be used to brighten the scene.
    :param color: represents light color (as a tuple of 3 values, range 0 - 255)
    """
    def __init__(self, color=(127, 127, 127)):
        self.color = np.array(color)

    def illuminates(self, point, scene):
        return True

    def get_light_intensity_at(self, point):
        return self.color

    def get_light_vector_at(self, point):
        return None


class Sun:
    """
    Represents a powerful light with infinitely distant source.

    All light rays for this light source are parallel (there is no center point). Light intensity never fades, but \
    obstacles can stop light rays. This light source can be used to easily illuminate the whole scene, while still \
    producing specular reflections.
    :param color: represents light color (as a tuple of 3 values, range 0 - 255)
    :param direction: light ray direction
    """
    def __init__(self, color=(127, 127, 127), direction=(0, -1, 0)):
        self.direction = direction / np.linalg.norm(direction)
        self.color = np.array(color)

    def illuminates(self, point, scene):
        return not scene.check_collision(point, -self.direction)

    def get_light_intensity_at(self, point):
        return self.color

    def get_light_vector_at(self, point):
        return self.direction
