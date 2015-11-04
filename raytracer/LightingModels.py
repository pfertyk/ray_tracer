import numpy


def reflection(vector, normal):
    vec = vector
    vec = vec / numpy.linalg.norm(vec)
    reflection = (vec - normal * 2.0 * numpy.dot(vec, normal)) * numpy.dot(vector, vector)
    return reflection


def whitted_lighting_model(scene, eye, collision_result, level):
    collision_point, normal, material = collision_result
    color = (0, 0, 0)
    V = eye - collision_point
    V = V / numpy.linalg.norm(V)

    for light in scene.lights:
        if light.illuminates(collision_point, scene):
            light_vector = light.get_light_vector_at(collision_point)
            light_color = light.get_light_intensity_at(collision_point)
            coeff1 = 1
            if light_vector is not None:
                coeff1 = numpy.dot(-light_vector, normal)
                coeff1 = max(coeff1, 0.0)

                R = reflection(light_vector, normal)
                R = R / numpy.linalg.norm(R)
                coeff2 = numpy.dot(R, V)
                coeff2 = max(coeff2, 0.0)
                coeff2 = coeff2**material.phong_exponent
                specular = [int(x * y * coeff2/255) for x, y in zip(material.specular_color, light_color)]
                color = tuple(x + y for x, y in zip(color, specular))
            diffColor = [int(x * y * coeff1/255) for x, y in zip(material.color, light_color)]
            color = tuple(x + y for x, y in zip(color, diffColor))
    if material.reflection_factor > 0:
        reflected_vector = reflection(-V, normal)
        reflected_color = scene.trace_ray(collision_point, reflected_vector, level-1)
        color = tuple(x + y for x, y in zip(color, reflected_color))
    return color
