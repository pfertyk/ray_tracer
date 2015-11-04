from collections import namedtuple
import numpy as np
import math
from raytracer.Materials import GRAY_MATTE

CollisionResult = namedtuple('CollisionResult', 'point normal material')


class Sphere:
    def __init__(self, pos=(0, 0, 0), radius=1, material=GRAY_MATTE):
        self.pos = pos
        self.radius = radius
        self.material = material

    def check_collision(self, eye, direction, near, far):
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

        if is_collision:
            collision_point = direction * collision_distance + eye
            normal = collision_point - self.pos
            normal /= np.linalg.norm(normal)
            return CollisionResult(collision_point, normal, self.material)
        else:
            return None


class Plane:
    def __init__(self, pos=(0, 0, 0), normal=(0, 1, 0), material=GRAY_MATTE):
        self.pos = pos
        normal /= np.linalg.norm(normal)
        self.normal = normal
        self.material = material

    def check_collision(self, eye, direction, near, far):
        det = np.dot(direction, self.normal)
        if det != 0:
            t = np.dot(self.normal, np.subtract(self.pos, eye)) / det
            if near <= t <= far:
                return CollisionResult(direction * t + eye, self.normal, self.material)
        return None


class Circle:
    def __init__(self, pos=(0, 0, 0), normal=(0, 1, 0), radius=1, front_material=GRAY_MATTE, back_material=None):
        if back_material is None:
            back_material = front_material
        self.front_plane = Plane(pos, normal, front_material)
        self.back_plane = Plane(pos, np.multiply(normal, -1), back_material)
        self.radius = radius

    def check_collision(self, eye, direction, near, far):
        if np.dot(direction, self.front_plane.normal) < 0:
            collision_result = self.front_plane.check_collision(eye, direction, near, far)
        else:
            collision_result = self.back_plane.check_collision(eye, direction, near, far)
        if collision_result:
            distance = np.linalg.norm(self.front_plane.pos - collision_result.point)
            if distance <= self.radius:
                return collision_result
        else:
            return None
