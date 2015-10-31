import numpy
import CollisionResult
import Material


class Plane:
    def __init__(self, pos = numpy.array([0.0, 0.0, 0.0]), normal = numpy.array([0.0, 1.0, 0.0]),  material = None):
        self.pos = pos
        normal = normal / numpy.linalg.norm(normal)
        
        self.normal = normal
        if material != None:
            self.material = material
        else:
            self.material = Material.Material()
        
    def collision(self, e, d, near, far):
        result = CollisionResult.CollisionResult()
        result.isCollision = False;
        det = numpy.dot(d, self.normal)
        if det != 0:
            t = numpy.dot(self.normal, (self.pos - e)) / det;
            if t >= near and t <= far:
                result.isCollision = True;
                result.collisionDistance = t;
                result.material = self.material;
                result.normal = self.normal
                result.collisionPoint = d * t + e;
        return result; 