import numpy as np
import math


white_material = {
    'ambient_color': (255, 255, 255),
    'diffuse_color': (255, 255, 255),
    'specular_color': (255, 255, 255),
    'ambient_coeff': 1,
    'diffuse_coeff': 1,
    'specular_coeff': 1,
    'exponent': 60
}


orange_material = dict(white_material)
orange_material['ambient_color'] = orange_material['diffuse_color'] = (255, 165, 0)

blue_material = dict(white_material)
blue_material['ambient_color'] = blue_material['diffuse_color'] = (30, 144, 255)

gray_material = dict(white_material)
gray_material['ambient_color'] = gray_material['diffuse_color'] = (127, 127, 127)
gray_material['specular_color'] = (0, 0, 0)


class CollisionResult:
    def __init__(self):
        self.collisionDistance = 0.0
        self.material = gray_material
        self.isCollision = False


class Sphere:
    def __init__(self, pos=(0, 0, 0), radius=1, material=gray_material):
        self.pos = pos
        self.radius = radius
        self.material = material

    def collision(self, e, d, near, far):
        result = CollisionResult()
        result.isCollision = False

        temp = np.subtract(e, self.pos)
        a = np.dot(d, d)
        b = 2 * (np.dot(temp, d))
        c = np.dot(temp, temp) - (self.radius * self.radius)
        delta = b*b - 4*a*c

        if delta > 0:
            t1 = (-b - math.sqrt(delta)) / (2*a)
            t2 = (-b + math.sqrt(delta)) / (2*a)
            if (near <= t1 <= far) and (near <= t2 <= far):
                result.isCollision = True
                result.collisionDistance = min(t1, t2)
            elif near <= t1 <= far:
                result.isCollision = True
                result.collisionDistance = t1
            elif near <= t2 <= far:
                result.isCollision = True
                result.collisionDistance = t2
        elif delta == 0:
            t = -b / (2 * a)
            if near <= t <= far:
                result.isCollision = True
                result.collisionDistance = t

        if result.isCollision:
            result.collisionPoint = d * result.collisionDistance + e
            normal = result.collisionPoint - self.pos
            normal = normal / np.linalg.norm(normal)
            result.normal = normal
            result.material = self.material

        return result


class Plane:
    def __init__(self, pos=(0, 0, 0), normal=(0, 1, 0),  material=gray_material):
        self.pos = pos
        normal = normal / np.linalg.norm(normal)
        self.normal = normal
        self.material = material

    def collision(self, e, d, near, far):
        result = CollisionResult()
        result.isCollision = False
        det = np.dot(d, self.normal)
        if det != 0:
            t = np.dot(self.normal, np.subtract(self.pos, e)) / det
            if near <= t <= far:
                result.isCollision = True
                result.collisionDistance = t
                result.material = self.material
                result.normal = self.normal
                result.collisionPoint = d * t + e
        return result


class Light:
    def __init__(self, pos=(0, 0, 0), color=(255, 255, 255), attenuate=False, a=1, b=0, c=0):
        self.color = color
        self.pos = pos
        self.attenuate = attenuate
        self.a = a
        self.b = b
        self.c = c

    def get_light_intensity_at(self, point):
            if self.attenuate:
                d = np.linalg.norm(self.pos - point)
                att_factor = self.a * d * d + self.b * d + self.c
                color = (self.color[0] / att_factor, self.color[1] / att_factor, self.color[2] / att_factor)
            else:
                color = self.color
            return color