"""Evaluate the volume of the solid between the paraboloids with SymPy.

In cylindrical coordinates about the y-axis the solid is r**2 <= y <= 8 - r**2
with 0 <= r <= 2, so the volume is the integral of (8 - 2 r**2) r over the disk.
"""

from sympy import Rational, integrate, pi, simplify, symbols

r, theta, y = symbols("r theta y", positive=True)

upper_paraboloid = 8 - r**2
lower_paraboloid = r**2

inner_integral = integrate(1, (y, lower_paraboloid, upper_paraboloid))
print(f"height of the solid at radius r: {simplify(inner_integral)}")

middle_integral = integrate(inner_integral * r, (r, 0, 2))
print(f"integrand after the height:      {simplify(inner_integral * r)}")
print(f"radial antiderivative:           {simplify(integrate(inner_integral * r, r))}")
print(f"radial integral r=0..2:          {simplify(middle_integral)}")

volume = simplify(integrate(middle_integral, (theta, 0, 2 * pi)))
print(f"volume:                          {volume}")
print(f"decimal value:                   {float(volume.evalf(15)):.6f}")

# Cross-check: sum the areas of the horizontal sections A(y) = pi * r**2.
section_area_low = simplify(pi * y)
section_area_high = simplify(pi * (8 - y))
section_total = simplify(
    integrate(section_area_low, (y, 0, 4)) + integrate(section_area_high, (y, 4, 8))
)
print(f"section area for 0<=y<=4:        {section_area_low}")
print(f"section area for 4<=y<=8:        {section_area_high}")
print(f"integral of the section areas:   {section_total}")

# Cross-check: the height 8 - 2 r**2 at r = 0 and r = 2.
height = simplify(upper_paraboloid - lower_paraboloid)
print(f"height 8 - 2r^2 at r=0:          {height.subs(r, 0)}")
print(f"height 8 - 2r^2 at r=2:          {height.subs(r, 2)}")

assert volume == 16 * pi
assert section_total == 16 * pi
print("the symbolic result equals 16*pi")
