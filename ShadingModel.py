import numpy


def reflection(vector, normal):
    vec = vector
    vec = vec / numpy.linalg.norm(vec)
    reflection = (vec - normal * 2.0 * numpy.dot(vec, normal)) * numpy.dot(vector, vector)
    return reflection

class PhongShadingModel:
    def calculate_color(self, collisionResult, scene, eye):
        color = [int(collisionResult.material.ambientCoeff*x*y/255) for x, y in zip(collisionResult.material.ambientColor, scene.ambientColor)]
        
        V = eye - collisionResult.collisionPoint
        V = V / numpy.linalg.norm(V)
        
        for light in scene.lights:
            L = light.pos - collisionResult.collisionPoint
            l = numpy.linalg.norm(L)
            L = L / numpy.linalg.norm(L)
            if not scene.collision(collisionResult.collisionPoint, L, 0.00001, l).isCollision:
                lightColor = light.get_light_intensity(collisionResult.collisionPoint)
                R = reflection(-L, collisionResult.normal)
                R = R / numpy.linalg.norm(R)
                coeff1 = numpy.dot(L, collisionResult.normal)
                coeff1 = max(coeff1, 0.0)
                diffColor = [int(x * y * collisionResult.material.diffuseCoeff * coeff1/255) for x,y in zip(collisionResult.material.diffuseColor, lightColor)]
                color = [x + y for x, y in zip(color, diffColor)]
                coeff2 = numpy.dot(R, V)
                coeff2 = max(coeff2, 0.0);
                coeff2 = coeff2**collisionResult.material.exponent
                specColor = [int(x * y * collisionResult.material.specularCoeff * coeff2/255) for x,y in zip(collisionResult.material.specularColor, lightColor)]
                color = [x + y for x, y in zip(color, specColor)]
        
        
        return color