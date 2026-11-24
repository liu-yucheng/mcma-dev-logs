"""The solid E is the cylinder -2 <= x <= 2 with y**2 + z**2 <= 9, and its volume is 36*pi."""
import math
import random
import sympy as sp

y, z = sp.symbols("y z", real=True)
V_disk = sp.integrate(1, (z, -sp.sqrt(9 - y**2), sp.sqrt(9 - y**2)), (y, -3, 3))
V_exact = 4 * V_disk
print("V exact =", V_exact, "=", round(float(V_exact), 4))
for xv in (-2.0, 0.0, 2.0):
    pts = [(xv, 3.0*math.cos(k*math.pi/4), 3.0*math.sin(k*math.pi/4)) for k in range(8)]
    print("x =", xv, "boundary:", [(round(a, 3), round(b, 3), round(c, 3)) for a, b, c in pts])
for xv in (-2.0, 2.0):
    print("corners at x =", xv, ":", [(3.0, 0.0), (0.0, 3.0), (-3.0, 0.0), (0.0, -3.0)])
random.seed(20261124)
N = 200000
hits = 0
for _ in range(N):
    py, pz = random.uniform(-3.0, 3.0), random.uniform(-3.0, 3.0)
    if py*py + pz*pz <= 9.0:
        hits += 1
V_mc = 144.0 * hits / N
print("V Monte Carlo =", round(V_mc, 4), "from", hits, "hits of", N)
assert abs(V_mc - float(V_exact)) < 0.5
print("PASS 1.1")
