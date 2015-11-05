from collections import namedtuple
import numpy as np
import math
from raytracer.Materials import GRAY_GLOSSY

CollisionResult = namedtuple('CollisionResult', 'point normal material')


class Sphere:
    def __init__(self, center=(0, 0, 0), radius=1, material=GRAY_GLOSSY):
        self.center = np.array(center)
        self.radius = radius
        self.material = material

    def check_collision(self, eye, direction, near, far):
        collision_distance = None

        to_eye = eye - self.center
        a = np.dot(direction, direction)
        b = 2*np.dot(to_eye, direction)
        c = np.dot(to_eye, to_eye) - self.radius**2
        delta = b**2 - 4*a*c

        if delta > 0:
            distance1 = (-b - math.sqrt(delta)) / (2*a)
            distance2 = (-b + math.sqrt(delta)) / (2*a)
            collision_distance = min((d for d in (distance1, distance2) if near <= d <= far), default=None)
        elif delta == 0:
            distance = -b / (2*a)
            if near <= distance <= far:
                collision_distance = distance

        if collision_distance:
            collision_point = eye + direction*collision_distance
            normal = collision_point - self.center
            normal /= np.linalg.norm(normal)
            return CollisionResult(collision_point, normal, self.material)
        else:
            return None


class Plane:
    def __init__(self, position=(0, 0, 0), normal=(0, 1, 0), material=GRAY_GLOSSY):
        self.position = np.array(position)
        self.normal = normal / np.linalg.norm(normal)
        self.material = material

    def check_collision(self, eye, direction, near, far):
        d = np.dot(direction, self.normal)
        if d != 0:
            distance = np.dot(self.normal, (self.position - eye)) / d
            if near <= distance <= far:
                return CollisionResult(eye + direction*distance, self.normal, self.material)
        return None


class Circle:
    def __init__(self, center=(0, 0, 0), normal=(0, 1, 0), radius=1, front_material=GRAY_GLOSSY, back_material=None):
        if back_material is None:
            back_material = front_material
        normal = np.array(normal)
        self.front_plane = Plane(center, normal, front_material)
        self.back_plane = Plane(center, -normal, back_material)
        self.radius = radius

    def check_collision(self, eye, direction, near, far):
        if np.dot(direction, self.front_plane.normal) < 0:
            collision_result = self.front_plane.check_collision(eye, direction, near, far)
        else:
            collision_result = self.back_plane.check_collision(eye, direction, near, far)
        if collision_result:
            distance = np.linalg.norm(self.front_plane.position - collision_result.point)
            if distance <= self.radius:
                return collision_result
        else:
            return None
