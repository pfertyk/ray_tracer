import CollisionResult
import ShadingModel


class Scene:
    def __init__(self, background_color=(0, 0, 0)):
        self.objects = []
        self.lights = []
        self.background_color = background_color
        self.shadingModel = ShadingModel.PhongShadingModel()
        self.ambientColor = (127, 127, 127)
    
    def collision(self, e, d, near, far):
        collision_result = CollisionResult.CollisionResult()
        collision_result.collisionDistance = far
        collision_result.isCollision = False
        
        for obj in self.objects:
            temp_result = obj.collision(e, d, near, collision_result.collisionDistance)
            if temp_result.isCollision:
                collision_result = temp_result
        
        return collision_result
    
    def trace(self, e, d, near, far):
        collision_result = self.collision(e, d, near, far)
        if not collision_result.isCollision:
            return self.background_color
        else:
            color = self.shadingModel.calculate_color(collision_result, self, e)
            return color
