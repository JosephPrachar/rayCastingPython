import collisions
import vector_math
import data

# shorten libs
col = collisions
vm = vector_math


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

        return vm.color_add(ambientColor, pointLighting)


def cast_all_rays(min_x, max_x, min_y, max_y, width, height, eye_point, sphere_list, color, light):
    deltaX = float(max_x - min_x) / width
    deltaY = float(max_y - min_y) / height
    y = max_y
    x = min_x
    count = 0
    while y > min_y:
        while x < max_x:
            pointToCastThrough = data.Point(x, y, 0)
            vectorToCast = vm.vector_from_to(eye_point, pointToCastThrough)
            rayThroughRec = data.Ray(eye_point, vectorToCast)

            result = cast_ray(rayThroughRec, sphere_list, color, light, eye_point)
            print_scaled_pixel(result)

            x += deltaX
            count += 1
        y -= deltaY
        x = min_x


def print_scaled_pixel(color):
    vm.color_bounds_check(color)
    print int(color.red * vm.max_pixel_val), ' ', int(color.green * vm.max_pixel_val), ' ', int(
        color.blue * vm.max_pixel_val), ' ',


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


def compute_sphere_on_window(sphere, eye):
    # 1. find line from eye to center of sphere
    # 2. plug in z=0 to line to find center of circle on window
    # 3. use similar triangles to find radius of circle on window

    # 1.
    eye_to_sphere = vm.vector_from_to(eye, sphere.center)

    # 2.
    t = (-1 * eye.z) / eye_to_sphere.z
    eye_to_window = vm.scale_vector(eye_to_sphere, t)
    circle_center = vm.translate_point(eye, eye)

    # 3.
    radius = (sphere.radius * vm.length_vector(eye_to_window)) / vm.length_vector(eye_to_sphere)

    # possible addition to function
    # return a tuple of (circle, dist(eye, sphere)
    # this will allow cast ray to not have to run find_intersection_points() to get the nearest sphere

    return data.Circle(circle_center, radius)

  
  
  
  






















  

  
