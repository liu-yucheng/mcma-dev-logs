"""Check the six orders of Exercise 15.7.31 with nested quadrature.

The script integrates every order a second time with nested mpmath quadrature
at 20 decimal digits. It compares the twelve numerical values with the exact
values from part1_step2.py and prints the largest deviation.
"""

from mpmath import mp, mpf, quad

mp.dps = 20

EXACT_ONE = mpf(128) / mpf(15)
EXACT_YZ = mpf(65536) / mpf(9009)


def constant(px, py, pz):
    """Return the integrand 1."""
    return mpf(1)


def y_squared_z_squared(px, py, pz):
    """Return the test integrand y**2 * z**2."""
    return py**2 * pz**2


def order_dz_dy_dx(f):
    """Integrate z first, then y, then x."""
    def over_z(px, py):
        return quad(lambda pz: f(px, py, pz), [mpf(0), 2 - py / 2])

    def over_y(px):
        return quad(lambda py: over_z(px, py), [px**2, mpf(4)])

    return quad(over_y, [mpf(-2), mpf(2)])


def order_dz_dx_dy(f):
    """Integrate z first, then x, then y."""
    def over_z(py, px):
        return quad(lambda pz: f(px, py, pz), [mpf(0), 2 - py / 2])

    def over_x(py):
        return quad(lambda px: over_z(py, px), [-mp.sqrt(py), mp.sqrt(py)])

    return quad(over_x, [mpf(0), mpf(4)])


def order_dy_dz_dx(f):
    """Integrate y first, then z, then x."""
    def over_y(px, pz):
        return quad(lambda py: f(px, py, pz), [px**2, 4 - 2 * pz])

    def over_z(px):
        return quad(lambda pz: over_y(px, pz), [mpf(0), 2 - px**2 / 2])

    return quad(over_z, [mpf(-2), mpf(2)])


def order_dy_dx_dz(f):
    """Integrate y first, then x, then z."""
    def over_y(pz, px):
        return quad(lambda py: f(px, py, pz), [px**2, 4 - 2 * pz])

    def over_x(pz):
        reach = mp.sqrt(4 - 2 * pz)
        return quad(lambda px: over_y(pz, px), [-reach, reach])

    return quad(over_x, [mpf(0), mpf(2)])


def order_dx_dy_dz(f):
    """Integrate x first, then y, then z."""
    def over_x(pz, py):
        return quad(lambda px: f(px, py, pz), [-mp.sqrt(py), mp.sqrt(py)])

    def over_y(pz):
        return quad(lambda py: over_x(pz, py), [mpf(0), 4 - 2 * pz])

    return quad(over_y, [mpf(0), mpf(2)])


def order_dx_dz_dy(f):
    """Integrate x first, then z, then y."""
    def over_x(py, pz):
        return quad(lambda px: f(px, py, pz), [-mp.sqrt(py), mp.sqrt(py)])

    def over_z(py):
        return quad(lambda pz: over_x(py, pz), [mpf(0), 2 - py / 2])

    return quad(over_z, [mpf(0), mpf(4)])


def main():
    """Print every numerical value and the largest deviation."""
    checks = [
        ("dz dy dx", order_dz_dy_dx),
        ("dz dx dy", order_dz_dx_dy),
        ("dy dz dx", order_dy_dz_dx),
        ("dy dx dz", order_dy_dx_dz),
        ("dx dy dz", order_dx_dy_dz),
        ("dx dz dy", order_dx_dz_dy),
    ]
    print(f"exact volume     {mp.nstr(EXACT_ONE, 16)}")
    print(f"exact y^2 z^2    {mp.nstr(EXACT_YZ, 16)}")
    worst = mpf(0)
    for label, method in checks:
        value_one = method(constant)
        value_yz = method(y_squared_z_squared)
        gap_one = abs(value_one - EXACT_ONE)
        gap_yz = abs(value_yz - EXACT_YZ)
        worst = max(worst, gap_one, gap_yz)
        print(f"  {label}  f=1 {mp.nstr(value_one, 16)}  "
              f"dev {mp.nstr(gap_one, 3)}  f=y^2 z^2 {mp.nstr(value_yz, 16)}  "
              f"dev {mp.nstr(gap_yz, 3)}")
    print(f"largest deviation {mp.nstr(worst, 6)}")
    assert worst < mpf("1e-12")
    print("all twelve values agree with the exact values")


if __name__ == "__main__":
    main()
