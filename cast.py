import sys
import datetime

import collisions
import vector_math
import data


# shorten libs
col = collisions
vm = vector_math

# global
max_pixel_val = 255


def cast_ray(ray, sphere_list, color, light, eye, collision_sphere):
    hits = col.sphere_intersection_point_tuple(ray, collision_sphere)
    if hits[1] is None:
        return cast_ray_complete(ray, sphere_list, color, light, eye)

    ambientColor = compute_ambient_lighting(hits[0], color)
    pointLighting = compute_point_and_specular_light(hits[1], hits[0], light, sphere_list, eye)

    return vm.color_add(ambientColor, pointLighting)


def cast_ray_complete(ray, sphere_list, color, light, eye):
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

        return vm.color_add(ambientColor, pointLighting)


def cast_all_rays(min_x, max_x, min_y, max_y, width, height, eye_point, sphere_list, color, light, output_file):
    circle_projections = [project_sphere_on_window(cur_sphere, eye_point) for cur_sphere in sphere_list]
    # circle_projections = (sphere, circle_projection, dist from eye to sphere)

    sorted(circle_projections, key=lambda dist: dist[2])

    total_pixels = width * height

    before_time = datetime.datetime.now()
    for i in range(1000):
        cast_ray(data.Ray(eye_point, vm.vector_from_to(eye_point, sphere_list[0].center)),
                 sphere_list, color, light, eye_point)
    after_time = datetime.datetime.now()
    delta_time = after_time - before_time
    low_est = delta_time * int(total_pixels / 1000)
    high_est = low_est * 2

    print total_pixels, 'rays to cast on ', len(sphere_list), 'spheres'
    print 'time estimate: ', str(low_est), "- ", str(high_est)
    print 'start' + (' ' * 41) + 'done'
    print ('|' + (' ' * 9)) * 6

    deltaX = float(max_x - min_x) / width
    deltaY = float(max_y - min_y) / height
    y = max_y
    x = min_x

    count = 0
    while y > min_y:
        while x < max_x:
            circle_hits = point_in_circles(circle_projections, data.Point(x, y, 0))  # gets all intersecting spheres
            result = data.Color(1, 1, 1)

            if len(circle_hits) != 0:  # if the current point actually hits a sphere run computation
                pointToCastThrough = data.Point(x, y, 0)
                vectorToCast = vm.vector_from_to(eye_point, pointToCastThrough)
                rayThroughRec = data.Ray(eye_point, vectorToCast)

                result = cast_ray(rayThroughRec, sphere_list, color, light, eye_point, circle_hits[0][0])

            print_scaled_pixel(result, output_file)

            x += deltaX
            count += 1
            if count % 1000:
                if count > total_pixels / 50:
                    count = 0
                    sys.stderr.write('=')
        y -= deltaY
        x = min_x
    sys.stderr.write('==\n')


def print_scaled_pixel(color, file):
    vm.color_bounds_check(color)
    scaled_color = vm.color_scale(color, max_pixel_val)
    file.write(
        str(int(scaled_color.red)) + ' ' + str(int(scaled_color.green)) + ' ' + str(int(scaled_color.blue)) + '\n')


def compute_ambient_lighting(sphere, color):
    ambientColor = vm.color_mult(sphere.color, color)
    scaledAC = vm.color_scale(ambientColor, sphere.finish.ambient)
    return scaledAC


def compute_point_and_specular_light(intersection_point, sphere, light, sphere_list, eye):
    # Point light
    normal = col.sphere_normal_at_point(sphere, intersection_point)  # N
    scaledNormal = vm.scale_vector(normal, .01)
    p_sub_e = vm.translate_point(intersection_point, scaledNormal)  # P sub E
    l_sub_dir = vm.normalize_vector(vm.vector_from_to(p_sub_e, light.pt))  # L sub dir
    l_dot_n = vm.dot_vector(normal, l_sub_dir)  # if neg diffuse is zero

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
    lightTimesSphere = vm.color_mult(light.color, sphere.color)
    pointColor = vm.color_scale(lightTimesSphere, dotTimesDiffuse)  # formula to get final point light contribution

    # Specular light
    reflect = vm.difference_vector(l_sub_dir, vm.scale_vector(normal, 2 * l_dot_n))
    v_sub_dir = vm.normalize_vector(vm.vector_from_to(eye, p_sub_e))

    specIntense = vm.dot_vector(reflect, v_sub_dir)
    specColor = data.Color(0, 0, 0)
    if specIntense > 0:
        scale = sphere.finish.specular * pow(specIntense, (1.0 / sphere.finish.roughness))
        specColor = vm.color_scale(light.color, scale)

    return vm.color_add(pointColor, specColor)


def project_sphere_on_window(sphere, eye):
    # 1. find line from eye to center of sphere
    # 2. plug in z=0 to line to find center of circle on window
    # 3. use similar triangles to find radius of circle on window

    # 1.
    eye_to_sphere = vm.vector_from_to(eye, sphere.center)

    # 2.
    t = (-1 * eye.z) / eye_to_sphere.z
    eye_to_window = vm.scale_vector(eye_to_sphere, t)
    circle_center = vm.translate_point(eye, eye_to_window)

    # 3.
    dist_to_sphere = vm.length_vector(eye_to_sphere)
    radius = (sphere.radius * vm.length_vector(eye_to_window)) / dist_to_sphere

    # DONE: todo: possible addition to function
    # return a tuple of (sphere, circle, dist(eye, sphere))
    # this will allow cast ray to not have to run find_intersection_points() to get the nearest sphere

    return sphere, data.Circle(circle_center, radius), dist_to_sphere


def point_in_circles(circle_tuple, pt):
    # return [(sphere, circle, dist) for (sphere, circle, dist) in circle_tuple if point_in_circle(circle, pt)]
    return [tuple for tuple in circle_tuple if point_in_circle(tuple[1], pt)]


def point_in_circle(circle, pt):
    if (circle.center.z != pt.z):
        return False

    if (vm.distance_point(circle.center, pt) <= circle.radius + .1):
        return True
    else:
        return False
