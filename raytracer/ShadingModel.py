import numpy


def reflection(vector, normal):
    vec = vector
    vec = vec / numpy.linalg.norm(vec)
    reflection = (vec - normal * 2.0 * numpy.dot(vec, normal)) * numpy.dot(vector, vector)
    return reflection

class PhongShadingModel:
    def calculate_color(self, collision_result, scene, eye):
        material = collision_result.material
        color = tuple(int(material['ambient_coeff']*x*y/255) for x, y in zip(material['ambient_color'], scene.ambientColor))
        
        V = eye - collision_result.collisionPoint
        V = V / numpy.linalg.norm(V)
        
        for light in scene.lights:
            L = light.pos - collision_result.collisionPoint
            l = numpy.linalg.norm(L)
            L = L / numpy.linalg.norm(L)
            if not scene.collision(collision_result.collisionPoint, L, 0.00001, l).isCollision:
                lightColor = light.get_light_intensity_at(collision_result.collisionPoint)
                R = reflection(-L, collision_result.normal)
                R = R / numpy.linalg.norm(R)
                coeff1 = numpy.dot(L, collision_result.normal)
                coeff1 = max(coeff1, 0.0)
                diffColor = [int(x * y * material['diffuse_coeff'] * coeff1/255) for x,y in zip(material['diffuse_color'], lightColor)]
                color = tuple(x + y for x, y in zip(color, diffColor))
                coeff2 = numpy.dot(R, V)
                coeff2 = max(coeff2, 0.0)
                coeff2 = coeff2**material['exponent']
                specColor = [int(x * y * material['specular_coeff'] * coeff2/255) for x,y in zip(material['specular_color'], lightColor)]
                color = tuple(x + y for x, y in zip(color, specColor))

        if material['reflection'] > 0:
            reflected_vector = reflection(-V, collision_result.normal)
            reflected_color = scene.trace(collision_result.collisionPoint, reflected_vector, 0.00001, 100000)
            color = tuple(x + y for x, y in zip(color, reflected_color))
        
        return color
