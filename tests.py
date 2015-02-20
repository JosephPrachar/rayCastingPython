import math
import unittest
import data
import cast
import vector_math

# global setup for cast_ray
eye = data.Point(0.0, 0.0, -14.0)
spheres = [data.Sphere(data.Point(.5, 1.5, -3.0), 0.5, data.Color(1, 0, 0), data.Finish(.4, .4, .5, .05)),
            data.Sphere(data.Point(1.0, 1.0, 0.0), 2.0, data.Color(0, 0, 1), data.Finish(.2, .4, .5, .05))]
ambientColor = data.Color(1.0,1.0,1.0)
pointLight = data.Light(data.Point(-100.0, 100.0, -100.0), data.Color(1.5,1.5,1.5))
blackPointLight = data.Light(data.Point(-100.0, 100.0, -100.0), data.Color(0,0,0))

vm = vector_math

class Testing(unittest.TestCase):
    # Part 1
    def test_cast_ray_1(self):
        ray = data.Ray(eye, vm.vector_from_to(eye, spheres[0].center))
        result = cast.cast_ray(ray, spheres, ambientColor, blackPointLight, eye)
        self.assertEqual(result == data.Color(1.0, 1.0, 1.0), False)
        pass
    def test_cast_ray_2(self):
        ray = data.Ray(eye, vm.vector_from_to(spheres[0].center, eye))
        result = cast.cast_ray(ray, spheres, ambientColor, blackPointLight, eye)
        self.assertEqual(result == data.Color(1.0, 1.0, 1.0), True)
        pass
    # Part 2
    def test_cast_ray_3(self):
        ray = data.Ray(eye, vm.vector_from_to(eye, spheres[0].center))
        result = cast.cast_ray(ray, spheres, ambientColor, blackPointLight, eye)
        self.assertEqual(result.red > result.green and result.red > result.blue, True)  #ensure that the dominant color is red
        pass
    def test_cast_ray_4(self):
        ray = data.Ray(eye, vm.vector_from_to(eye, spheres[1].center))
        result = cast.cast_ray(ray, spheres, ambientColor, blackPointLight, eye)
        self.assertEqual(result.green < result.blue and result.blue > result.red, True) #ensure that the dominant color is blue
        pass

    def test_color_mult_1(self):
        one = data.Color(1,1,1)
        two = data.Color(.5, .5, .5)
        result = cast.color_mult(one, two)
        val = data.Color(.5, .5, .5)
        self.assertEqual(result == val, True)
        pass
    def test_color_mult_2(self):
        one = data.Color(1, 1.5, .5)
        two = data.Color(.5, .5, .5)
        result = cast.color_mult(one, two)
        val = data.Color(.5, .75, .25)
        self.assertEqual(result == val, True)
        pass

    def test_color_add_1(self):
        one = data.Color(1,1,1)
        two = data.Color(.5, .5, .5)
        result = cast.color_add(one, two)
        val = data.Color(1.5, 1.5, 1.5)
        self.assertEqual(result == val, True)
        pass
    def test_color_add_2(self):
        one = data.Color(1, 2, 3)
        two = data.Color(0, .5, 1)
        result = cast.color_add(one, two)
        val = data.Color(1, 2.5, 4)
        self.assertEqual(result == val, True)
        pass

    def test_color_scale_1(self):
        one = data.Color(1,1,1)
        two = 5
        result = cast.color_scale(one, two)
        val = data.Color(5, 5, 5)
        self.assertEqual(result == val, True)
        pass
    def test_color_scale_2(self):
        one = data.Color(1,1,1)
        two = 0
        result = cast.color_scale(one, two)
        val = data.Color(0,0,0)
        self.assertEqual(result == val, True)
        pass

    def test_color_bounds_1(self):
        one = data.Color(.5, .3, .2)
        cast.color_bounds_check(one)
        val = data.Color(.5, .3, .2)
        self.assertEqual(one == val, True)
        pass
    def test_color_bounds_2(self):
        one = data.Color(1.5, 1.3, 1.2)
        cast.color_bounds_check(one)
        val = data.Color(1, 1, 1)
        self.assertEqual(one == val, True)
        pass    

if __name__ == "__main__":
  unittest.main()
