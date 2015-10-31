import numpy
import math
import CollisionResult
import Material


class Sphere:
    def __init__(self, pos = numpy.array([0.0, 0.0, 0.0]), radius = 1.0, material = None):
        self.pos = pos
        self.radius = radius
        if material != None:
            self.material = material
        else:
            self.material = Material.Material()
            
            
    def collision(self, e, d, near, far):
        result = CollisionResult.CollisionResult()
        result.isCollision = False
        
        temp = e - self.pos
        a = numpy.dot(d, d)
        b = 2 * (numpy.dot(temp, d))
        c = numpy.dot(temp, temp) - (self.radius * self.radius)
        delta = b*b - 4*a*c
        
        if delta > 0:
            t1 = (-b - math.sqrt(delta)) / (2*a)
            t2 = (-b + math.sqrt(delta)) / (2*a)
            if (t1 >= near and t1 <= far) and (t2 >= near and t2 <= far):
                result.isCollision = True
                result.collisionDistance = min(t1, t2)
            elif t1 >= near and t1 <= far:
                result.isCollision = True
                result.collisionDistance = t1
            elif t2 >= near and t2 <= far:
                result.isCollision = True
                result.collisionDistance = t2
        elif delta == 0:
            t = -b / (2 * a);
            if (t >= near and t <= far):
                result.isCollision = True
                result.collisionDistance = t
                
        if result.isCollision:
            result.collisionPoint = d * result.collisionDistance + e
            normal = result.collisionPoint - self.pos
            normal = normal / numpy.linalg.norm(normal)
            result.normal = normal
            result.material = self.material
            
        return result
        