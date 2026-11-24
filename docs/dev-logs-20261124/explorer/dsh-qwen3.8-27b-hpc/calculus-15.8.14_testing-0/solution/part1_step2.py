"""The horizontal slice at height z is a disk of radius min(sqrt(z), sqrt(5-z)), so A(1)=pi, A(5/2)=5pi/2, A(4)=pi."""
import numpy as np
from fractions import Fraction

z = Fraction(1, 1)
Rf = float(min(z, Fraction(5, 1) - z))**0.5
rng = np.random.default_rng(7)
for zf in (Fraction(1, 1), Fraction(5, 2), Fraction(4, 1)):
    R = float(min(zf, Fraction(5, 1) - zf))**0.5
    Aex = float(np.pi*min(zf, Fraction(5, 1) - zf))
    N = 8_000_000
    s = 2.0*R
    xs = rng.uniform(-s, s, N)
    ys = rng.uniform(-s, s, N)
    Anum = 4.0*s*s*float(np.mean(xs**2 + ys**2 <= R*R))
    print("z =", float(zf), " R =", round(R, 4), " A_exact =", round(Aex, 4), " A_mc =", round(Anum, 4))
    print("corners:", [(-round(R, 4), 0.0), (round(R, 4), 0.0), (0.0, -round(R, 4)), (0.0, round(R, 4))])
    assert abs(Anum - Aex) <= 8e-3, "slice area mismatch"
print("PASS 1.2")
