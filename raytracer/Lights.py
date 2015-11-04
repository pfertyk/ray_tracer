import numpy as np


class Lamp:
    def __init__(self, color=(127, 127, 127), position=(0, 0, 0), max_lighting_distance=30):
        self.color = color
        self.position = position
        self.max_lighting_distance = max_lighting_distance

    def illuminates(self, point, scene):
        light_vector = np.subtract(self.position, point)
        light_vector_len = np.linalg.norm(light_vector)
        return not scene.check_collision(point, light_vector / light_vector_len, far=light_vector_len)

    def get_light_intensity_at(self, point):
        distance = np.linalg.norm(np.subtract(point, self.position))
        if distance > self.max_lighting_distance:
            return 0, 0, 0
        else:
            factor = ((self.max_lighting_distance - distance) / self.max_lighting_distance)**2
            return np.multiply(self.color, factor)

    def get_light_vector_at(self, point):
        light_vector = np.subtract(point, self.position)
        light_vector /= np.linalg.norm(light_vector)
        return light_vector


class Ambient:
    def __init__(self, color=(127, 127, 127)):
        self.color = color

    def illuminates(self, point, scene):
        return True

    def get_light_intensity_at(self, point):
        return self.color

    def get_light_vector_at(self, point):
        return None


class Sun:
    def __init__(self, color=(127, 127, 127), direction=(0, -1, 0)):
        self.direction = direction / np.linalg.norm(direction)
        self.color = color

    def illuminates(self, point, scene):
        return not scene.check_collision(point, -self.direction)

    def get_light_intensity_at(self, point):
        return self.color

    def get_light_vector_at(self, point):
        return self.direction
