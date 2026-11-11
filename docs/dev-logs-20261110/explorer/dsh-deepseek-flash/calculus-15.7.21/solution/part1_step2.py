"""Evaluate the volume of the solid with SymPy.

The inner integral removes z and leaves the height 1 - y. The middle integral
removes y and leaves 1/2 - x**2 + x**4/2. The outer integral removes x. Two
further checks slice the solid by the planes y = constant and z = constant.
"""

from sympy import Rational, integrate, simplify, sqrt, symbols

x, y, z = symbols("x y z", real=True)

height = 1 - y
inner_integral = integrate(height, (y, x**2, 1))
print(f"inner integral over y:           {simplify(inner_integral)}")

antiderivative = integrate(inner_integral, x)
print(f"antiderivative in x:             {simplify(antiderivative)}")
print(f"value at x=1:                    {simplify(antiderivative.subs(x, 1))}")
print(f"value at x=-1:                   {simplify(antiderivative.subs(x, -1))}")

volume = simplify(integrate(inner_integral, (x, -1, 1)))
print(f"volume:                          {volume}")
print(f"decimal value:                   {float(volume.evalf(15)):.6f}")

# Check 1: sections at a fixed x are triangles, and their area integrates to the volume.
section_area = simplify(inner_integral)
print(f"section area at fixed x:         {section_area}")
print(f"section area at x=0:             {simplify(section_area.subs(x, 0))}")
print(f"section area at x=0.5:           {float(section_area.subs(x, 0.5)):.5f}")
print(f"lower edge y=x^2 at x=0.5:       {float(Rational(1, 4)):.5f}")
print(f"upper edge z=1-y at y=0.25:      {float(Rational(3, 4)):.5f}")
print(f"integral of the section areas:   {simplify(integrate(section_area, (x, -1, 1)))}")

# Check 2: sections at a fixed z are parabolic segments.
width = sqrt(1 - z)
section_area_z = simplify(integrate(1 - z - x**2, (x, -width, width)))
print(f"area of the section at height z: {simplify(section_area_z)}")
print(f"integral of the z-sections:      {simplify(integrate(section_area_z, (z, 0, 1)))}")

# Check 3: sections at a fixed y are rectangles of width 2 sqrt(y) and height 1 - y.
section_area_y = simplify(2 * sqrt(y) * (1 - y))
print(f"area of the section at y:        {section_area_y}")
print(f"integral of the y-sections:      {simplify(integrate(section_area_y, (y, 0, 1)))}")

assert volume == Rational(8, 15)
print("the symbolic result equals 8/15")
