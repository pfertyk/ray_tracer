import numpy


class Light:
    def __init__(self, color = [255, 255, 255], pos = numpy.array([0.0, 0.0, 0.0]), attenuate = False, a = 1, b = 0, c = 0):
        self.color = color
        self.pos = pos
        self.attenuate = attenuate
        self.a = a
        self.b = b
        self.c = c
        
    def get_light_intensity(self, at):
            if self.attenuate:
                d = numpy.linalg.norm(self.pos - at)
                attFactor = self.a * d * d + self.b * d + self.c
                color =  numpy.array([self.color[0] / attFactor, self.color[1] / attFactor, self.color[2] / attFactor])
            else:
                color = self.color
            return color
        