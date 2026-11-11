"""Evaluate the volume of the wedge numerically with mpmath.

Two integration orders must agree with pi/4 - 1/3: the order dx dz dy that the text
uses and the order dz dx dy. The script also evaluates the integral of y over the
quarter disk, which produces the term 1/3.
"""

from mpmath import mp

mp.dps = 20
exact_value = mp.pi / 4 - mp.mpf(1) / 3

first_order = mp.quad(
    lambda y_value: mp.quad(
        lambda z_value: mp.quad(lambda x_value: 1, [y_value, 1]),
        [0, mp.sqrt(1 - y_value**2)],
    ),
    [0, 1],
)
print(f"order dx dz dy: {mp.nstr(first_order, 16)}")

second_order = mp.quad(
    lambda y_value: mp.quad(
        lambda x_value: mp.quad(lambda z_value: 1, [0, mp.sqrt(1 - y_value**2)]),
        [y_value, 1],
    ),
    [0, 1],
)
print(f"order dz dx dy: {mp.nstr(second_order, 16)}")

quarter_disk = mp.quad(lambda y_value: mp.sqrt(1 - y_value**2), [0, 1])
y_term = mp.quad(lambda y_value: y_value * mp.sqrt(1 - y_value**2), [0, 1])
print(f"integral of sqrt(1 - y^2): {mp.nstr(quarter_disk, 16)}")
print(f"integral of y*sqrt(1 - y^2): {mp.nstr(y_term, 16)}")

print(f"exact value pi/4 - 1/3: {mp.nstr(exact_value, 16)}")
print(f"first difference:  {mp.nstr(first_order - exact_value, 3)}")
print(f"second difference: {mp.nstr(second_order - exact_value, 3)}")
