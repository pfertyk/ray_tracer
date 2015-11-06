import numpy as np
from raytracer.LightingModels import whitted_lighting_model


class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []
        self.background_color = (64, 64, 64)
        self.lighting_model = whitted_lighting_model
        self.max_recursion_level = 4
        self.near = 1e-10
        self.far = 10000
    
    def check_collision(self, eye, direction, near=None, far=None):
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
        if recursion_level is None:
            recursion_level = self.max_recursion_level
        if recursion_level == 0:
            return self.background_color
        collision_result = self.check_collision(eye, direction, self.near, self.far)
        if collision_result:
            return self.lighting_model(self, direction, collision_result, recursion_level)
        else:
            return self.background_color
