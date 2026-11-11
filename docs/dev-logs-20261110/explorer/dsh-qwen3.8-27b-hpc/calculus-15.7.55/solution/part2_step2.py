"""Part (b) of problem 15.7.55: exact maximum value of
int_E (1 - x^2 - 2 y^2 - 3 z^2) dV with E = {x^2 + 2 y^2 + 3 z^2 <= 1}.

Method A: the scaling (x, y, z) = (u, v/sqrt(2), w/sqrt(3)) (Jacobian
1/sqrt(6)) maps E onto the unit ball B, and
1 - x^2 - 2 y^2 - 3 z^2 becomes 1 - rho^2. Integrate (1 - rho^2)
over B in spherical coordinates.

Method B (independent, no spherical coordinates): slice E by the plane
z = z0. The cross section is the ellipse x^2/a^2 + y^2/b^2 <= 1 with
a^2 = b^2*2 = 1 - 3 z0^2. For an ellipse with semiaxes (a, b),
  int_Ell x^2 dA = pi a^3 b / 4,   int_Ell y^2 dA = pi a b^3 / 4,
  int_Ell 1  dA = pi a b,
whereas on the unit disk each of the three integrals (1, u^2, v^2)
equals pi/4, pi/4, pi/4. The scaling law for a^2 and b^2 is verified
directly by integrating over the actual ellipse in sympy, then the
slice integral in z0 is a polynomial, and its integral over
z0 in [-1/sqrt(3), 1/sqrt(3)] is exact. Monte-Carlo confirms.
"""
import numpy as np
import sympy as sp

# --- verify the ellipse moment formulas by direct integration on the
#     actual ellipse x^2/a^2 + y^2/b^2 <= 1 with free a, b ---
a, b = sp.symbols("a b", positive=True)
u = sp.symbols("u", real=True)
ymax = b * sp.sqrt(1 - u**2 / a**2)
A1 = sp.integrate(sp.integrate(1, (sp.Symbol("v"), -ymax, ymax)), (u, -a, a))
A2 = sp.integrate(sp.integrate(u**2, (sp.Symbol("v"), -ymax, ymax)), (u, -a, a))
A3 = sp.integrate(sp.integrate(sp.Symbol("v")**2, (sp.Symbol("v"), -ymax, ymax)), (u, -a, a))
print("ellipse int 1  dA =", sp.simplify(A1))
print("ellipse int x^2 dA =", sp.simplify(A2))
print("ellipse int y^2 dA =", sp.simplify(A3))
assert sp.simplify(A1 - sp.pi * a * b) == 0
assert sp.simplify(A2 - sp.pi * a**3 * b / 4) == 0
assert sp.simplify(A3 - sp.pi * a * b**3 / 4) == 0

# --- Method A: unit ball, spherical ---
rho, phi, theta = sp.symbols("rho phi theta", nonnegative=True)
J = 1 / sp.sqrt(6)
I_A = sp.integrate(sp.integrate(sp.integrate(
    (1 - rho**2) * J * rho**2 * sp.sin(phi), (rho, 0, 1)),
    (phi, 0, sp.pi)), (theta, 0, 2 * sp.pi))
I_A = sp.simplify(I_A)
print("Method A (ball/spherical) exact =", I_A)
print("Method A numeric =", sp.N(I_A, 15))

# --- Method B: z-slices, ellipse moments ---
z0 = sp.symbols("z0", real=True)
a2 = 1 - 3*z0**2               # = a^2 = 2 b^2 on the slice
# a*b = a^2/sqrt(2);  a^3 b = a^4/sqrt(2);  a b^3 = a^4/2
area   = sp.pi * a2 / sp.sqrt(2)
mx     = sp.pi * a2**2 / (4 * sp.sqrt(2))
my     = sp.pi * a2**2 / (8 * sp.sqrt(2))
# g = 1 - x^2 - 2 y^2 - 3 z0^2 on the slice, so the y^2 term carries a factor 2
slice_int = sp.simplify((1 - 3*z0**2) * area - mx - 2*my)
print("slice integral (simplified) =", slice_int)
I_B = sp.integrate(slice_int, (z0, -1/sp.sqrt(3), 1/sp.sqrt(3)))
I_B = sp.simplify(I_B)
print("Method B (z-slices)     exact =", I_B)
print("Method B numeric =", sp.N(I_B, 15))
assert sp.simplify(I_A - I_B) == 0, "methods disagree"

# --- Monte-Carlo: unbiased box estimator E_box[g * 1_E] * Vol(box) ---
rng = np.random.default_rng(7)
N = 12_000_000
A, B, C = 1.0, 1.0/np.sqrt(2), 1.0/np.sqrt(3)
box = (2*A) * (2*B) * (2*C)
X = rng.uniform(-A, A, N); Y = rng.uniform(-B, B, N); Z = rng.uniform(-C, C, N)
f = np.where((X**2 + 2*Y**2 + 3*Z**2) <= 1, 1 - X**2 - 2*Y**2 - 3*Z**2, 0.0)
I_mc = float(f.mean()) * box
sd = float(f.std()) / np.sqrt(N) * box
print(f"Monte Carlo: I = {I_mc:.6f} +- {sd:.2e}   (exact {float(sp.N(I_A, 15)):.6f})")
assert abs(I_mc - float(sp.N(I_A, 15))) < 6 * sd + 1e-6

print("EXACT MAXIMUM =", I_A)
print("rationalized  =", sp.simplify(sp.radsimp(I_A)))
print("numeric       =", sp.N(I_A, 15))
