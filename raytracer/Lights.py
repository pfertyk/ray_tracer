import numpy as np


class Light:
    def __init__(self, pos=(0, 0, 0), color=(255, 255, 255), attenuate=False, a=1, b=0, c=0):
        self.color = color
        self.pos = pos
        self.attenuate = attenuate
        self.a = a
        self.b = b
        self.c = c

    def illuminates(self, point, scene):
        light_vector = np.subtract(self.pos, point)
        light_vector_len = np.linalg.norm(light_vector)
        return not scene.collision(point, light_vector / light_vector_len, 0.00001, light_vector_len)

    def get_light_intensity_at(self, point):
            if self.attenuate:
                distance = np.linalg.norm(self.pos - point)
                att_factor = self.a * distance * distance + self.b * distance + self.c
                color = (self.color[0] / att_factor, self.color[1] / att_factor, self.color[2] / att_factor)
            else:
                color = self.color
            return color

    def get_light_vector_at(self, point):
        light_vector = np.subtract(point, self.pos)
        light_vector /= np.linalg.norm(light_vector)
        return light_vector
