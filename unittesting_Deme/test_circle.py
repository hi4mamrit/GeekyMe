"""
unittest module for circle.py

How to test:-
put circle.py and test_circle.py in one folder  AND run:

=>python -m unittest test_circle.py
"""
from unittest import TestCase
from circle import circle_area
from math import pi

class TestCircleArea(TestCase):
  
  def test_area(self):
    #Test Area when radius > 0
    self.assertAlmostEqual(circle_area(1),pi)
    self.assertAlmostEqual(circle_area(0),0)
    self.assertAlmostEqual(circle_area(2),pi*(2**2))
    
  def test_value_error(self):
    #Raises ValueError when radius is negative
    self.assertRaises(ValueError,circle_area,-2)
    
  def test_type_error(self):
    #Raises TypeError for invalid types
    self.assertRaises(TypeError,circle_area,"amrit")
    self.assertRaises(TypeError,circle_area,2+3j)
    self.assertRaises(TypeError,circle_area,True)
    
