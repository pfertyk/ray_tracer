"""
Contains lighting models.

All vectors representing directions (normal vectors, ray vectors) passed to the
functions from this module have to be normalized, unless specified otherwise.
"""
import numpy as np


def whitted_lighting_model(scene, ray_direction, collision_result, recursion_level):
    """
    Represents lighting model with diffuse light, specular light and mirror reflections.

    This function calculates a color of a point as a sum of light it receives
    from all light sources on scene. If light source is directed, the diffuse light will
    be calculated using Lambertian reflectance and specular reflection will be added using
    Phong model. If the material is reflective, a reflected ray will be traced through the scene
    and its color added to the calculated color.
    :param scene: scene that is being rendered
    :param ray_direction: direction of a traced light ray
    :param collision_result: a tuple of (collision_point, normal_vector, object_material), cannot be None
    :param recursion_level: current recursion level for reflected rays
    :return: color as a tuple of 3 values (R, G, B), range 0 - 255.
    """
    collision_point, normal, material = collision_result
    color = np.array((0, 0, 0))
    for light in (light for light in scene.lights if light.illuminates(collision_point, scene)):
        light_color = light.get_light_intensity_at(collision_point)
        light_vector = light.get_light_vector_at(collision_point)
        if light_vector is not None:
            color += _calculate_diffuse_color(light_color, light_vector, material, normal)
            color += _calculate_specular_color(light_color, light_vector, material, normal, ray_direction)
        else:
            color += material.color * light_color / 255
    if material.reflection_factor > 0:
        reflected_vector = _reflection(ray_direction, normal)
        reflected_color = scene.trace_ray(collision_point, reflected_vector, recursion_level-1)
        color += np.array(reflected_color)
    return tuple(int(c) for c in color)


def _calculate_diffuse_color(light_color, light_vector, material, normal):
    """
    Calculates diffuse light using Lambertian reflectance.
    :return: numpy array of 3 values, range 0 - 255
    """
    diffuse_coefficient = max(np.dot(-light_vector, normal), 0)
    diffuse_color = np.multiply(material.color, light_color / 255) * diffuse_coefficient
    return diffuse_color


def _calculate_specular_color(light_color, light_vector, material, normal, ray_direction):
    """
    Calculates specular light using Phong reflection model.
    :return: numpy array of 3 values, range 0 - 255
    """
    reflected_light_vector = _reflection(light_vector, normal)
    specular_coefficient = max(np.dot(reflected_light_vector, -ray_direction), 0)**material.phong_exponent
    specular_color = np.multiply(material.specular_color, light_color / 255) * specular_coefficient
    return specular_color


def _reflection(vector, normal):
    """
    Creates a reflection of given vector in relation to given normal.
    """
    return vector - 2*(np.dot(vector, normal))*normal
