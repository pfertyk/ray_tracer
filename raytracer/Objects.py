"""
Contains scene objects.

Each object must implement a method check_collision(eye, direction, near, far). Vectors eye and direction represent \
the position and direction of a traced ray of light (direction must be normalized). Values near and far represent the\
minimal and maximal distance along the ray that a collision can occur (if a collision occurs outside of this range, \
it will not be detected). The value returned by this method is either None (if a collision with the object does not \
occur) or a tuple of (collision_point, normal, material). Collision point is a point at which the ray collides with \
the object, normal is a normalized normal vector at that point, and material is a material of given object.
"""
from collections import namedtuple
import numpy as np
import math
from raytracer.Materials import GRAY_GLOSSY

CollisionResult = namedtuple('CollisionResult', 'point normal material')


class Sphere:
    """
    Represents a sphere.

    Sphere is illuminated only from the outside. Inside can be illuminated using ambient light.

    :param center: center point of the sphere.
    :param radius: radius of the sphere (might be negative, in that case it will be converted to positive value)
    :param material: material of the sphere
    """
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
    """
    Represents an infinite plain.

    The plain is only illuminated from one side (the other can only be illuminated using ambient light).
    :param position: any point of this plane
    :param normal: normal vector of this plane (does not have to be normalized).
    :param material: material of the plane
    """
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
    """
    Represents a circle.

    Circle is a limited plane. Unlike a plane, it is properly illuminated from both sides.

    :param center: the center point of the circle
    :param normal: normal vector of the front side of the circle
    :param radius: radius of the circle
    :param front_material: material of the front side
    :param back_material: material of the back side (if not specified, front side material will be used)
    """
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
