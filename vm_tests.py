import unittest
import vector_math
import data
import math

class TestData(unittest.TestCase):

# equivilance testing

  def test_vector_eq_1(self):
    v1 = data.Vector(1,2,3)
    v2 = data.Vector(1,2,3)
    self.assertEqual(v1 == v2, True)
    pass
  def test_vector_eq_2(self):
    v1 = data.Vector(1,2,3)
    v2 = data.Vector(0,0,0)
    self.assertEqual(v1 == v2, False)
    v1.x = 0
    self.assertEqual(v1 == v2, False)
    pass

  def test_point_eq_1(self):
    v1 = data.Point(1,2,3)
    v2 = data.Point(1,2,3)
    self.assertEqual(v1 == v2, True)
    pass
  def test_point_eq_2(self):
    v1 = data.Point(1,2,3)
    v2 = data.Point(0,0,0)
    self.assertEqual(v1 == v2, False)
    v1.x = 0
    self.assertEqual(v1 == v2, False)
    pass

  def test_ray_eq_1(self):
    v1 = data.Ray(data.Point(1,2,3), data.Vector(4,5,6))
    v2 = data.Ray(data.Point(1,2,3), data.Vector(4,5,6))
    self.assertEqual(v1 == v2, True)
    pass
  def test_ray_eq_2(self):
    v1 = data.Ray(data.Point(1,2,3), data.Vector(4,5,6))
    v2 = data.Ray(data.Point(4,5,6), data.Vector(3,2,1))
    self.assertEqual(v1 == v2, False)
    pass

  def test_sphere_eq_1(self):
    v1 = data.Sphere(data.Point(1,2,3), 10)
    v2 = data.Sphere(data.Point(1,2,3), 10)
    self.assertEqual(v1 == v2, True)
    pass
  def test_sphere_eq_2(self): 
    v1 = data.Sphere(data.Point(1,2,3), 110)
    v2 = data.Sphere(data.Point(1,2,3), 10)
    self.assertEqual(v1 == v2, False)
    pass

# vector_math functions testing

  def test_scale_1(self):
    v = data.Vector(1,2,3)
    v = vector_math.scale_vector(v, 2)
    self.assertAlmostEqual(v.x, 2)
    self.assertAlmostEqual(v.y, 4)
    self.assertAlmostEqual(v.z, 6)
    pass
  def test_scale_2(self):
    v = data.Vector(0, .5, .75)
    v = vector_math.scale_vector(v, 100)
    self.assertAlmostEqual(v.x, 0)
    self.assertAlmostEqual(v.y, 50)
    self.assertAlmostEqual(v.z, 75)    
    pass

  def test_dot_1(self):
    v1 = data.Vector(1,2,3)
    v2 = data.Vector(4,5,6)
    dot = vector_math.dot_vector(v1, v2)
    self.assertAlmostEqual(dot, 32)

    pass
  def test_dot_2(self):
    v1 = data.Vector(0, .5, 1.5)
    v2 = data.Vector(4, 6, 8)
    dot = vector_math.dot_vector(v1, v2)
    self.assertAlmostEqual(dot, 15)
    pass

  def test_length_1(self):
    v = data.Vector(3,4,5)
    length = vector_math.length_vector(v)
    self.assertAlmostEqual(length, math.sqrt(50))
    pass
  def test_length_2(self):
    v = data.Vector(-6,-8,-10)
    length = vector_math.length_vector(v)
    self.assertAlmostEqual(length, math.sqrt(200))
    pass

  def test_normalize_1(self):
    v = data.Vector(3,4,5)
    l = vector_math.length_vector(v)
    n = vector_math.normalize_vector(v)
    ln = vector_math.length_vector(n)
    self.assertAlmostEqual(ln, 1)
    self.assertAlmostEqual(n.x, 3/l)
    self.assertAlmostEqual(n.y, 4/l)
    self.assertAlmostEqual(n.z, 5/l)
    pass
  def test_normalize_2(self):
    v = data.Vector(-6, -8, -10)
    l = vector_math.length_vector(v)
    n = vector_math.normalize_vector(v)
    ln = vector_math.length_vector(n)
    self.assertAlmostEqual(ln, 1)
    self.assertAlmostEqual(n.x, -6/l)
    self.assertAlmostEqual(n.y, -8/l)
    self.assertAlmostEqual(n.z, -10/l)
    pass

  def test_pointDiff_1(self):
    p1 = data.Point(1,2,3)
    p2 = data.Point(1,2,3)
    equals = data.Point(0,0,0)
    self.assertEqual(vector_math.difference_point(p1, p2) == equals, True)    
    pass
  def test_pointDiff_2(self):
    p1 = data.Point(4,5,6)
    p2 = data.Point(3,2,1)
    equals = data.Point(1, 3, 5)
    self.assertEqual(vector_math.difference_point(p1, p2) == equals, True)
    pass

  def test_vectorDiff_1(self):
    v1 = data.Vector(1,2,3)
    v2 = data.Vector(1,2,3)
    equals = data.Point(0,0,0)
    self.assertEqual(vector_math.difference_vector(v1, v2) == equals, True)
    pass
  def test_vectorDiff_2(self):
    v1 = data.Vector(4,5,6)
    v2 = data.Vector(3,2,1)
    equals = data.Vector(1,3,5)
    self.assertEqual(vector_math.difference_vector(v1,v2) == equals, True)
    pass

  def test_translate_1(self):
    p = data.Point(1,2,3)
    v = data.Vector(0,0,0)
    newp = vector_math.translate_point(p, v)
    self.assertEqual(p == newp, True)
    pass
  def test_translate_2(self):
    p = data.Point(1,2,3)
    v = data.Vector(4,5,6)
    newp = vector_math.translate_point(p, v)
    equals = data.Point(5, 7, 9)
    self.assertEqual(newp == equals, True)
    pass

  def test_vectorToFrom_1(self):
    p1 = data.Point(1,2,3)
    p2 = data.Point(0,0,0)
    v1 = vector_math.vector_from_to(p1, p2)
    v2 = vector_math.vector_from_to(p2, p1)
    equals1 = data.Vector(-1, -2, -3)
    equals2 = vector_math.scale_vector(v1, -1)
    self.assertEqual(v1 == equals1, True)
    self.assertEqual(v2 == equals2, True)
    pass
  def test_vectorToFrom_2(self):
    p1 = data.Point(4,4,4)
    p2 = data.Point(1,2,3)
    v1 = vector_math.vector_from_to(p1, p2)
    equals = data.Vector(-3, -2, -1)
    self.assertEqual(v1 == equals, True)
    pass

if __name__ == "__main__":
  unittest.main()
