"""All six iterated orderings evaluate numerically to the exact volume 36*pi of E."""
import math

def trap(g, a, b, n):
    h = (b - a) / n
    return h * (0.5 * g(a) + sum(g(a + k * h) for k in range(1, n)) + 0.5 * g(b))

R = lambda t: math.sqrt(9.0 - t * t)
C = lambda t: 1.0
NX, N = 2, 20000
dz_dy_dx = trap(lambda x: trap(lambda y: trap(C, -R(y), R(y), NX), -3.0, 3.0, N), -2.0, 2.0, NX)
dy_dz_dx = trap(lambda x: trap(lambda z: trap(C, -R(z), R(z), NX), -3.0, 3.0, N), -2.0, 2.0, NX)
dx_dy_dz = trap(lambda z: trap(lambda y: trap(C, -2.0, 2.0, NX), -R(z), R(z), NX), -3.0, 3.0, N)
dx_dz_dy = trap(lambda y: trap(lambda z: trap(C, -2.0, 2.0, NX), -R(y), R(y), NX), -3.0, 3.0, N)
dz_dx_dy = trap(lambda y: trap(lambda x: trap(C, -R(y), R(y), NX), -2.0, 2.0, NX), -3.0, 3.0, N)
dy_dx_dz = trap(lambda z: trap(lambda x: trap(C, -R(z), R(z), NX), -2.0, 2.0, NX), -3.0, 3.0, N)
V_exact = 36.0 * math.pi
vals = [dz_dy_dx, dy_dz_dx, dx_dy_dz, dx_dz_dy, dz_dx_dy, dy_dx_dz]
for name, v in zip(["dz dy dx", "dy dz dx", "dx dy dz", "dx dz dy", "dz dx dy", "dy dx dz"], vals):
    print(name, "=", round(v, 6))
assert all(abs(v - V_exact) < 1e-3 for v in vals)
print("exact =", round(V_exact, 6), "PASS 1.3")
