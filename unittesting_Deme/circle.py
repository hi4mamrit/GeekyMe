"""
A simple module to calculate area of a circle
"""
from math import pi

def circle_area(r):
#Calculates the area of circle
	if type(r) not in (int,float):
		raise TypeError("radius should be of int or float type. ")
	if r<0:
		raise ValueError("radius cannot be negative. ")
	return pi*(r**2)
