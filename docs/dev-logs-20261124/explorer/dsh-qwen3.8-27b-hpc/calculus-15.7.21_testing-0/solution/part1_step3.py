"""Print the volume V = 8/15 and verify it by three methods."""
import numpy as np
import sympy as sp
y = sp.symbols("y", positive=True)
inner = sp.integrate(1, (sp.Symbol("z"), 0, 1 - y))
V = sp.integrate(sp.integrate(inner, (sp.Symbol("x"), -sp.sqrt(y), sp.sqrt(y))), (y, 0, 1))
print("exact V =", V, "=", float(V))
Vx = sp.integrate(sp.integrate(1 - sp.Symbol("y2"), (sp.Symbol("y2"), sp.Symbol("x2") ** 2, 1)), (sp.Symbol("x2"), -1, 1))
print("fubini V =", Vx)
n = 20_000
ys = np.linspace(0, 1, n + 1)
f = 2 * (1 - ys) * np.sqrt(ys)
V_trap = float(np.trapz(f, ys))
print("numeric V =", V_trap)
rng = np.random.default_rng(21)
xs = rng.uniform(-1, 1, 600_000)
ysm = rng.uniform(0, 1, 600_000)
zs = rng.uniform(0, 1, 600_000)
hit = np.mean((xs ** 2 <= ysm) & (zs <= 1 - ysm))
V_mc = float(hit) * 2
print("monte carlo V =", V_mc)
assert V == sp.Rational(8, 15), V
assert Vx == V, (Vx, V)
assert abs(V_trap - float(V)) < 50 / n, (V_trap, float(V))
assert abs(V_mc - float(V)) < 0.03, (V_mc, float(V))
print("PASS 1.3")
