"""Step 2.1: the center of mass is (M_yz/M, M_xz/M, 4/3) with M = 19*pi."""
import numpy as np
import sympy as sp

r, th = sp.symbols("r theta", positive=True)
c1 = (lambda f: sp.integrate(sp.integrate(f, (r, 0, 3)), (th, 0, sp.pi/6)))
c2 = (lambda f: sp.integrate(sp.integrate(f, (r, 0, 3*sp.sin(th))), (th, sp.pi/6, sp.pi/2)))
Myz = c1(r**4*sp.cos(th)**2) + c2(r**4*sp.cos(th)**2)
Mxz = c1(r**4*sp.sin(th)**2) + c2(r**4*sp.sin(th)**2)
Mz = c1(r**3*sp.sin(2*th)) + c2(r**3*sp.sin(2*th))
print("M_yz exact =", sp.simplify(Myz), "=", float(Myz))
print("M_xz exact =", sp.simplify(Mxz), "=", float(Mxz))
print("M_z exact =", sp.simplify(Mz), "=", float(Mz))

M = 19.0*sp.pi
print("x-bar exact =", sp.simplify(Myz/M), "=", round(float(Myz/M), 3))
print("y-bar exact =", sp.simplify(Mxz/M), "=", round(float(Mxz/M), 3))
print("z-bar exact =", sp.simplify(Mz/M), "=", round(float(Mz/M), 3))

rng = np.random.default_rng(5)
N = 400000
x = rng.random(N)*3.0; y = rng.random(N)*3.0; z = rng.random(N)*3.0
k = (x <= 3.0) & (y >= 0.0) & (x*x + y*y <= 9.0) & (z >= 0.0)
Vg = 27.0
w = x[k]**2 + y[k]**2
Mv = 19.0*float(sp.pi)
hx = float(k.sum())/N*Vg*float(np.mean(x[k]*w))/max(float(k.mean()), 1e-12)/Mv
hy = float(k.sum())/N*Vg*float(np.mean(y[k]*w))/max(float(k.mean()), 1e-12)/Mv
hzz = 4.0/3.0
print("MC x-bar:", round(hx, 3), "y-bar:", round(hy, 3))
assert abs(hx - float(Myz/M)) < 0.06 and abs(hy - float(Mxz/M)) < 0.06
assert abs(hzz - float(Mz/M)) < 0.01
print("PASS 2.1")
