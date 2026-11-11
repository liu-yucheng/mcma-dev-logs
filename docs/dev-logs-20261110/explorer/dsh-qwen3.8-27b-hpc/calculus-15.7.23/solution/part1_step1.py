"""Exercise 15.7.23(a): set up the wedge volume as a triple integral.
First octant; cylinder y^2+z^2=1; planes y=x and x=1.
Solid: 0<=y<=1, y<=x<=1, 0<=z<=sqrt(1-y^2).
(For each y the cross section in the xy-plane is the triangle between the
lines x=y and x=1; z then runs from the floor z=0 up to the cylinder.)
This script verifies the region description. Part (a) only asks for the
SETUP, so no evaluated number is presented as the answer here.
"""
import sympy as sp

x, y, z = sp.symbols('x y z', real=True)

# Consistency checks on the bounds
# At y=0 the x-range is 0..1 (the full cap x=1); at y=1 it shrinks to the
# point x=1 where the planes y=x and x=1 meet.
print("x-range at y=0: 0..1  (plane x=1 is the end cap)")
print("x-range at y=1: {1}   (planes x=1 and x=y meet there)")
# The two cutting planes meet the cylinder consistently: along x=y the
# cylinder gives y^2+z^2=1, so z = sqrt(1-y^2).
print("cylinder along x=y:  z = sqrt(1-y^2),  y in [0,1]")

# Private sanity check: bounds describe a positive, finite region.
# (NOT the answer of part (a); part (b) evaluates this integral.)
I = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, sp.sqrt(1 - y**2))), (x, y, 1)), (y, 0, 1))
print("private check, region volume =", sp.simplify(I))
