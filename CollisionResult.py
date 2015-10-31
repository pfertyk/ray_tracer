import Material


class CollisionResult:
    def __init__(self):
        self.collisionDistance = 0.0
        self.material = Material.Material()
        self.isCollision = False