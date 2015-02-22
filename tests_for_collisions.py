import math
import unittest

import data
import collisions


magicValue = math.sqrt(3.0 / 2.0 - math.sqrt(2))


class Testing(unittest.TestCase):
    def test_sphere_intersection_1(self):
        sphere = data.Sphere(data.Point(5, 1, 0), 1)
        ray = data.Ray(data.Point(0, 0, 0), data.Vector(1, 0, 0))
        result = data.Point(5, 0, 0)
        compute = collisions.sphere_intersection_point(ray, sphere)
        self.assertEqual(compute == result, True)
        pass

    def test_sphere_intersection_2(self):
        sphere = data.Sphere(data.Point(1, 1, 0), 1)
        ray = data.Ray(data.Point(0, 0, 0), data.Vector(1, 1, 0))
        result = data.Point(magicValue, magicValue, 0)
        self.assertEqual(collisions.sphere_intersection_point(ray, sphere) == result, True)
        pass

    def test_sphere_intersection_3(self):
        sphere = data.Sphere(data.Point(1, 1, 1), 1)
        ray = data.Ray(data.Point(0, 0, 0), data.Vector(-1, -1, -1))
        result = None
        self.assertEqual(collisions.sphere_intersection_point(ray, sphere) == result, True)
        pass

    def test_find_intersection_1(self):
        t = math.sqrt(2)
        spheres = [data.Sphere(data.Point(1, 1, 0), t), data.Sphere(data.Point(2, 2, 0), t),
                   data.Sphere(data.Point(3, 3, 0), t)]
        ray = data.Ray(data.Point(0, 0, 0), data.Vector(1, 1, 0))
        result = [(spheres[0], data.Point(0, 0, 0)), (spheres[1], data.Point(1, 1, 0)),
                  (spheres[2], data.Point(2, 2, 0))]
        self.assertEqual(collisions.find_intersection_points(spheres, ray) == result, True)
        pass

    def test_find_intersection_2(self):
        spheres = [data.Sphere(data.Point(1, 1, 1), 1), data.Sphere(data.Point(2, 2, 2), 1),
                   data.Sphere(data.Point(3, 3, 3), 1)]
        ray = data.Ray(data.Point(0, 0, 0), data.Vector(1, 0, 0))
        result = []
        self.assertEqual(collisions.find_intersection_points(spheres, ray) == result, True)
        pass

    def test_sphere_1(self):
        sphere = data.Sphere(data.Point(0, 0, 0), 1)
        point = data.Point(0, 1, 0)
        result = data.Vector(0, 1, 0)
        self.assertEqual(collisions.sphere_normal_at_point(sphere, point) == result, True)
        pass

    def test_sphere_2(self):
        sphere = data.Sphere(data.Point(1, 0, 0), 1)
        point = data.Point(0, 0, 0)
        result = data.Vector(-1, 0, 0)
        self.assertEqual(collisions.sphere_normal_at_point(sphere, point) == result, True)
        pass


if __name__ == "__main__":
    unittest.main()
