import math

import vector_math

vm = vector_math


def sphere_intersection_point(ray, sphere):
    a = vm.dot_vector(ray.dir, ray.dir)
    b = (2 * vm.dot_vector(vm.difference_point(ray.pt, sphere.center), ray.dir))
    c = vm.dot_vector(vm.difference_point(ray.pt, sphere.center),
                      vm.difference_point(ray.pt, sphere.center)) - sphere.radius ** 2

    dis = b ** 2 - 4 * a * c
    if dis < 0:
        return None

    root = math.sqrt(dis)

    oneRoot = (((-1 * b) + root)) / (2 * a)
    otherRoot = (((-1 * b) - root)) / (2 * a)

    t = -1
    if oneRoot >= 0 and otherRoot >= 0:
        t = otherRoot
    elif oneRoot >= 0:
        t = oneRoot
    else:
        return None
    return vm.translate_point(ray.pt, vm.scale_vector(ray.dir, t))


def find_intersection_points(sphere_list, ray):
    toReturn = []
    for i in sphere_list:
        val = sphere_intersection_point(ray, i)
        if (val != None):
            toReturn.append((i, val))
    return toReturn


def sphere_normal_at_point(sphere, point):
    theVector = vm.vector_from_to(sphere.center, point)
    return vm.normalize_vector(theVector)
