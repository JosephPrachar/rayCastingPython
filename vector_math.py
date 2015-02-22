import data
import funcs
import math


def scale_vector(vector, scalar):
    return data.Vector(vector.x * scalar, vector.y * scalar, vector.z * scalar)


def dot_vector(vector1, vector2):
    return (vector1.x * vector2.x) + (vector1.y * vector2.y) + (vector1.z * vector2.z)


def length_vector(vector):
    #return funcs.hypotenuse(vector.z, funcs.hypotenuse(vector.x, vector.y))
    return math.sqrt(vector.x ** 2 + vector.y ** 2 + vector.z ** 2)


def normalize_vector(vector):
    factor = 1.0 / length_vector(vector)
    return scale_vector(vector, factor)


def difference_point(point1, point2):
    return data.Vector(point1.x - point2.x, point1.y - point2.y, point1.z - point2.z)


def difference_vector(vector1, vector2):
    return data.Vector(vector1.x - vector2.x, vector1.y - vector2.y, vector1.z - vector2.z)


def translate_point(point, vector):
    return data.Point(point.x + vector.x, point.y + vector.y, point.z + vector.z)


def vector_from_to(from_point, to_point):
    return data.Vector(to_point.x - from_point.x, to_point.y - from_point.y, to_point.z - from_point.z)

# global
max_pixel_val = 255

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

def distance_point(pt_one, pt_two):
    return length_vector(vector_from_to(pt_one, pt_two))