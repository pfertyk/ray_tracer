import numpy as np


def whitted_lighting_model(scene, ray_direction, collision_result, recursion_level):
    collision_point, normal, material = collision_result
    color = np.array((0, 0, 0))

    for light in scene.lights:
        if light.illuminates(collision_point, scene):
            light_vector = light.get_light_vector_at(collision_point)
            light_color = light.get_light_intensity_at(collision_point)
            coeff1 = 1
            if light_vector is not None:
                coeff1 = np.dot(-light_vector, normal)
                coeff1 = max(coeff1, 0.0)

                reflected_light_vector = _reflection(light_vector, normal)
                coeff2 = np.dot(reflected_light_vector, -ray_direction)
                coeff2 = max(coeff2, 0.0)
                coeff2 = coeff2**material.phong_exponent
                specular = [int(x * y * coeff2/255) for x, y in zip(material.specular_color, light_color)]
                color = tuple(x + y for x, y in zip(color, specular))
            diffColor = [int(x * y * coeff1/255) for x, y in zip(material.color, light_color)]
            color = tuple(x + y for x, y in zip(color, diffColor))
    if material.reflection_factor > 0:
        reflected_vector = _reflection(ray_direction, normal)
        reflected_color = scene.trace_ray(collision_point, reflected_vector, recursion_level-1)
        color = tuple(x + y for x, y in zip(color, reflected_color))
    return tuple(color)


def _reflection(vector, normal):
    return vector - 2*(np.dot(vector, normal))*normal
