import numpy


def reflection(vector, normal):
    vec = vector
    vec = vec / numpy.linalg.norm(vec)
    reflection = (vec - normal * 2.0 * numpy.dot(vec, normal)) * numpy.dot(vector, vector)
    return reflection


def whitted_lighting_model(scene, eye, collision_result, level):
    point, normal, material = collision_result
    color = tuple(int(material['ambient_coeff']*x*y/255) for x, y in zip(material['ambient_color'], scene.ambientColor))

    V = eye - point
    V = V / numpy.linalg.norm(V)

    for light in scene.lights:
        L = light.pos - point
        l = numpy.linalg.norm(L)
        L = L / numpy.linalg.norm(L)
        if not scene.collision(point, L, 0.00001, l):
            lightColor = light.get_light_intensity_at(point)
            R = reflection(-L, normal)
            R = R / numpy.linalg.norm(R)
            coeff1 = numpy.dot(L, normal)
            coeff1 = max(coeff1, 0.0)
            diffColor = [int(x * y * material['diffuse_coeff'] * coeff1/255) for x,y in zip(material['diffuse_color'], lightColor)]
            color = tuple(x + y for x, y in zip(color, diffColor))
            coeff2 = numpy.dot(R, V)
            coeff2 = max(coeff2, 0.0)
            coeff2 = coeff2**material['exponent']
            specColor = [int(x * y * material['specular_coeff'] * coeff2/255) for x,y in zip(material['specular_color'], lightColor)]
            color = tuple(x + y for x, y in zip(color, specColor))
    if material['reflection'] > 0:
        reflected_vector = reflection(-V, normal)
        reflected_color = scene.trace_ray(point, reflected_vector, 0.00001, 100000, level-1)
        color = tuple(x + y for x, y in zip(color, reflected_color))
    return color
