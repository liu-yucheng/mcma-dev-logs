import sympy as sp
import mpmath as mp

mp.mp.dps = 15
x, y, z = sp.symbols('x y z', real=True)

# E: 0 <= y <= 4 - x^2 - 4z^2,  x^2 + 4z^2 <= 4
#
# EXACT check, order 1 (dy dz dx): polynomial inner integrals.
I1 = sp.integrate(sp.integrate(sp.integrate(1, (y, 0, 4 - x**2 - 4*z**2)),
                               (z, -sp.sqrt(4 - x**2)/2, sp.sqrt(4 - x**2)/2)),
                              (x, -2, 2))
print("exact order dy dz dx ->", sp.simplify(I1))

# EXACT check, order 2 (dy dx dz): also polynomial.
I2 = sp.integrate(sp.integrate(sp.integrate(1, (y, 0, 4 - x**2 - 4*z**2)),
                               (x, -sp.sqrt(4 - 4*z**2), sp.sqrt(4 - 4*z**2))),
                              (z, -1, 1))
print("exact order dy dx dz ->", sp.simplify(I2))

# NUMERIC check (mpmath quad) for all six orders.  The six iterated
# integrals of f = 1 over E must each equal the volume of E.
V1 = mp.quad(lambda X: mp.quad(lambda Z: mp.quad(lambda Y: 1,
        [0, 4 - X**2 - 4*Z**2]),
        [-mp.sqrt(4 - X**2)/2, mp.sqrt(4 - X**2)/2]), [-2, 2])           # dy dz dx
V2 = mp.quad(lambda Z: mp.quad(lambda X: mp.quad(lambda Y: 1,
        [0, 4 - X**2 - 4*Z**2]),
        [-mp.sqrt(4 - 4*Z**2), mp.sqrt(4 - 4*Z**2)]), [-1, 1])           # dy dx dz
V3 = mp.quad(lambda X: mp.quad(lambda Y: mp.quad(lambda Z: 1,
        [-mp.sqrt(4 - X**2 - Y)/2, mp.sqrt(4 - X**2 - Y)/2]),
        [0, 4 - X**2]), [-2, 2])                                         # dz dy dx
V4 = mp.quad(lambda Y: mp.quad(lambda X: mp.quad(lambda Z: 1,
        [-mp.sqrt(4 - Y - X**2)/2, mp.sqrt(4 - Y - X**2)/2]),
        [-2*mp.sqrt(1 - Y/4), 2*mp.sqrt(1 - Y/4)]), [0, 4])              # dz dx dy
V5 = mp.quad(lambda Y: mp.quad(lambda Z: mp.quad(lambda X: 1,
        [-mp.sqrt(4 - Y - 4*Z**2), mp.sqrt(4 - Y - 4*Z**2)]),
        [-mp.sqrt(4 - Y)/2, mp.sqrt(4 - Y)/2]), [0, 4])                  # dx dz dy
V6 = mp.quad(lambda Z: mp.quad(lambda Y: mp.quad(lambda X: 1,
        [-mp.sqrt(4 - 4*Z**2 - Y), mp.sqrt(4 - 4*Z**2 - Y)]),
        [0, 4 - 4*Z**2]), [-1, 1])                                       # dx dy dz

expected = mp.mpf(4) * mp.pi
for name, v in [("dy dz dx", V1), ("dy dx dz", V2), ("dz dy dx", V3),
                ("dz dx dy", V4), ("dx dz dy", V5), ("dx dy dz", V6)]:
    print(name, "->", mp.nstr(v, 12))
    assert mp.almosteq(v, expected, rel_eps=1e-10), name

print("OK: all six orders equal the volume 4*pi =", mp.nstr(expected, 12))
assert sp.simplify(I1 - 4*sp.pi) == 0 and sp.simplify(I2 - 4*sp.pi) == 0
