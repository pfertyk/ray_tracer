import numpy as np
from raytracer import ShadingModel


class Scene:
    def __init__(self, background_color=(0, 0, 0)):
        self.objects = []
        self.lights = []
        self.background_color = background_color
        self.shadingModel = ShadingModel.PhongShadingModel()
        self.ambientColor = (127, 127, 127)
        self.max_level = 4
    
    def collision(self, eye, direction, near, far):
        collision_result = None
        distance = far
        for obj in self.objects:
            temp_result = obj.collision(eye, direction, near, distance)
            if temp_result:
                temp_distance = np.linalg.norm(np.subtract(eye, temp_result.point))
                if temp_distance < distance:
                    collision_result = temp_result
                    distance = temp_distance
        return collision_result
    
    def trace_ray(self, eye, direction, near, far, level=None):
        if level is None:
            level = self.max_level
        if level == 0:
            return self.background_color
        collision_result = self.collision(eye, direction, near, far)
        if collision_result:
            return self.shadingModel.calculate_color(self, eye, collision_result, level)
        else:
            return self.background_color
