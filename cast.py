import collisions
import vector_math
import data
import sys
import datetime

# shorten libs
col = collisions
vm = vector_math

#global
max_pixel_val = 255


def cast_ray(ray, sphere_list, color, light, eye):
    hits = col.find_intersection_points(sphere_list, ray)
    if (len(hits) == 0):
        return data.Color(1.0, 1.0, 1.0)
    else:
        small = 0
        for i in range(1, len(hits)):
            cur = vm.length_vector(vm.difference_point(ray.pt, hits[i][1]))
            smallest = vm.length_vector(vm.difference_point(ray.pt, hits[small][1]))
            if cur < smallest:
                small = i

        ambientColor = compute_ambient_lighting(hits[small][0], color)
        pointLighting = compute_point_and_specular_light(hits[small][1], hits[small][0], light, sphere_list, eye)

        return color_add(ambientColor, pointLighting)


def cast_all_rays(min_x, max_x, min_y, max_y, width, height, eye_point, sphere_list, color, light, output_file):
    deltaX = float(max_x - min_x) / width
    deltaY = float(max_y - min_y) / height
    y = max_y
    x = min_x

    while y > min_y:
        while x < max_x:
            pointToCastThrough = data.Point(x, y, 0)
            vectorToCast = vm.vector_from_to(eye_point, pointToCastThrough)
            rayThroughRec = data.Ray(eye_point, vectorToCast)

            result = cast_ray(rayThroughRec, sphere_list, color, light, eye_point)
            print_scaled_pixel(result, output_file)

            x += deltaX

        y -= deltaY
        x = min_x


def print_scaled_pixel(color, file):
    color_bounds_check(color)
    scaled_color = color_scale(color, max_pixel_val)
    file.write(str(int(scaled_color.red)) + ' ' + str(int(scaled_color.green)) + ' ' + str(int(scaled_color.blue)) + '\n')
    #print str(int(scaled_color.red)) + ' ' + str(int(scaled_color.green)) + ' ' + str(int(scaled_color.blue)) + '\n'

def color_mult(one, two):
    return data.Color(one.red * two.red, one.green * two.green, one.blue * two.blue)


def color_add(one, two):
    return data.Color(one.red + two.red, one.green + two.green, one.blue + two.blue)


def color_scale(color, val):
    return data.Color(color.red * val, color.green * val, color.blue * val)


def color_bounds_check(color):
    if color.red > 1.0:
        color.red = 1.0
    if color.green > 1.0:
        color.green = 1.0
    if color.blue > 1.0:
        color.blue = 1.0


def compute_ambient_lighting(sphere, color):
    ambientColor = color_mult(sphere.color, color)
    scaledAC = color_scale(ambientColor, sphere.finish.ambient)
    return scaledAC


def compute_point_and_specular_light(intersection_point, sphere, light, sphere_list, eye):
    # Point light
    normal = col.sphere_normal_at_point(sphere, intersection_point)  # N
    scaledNormal = vm.scale_vector(normal, .01)
    p_sub_e = vm.translate_point(intersection_point, scaledNormal)  # P sub E
    l_sub_dir = vm.normalize_vector(vm.vector_from_to(p_sub_e, light.pt))  # L sub dir
    l_dot_n = vm.dot_vector(normal, l_sub_dir)  #if neg diffuse is zero

    if l_dot_n <= 0:  # point on dark side of sphere
        return data.Color(0, 0, 0)

    rayToLight = data.Ray(p_sub_e, l_sub_dir)

    intersections = col.find_intersection_points(sphere_list, rayToLight)

    if (len(intersections) > 0):
        distToLight = vm.length_vector(vm.difference_point(light.pt, p_sub_e))
        for i in range(len(intersections)):
            if vm.length_vector(vm.difference_point(rayToLight.pt, intersections[i][1])) < distToLight:
                return data.Color(0, 0, 0)  # sphere blocking light

    dotTimesDiffuse = l_dot_n * sphere.finish.diffuse
    lightTimesSphere = color_mult(light.color, sphere.color)
    pointColor = color_scale(lightTimesSphere, dotTimesDiffuse)  # formula to get final point light contribution

    # Specular light
    reflect = vm.difference_vector(l_sub_dir, vm.scale_vector(normal, 2 * l_dot_n))
    v_sub_dir = vm.normalize_vector(vm.vector_from_to(eye, p_sub_e))

    specIntense = vm.dot_vector(reflect, v_sub_dir)
    specColor = data.Color(0, 0, 0)
    if specIntense > 0:
        scale = sphere.finish.specular * pow(specIntense, (1.0 / sphere.finish.roughness))
        specColor = color_scale(light.color, scale)

    return color_add(pointColor, specColor)
    

