from utility import epsilon_equal

class Point:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
  def __eq__(self, other):
    return epsilon_equal(self.x, other.x) and epsilon_equal(self.y, other.y) and epsilon_equal(self.z, other.z)
  def __str__(self):
    return "<" + self.x.__str__() + ", " + self.y.__str__() + ", " + self.z.__str__() + ">"
  def __repr__(self):
    return self.__str__()

class Vector:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
  def __eq__(self, other):
    return epsilon_equal(self.x, other.x) and epsilon_equal(self.y, other.y) and epsilon_equal(self.z, other.z)
  def __str__(self):
    return "<" + self.x.__str__() + ", " + self.y.__str__() + ", " + self.z.__str__() + ">"
  def __repr__(self):
    return self.__str__()

class Ray:
  def __init__(self, pt, dir):
    self.pt = pt
    self.dir = dir
  def __eq__(self, other):
    return (self.pt == other.pt) and (self.dir == other.dir)
  def __str__(self):
    return "<pt:" + self.pt.__str__() + " v:" + self.dir.__str__() + ">"
  def __repr__(self):
    return self.__str__()

class Sphere:
  def __init__(self, center, radius, color, finish):
    self.center = center
    self.radius = radius
    self.color = color
    self.finish = finish
  def __eq__(self, other):
    return (self.center == other.center) and epsilon_equal(self.radius, other.radius)
  def __str__(self):
    return "<ct:" + self.center.__str__() + " r:" + self.radius.__str__() + ">"
  def __repr__(self):
    return self.__str__()

class Color:
  def __init__(self, red, green, blue):
    self.red = red
    self.green = green
    self.blue = blue
  def __eq__(self, other):
    return epsilon_equal(self.red, other.red) and epsilon_equal(self.green, other.green) and epsilon_equal(self.blue, other.blue)

class Finish:
  def __init__(self, ambient, diffuse, specular, roughness):
    self.ambient = ambient
    self.diffuse = diffuse
    self.specular = specular
    self.roughness = roughness
  def __eq__(self, other):
    return epsilon_equal(self.ambient, other.ambient) and epsilon_equal(self.diffuse, other.diffuse) and epsilon_equal(self.specular, other.specular) and epsilon_equal(self.roughness, other.roughness)

class Light:
  def __init__(self, pt, color):
    self.pt = pt
    self.color = color
  def __eq__(self, other):
    return self.pt == other.pt and self.color == other.color
