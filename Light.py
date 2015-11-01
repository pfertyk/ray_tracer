import numpy


class Light:
    def __init__(self, color=(255, 255, 255), pos=(0, 0, 0), attenuate=False, a=1, b=0, c=0):
        self.color = color
        self.pos = pos
        self.attenuate = attenuate
        self.a = a
        self.b = b
        self.c = c
        
    def get_light_intensity_at(self, point):
            if self.attenuate:
                d = numpy.linalg.norm(self.pos - point)
                att_factor = self.a * d * d + self.b * d + self.c
                color = (self.color[0] / att_factor, self.color[1] / att_factor, self.color[2] / att_factor)
            else:
                color = self.color
            return color
