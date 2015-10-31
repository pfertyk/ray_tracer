import CollisionResult
import ShadingModel


class Scene:
    def __init__(self, backgroundColor = [0, 0, 0]):
        self.objects = []
        self.lights = []
        self.backgroundColor = backgroundColor
        self.shadingModel = ShadingModel.PhongShadingModel()
        self.ambientColor = [127, 127, 127]
    
    def collision(self, e, d, near, far):
        collisionResult = CollisionResult.CollisionResult()
        collisionResult.collisionDistance = far
        collisionResult.isCollision = False
        
        for obj in self.objects:
            tempResult = obj.collision(e, d, near, collisionResult.collisionDistance)
            if tempResult.isCollision:
                collisionResult = tempResult
        
        return collisionResult
    
    def trace(self, e, d, near, far, eye):
        collisionResult = self.collision(e, d, near, far)
        if not collisionResult.isCollision :
            return self.backgroundColor
        else:
            color = self.shadingModel.calculate_color(collisionResult, self, eye);
            return color; 