import numpy as np


def whitted_lighting_model(scene, ray_direction, collision_result, recursion_level):
    collision_point, normal, material = collision_result
    color = np.array((0, 0, 0))
    for light in (light for light in scene.lights if light.illuminates(collision_point, scene)):
        light_color = light.get_light_intensity_at(collision_point)
        light_vector = light.get_light_vector_at(collision_point)
        if light_vector is not None:
            color += _calculate_specular_color(light_color, light_vector, material, normal, ray_direction)
            color += _calculate_diffuse_color(light_color, light_vector, material, normal)
        else:
            color += material.color * light_color / 255
    if material.reflection_factor > 0:
        reflected_vector = _reflection(ray_direction, normal)
        reflected_color = scene.trace_ray(collision_point, reflected_vector, recursion_level-1)
        color += np.array(reflected_color)
    return tuple(int(c) for c in color)


def _calculate_diffuse_color(light_color, light_vector, material, normal):
    diffuse_coefficient = max(np.dot(-light_vector, normal), 0)
    diffuse_color = np.multiply(material.color, light_color / 255) * diffuse_coefficient
    return diffuse_color


def _calculate_specular_color(light_color, light_vector, material, normal, ray_direction):
    reflected_light_vector = _reflection(light_vector, normal)
    specular_coefficient = max(np.dot(reflected_light_vector, -ray_direction), 0)**material.phong_exponent
    specular_color = np.multiply(material.specular_color, light_color / 255) * specular_coefficient
    return specular_color


def _reflection(vector, normal):
    return vector - 2*(np.dot(vector, normal))*normal
