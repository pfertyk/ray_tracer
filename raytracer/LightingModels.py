import numpy as np


def whitted_lighting_model(scene, ray_direction, collision_result, recursion_level):
    collision_point, normal, material = collision_result
    color = np.array((0, 0, 0))

    for light in scene.lights:
        if light.illuminates(collision_point, scene):
            light_vector = light.get_light_vector_at(collision_point)
            light_color = light.get_light_intensity_at(collision_point)
            if light_vector is not None:
                coeff1 = np.dot(-light_vector, normal)
                coeff1 = max(coeff1, 0.0)

                specular_color = _calculate_specular_color(light_color, light_vector, material, normal, ray_direction)
                color += specular_color
                diffColor = [int(x * y * coeff1/255) for x, y in zip(material.color, light_color)]
                color = tuple(x + y for x, y in zip(color, diffColor))
            else:
                color += material.color * light_color / 255
    if material.reflection_factor > 0:
        reflected_vector = _reflection(ray_direction, normal)
        reflected_color = scene.trace_ray(collision_point, reflected_vector, recursion_level-1)
        color += np.array(reflected_color)
    return tuple(int(c) for c in color)


def _calculate_specular_color(light_color, light_vector, material, normal, ray_direction):
    reflected_light_vector = _reflection(light_vector, normal)
    specular_coefficient = max(np.dot(reflected_light_vector, -ray_direction), 0)**material.phong_exponent
    specular = np.multiply(material.specular_color, light_color / 255) * specular_coefficient
    return specular


def _reflection(vector, normal):
    return vector - 2*(np.dot(vector, normal))*normal
