import numpy as np
from raytracer.LightingModels import whitted_lighting_model


class Scene:
    """
    Represents a scene.

    Scene contains all visible objects and all light sources.
    It also contains lighting model that represents laws of
    physics (it is responsible for proper color calculation).
    """
    def __init__(self):
        self.objects = []
        self.lights = []
        self.background_color = (64, 64, 64)
        self.lighting_model = whitted_lighting_model
        self.max_recursion_level = 4
        self.near = 1e-10
        self.far = 10000
    
    def check_collision(self, eye, direction, near=None, far=None):
        """
        Checks if a ray collides with any object on the scene.
        :param eye: beginning of a traced ray
        :param direction: direction of a traced ray (must be normalized)
        :param near: minimal distance of detecting collisions
        :param far: maximal distance of detecting collisions
        :return: a tuple of (collision point, normal, material) or None, if there is no collision
        """
        if near is None:
            near = self.near
        if far is None:
            far = self.far
        collision_result = None
        min_collision_distance = far
        for obj in self.objects:
            result = obj.check_collision(eye, direction, near, min_collision_distance)
            if result:
                distance = np.linalg.norm(np.subtract(eye, result.point))
                if distance < min_collision_distance:
                    collision_result = result
                    min_collision_distance = distance
        return collision_result
    
    def trace_ray(self, eye, direction, recursion_level=None):
        """
        Traces a ray of light through a scene and returns its color.

        Detects first object that a ray collides with and calculates its color at given point.
        If there is no collision (or recursion level reached 0), returns background color of the scene.
        :param eye: beginning point of a traced ray
        :param direction: direction of a traced ray (must be normalized)
        :param recursion_level: number of times the ray can reflect from any surface to create mirror reflection
        (if None, the scene's max_recursion_level will be used)
        :return: color of given ray of light, as a tuple (R, G, B) (values range from 0 to 255)
        """
        if recursion_level is None:
            recursion_level = self.max_recursion_level
        if recursion_level == 0:
            return self.background_color
        collision_result = self.check_collision(eye, direction, self.near, self.far)
        if collision_result:
            return self.lighting_model(self, direction, collision_result, recursion_level)
        else:
            return self.background_color
