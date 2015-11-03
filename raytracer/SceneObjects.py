from collections import namedtuple
import numpy as np
import math


white_material = {
    'ambient_color': (255, 255, 255),
    'diffuse_color': (255, 255, 255),
    'specular_color': (255, 255, 255),
    'ambient_coeff': 1,
    'diffuse_coeff': 1,
    'specular_coeff': 1,
    'exponent': 60,
    'reflection': 0
}


orange_material = dict(white_material)
orange_material['ambient_color'] = orange_material['diffuse_color'] = (255, 165, 0)

blue_material = dict(white_material)
blue_material['ambient_color'] = blue_material['diffuse_color'] = (30, 144, 255)

gray_material = dict(white_material)
gray_material['ambient_color'] = gray_material['diffuse_color'] = (127, 127, 127)
gray_material['specular_color'] = (0, 0, 0)

reflective_material = dict(white_material)
reflective_material['reflection'] = 1
reflective_material['ambient_coeff'] = reflective_material['diffuse_coeff'] = 0


CollisionResult = namedtuple('CollisionResult', 'point normal material')


class Sphere:
    def __init__(self, pos=(0, 0, 0), radius=1, material=gray_material):
        self.pos = pos
        self.radius = radius
        self.material = material

    def collision(self, eye, direction, near, far):
        is_collision = False

        temp = np.subtract(eye, self.pos)
        a = np.dot(direction, direction)
        b = 2 * (np.dot(temp, direction))
        c = np.dot(temp, temp) - (self.radius * self.radius)
        delta = b*b - 4*a*c

        if delta > 0:
            t1 = (-b - math.sqrt(delta)) / (2*a)
            t2 = (-b + math.sqrt(delta)) / (2*a)
            if (near <= t1 <= far) and (near <= t2 <= far):
                is_collision = True
                collision_distance = min(t1, t2)
            elif near <= t1 <= far:
                is_collision = True
                collision_distance = t1
            elif near <= t2 <= far:
                is_collision = True
                collision_distance = t2
        elif delta == 0:
            t = -b / (2 * a)
            if near <= t <= far:
                is_collision = True
                collision_distance = t

        collision_result = None
        if is_collision:
            collision_point = direction * collision_distance + eye
            normal = collision_point - self.pos
            normal = normal / np.linalg.norm(normal)
            collision_result = CollisionResult(collision_point, normal, self.material)
        return collision_result


class Plane:
    def __init__(self, pos=(0, 0, 0), normal=(0, 1, 0),  material=gray_material):
        self.pos = pos
        normal = normal / np.linalg.norm(normal)
        self.normal = normal
        self.material = material

    def collision(self, eye, direction, near, far):
        collision_result = None
        det = np.dot(direction, self.normal)
        if det != 0:
            t = np.dot(self.normal, np.subtract(self.pos, eye)) / det
            if near <= t <= far:
                collision_result = CollisionResult(direction * t + eye, self.normal, self.material)
        return collision_result
