"""Check all six orders numerically with mpmath.

The integrands are f = 1 and f = y**2 * z**2. Every limit may depend on the
variables that are still free, so each limit is a function of a point record.
"""

from mpmath import mp

mp.dps = 20

nine = mp.mpf(9)
three = mp.mpf(3)
two = mp.mpf(2)

orders = {
    "dz dy dx": (
        ("z", lambda point: -mp.sqrt(nine - point["y"] ** 2),
         lambda point: mp.sqrt(nine - point["y"] ** 2)),
        ("y", lambda point: -three, lambda point: three),
        ("x", lambda point: -two, lambda point: two),
    ),
    "dz dx dy": (
        ("z", lambda point: -mp.sqrt(nine - point["y"] ** 2),
         lambda point: mp.sqrt(nine - point["y"] ** 2)),
        ("x", lambda point: -two, lambda point: two),
        ("y", lambda point: -three, lambda point: three),
    ),
    "dy dz dx": (
        ("y", lambda point: -mp.sqrt(nine - point["z"] ** 2),
         lambda point: mp.sqrt(nine - point["z"] ** 2)),
        ("z", lambda point: -three, lambda point: three),
        ("x", lambda point: -two, lambda point: two),
    ),
    "dy dx dz": (
        ("y", lambda point: -mp.sqrt(nine - point["z"] ** 2),
         lambda point: mp.sqrt(nine - point["z"] ** 2)),
        ("x", lambda point: -two, lambda point: two),
        ("z", lambda point: -three, lambda point: three),
    ),
    "dx dy dz": (
        ("x", lambda point: -two, lambda point: two),
        ("y", lambda point: -mp.sqrt(nine - point["z"] ** 2),
         lambda point: mp.sqrt(nine - point["z"] ** 2)),
        ("z", lambda point: -three, lambda point: three),
    ),
    "dx dz dy": (
        ("x", lambda point: -two, lambda point: two),
        ("z", lambda point: -mp.sqrt(nine - point["y"] ** 2),
         lambda point: mp.sqrt(nine - point["y"] ** 2)),
        ("y", lambda point: -three, lambda point: three),
    ),
}


def evaluate(order, integrand):
    """Integrate the integrand in the given innermost-to-outermost order."""

    def nest(position, point):
        if position < 0:
            return integrand(point)
        variable, lower, upper = order[position]
        return mp.quad(
            lambda value: nest(position - 1, {**point, variable: value}),
            [lower(point), upper(point)],
        )

    return nest(len(order) - 1, {})


exact_volume = mp.pi * 36
exact_second = mp.pi * mp.mpf(243) / 2
print(f"exact volume 36*pi: {mp.nstr(exact_volume, 15)}")
print(f"exact second value 243*pi/2: {mp.nstr(exact_second, 15)}")

print("numeric values with f = 1")
for name, order in orders.items():
    value = evaluate(order, lambda point: mp.mpf(1))
    print(f"  {name}: {mp.nstr(value, 15)}  deviation {mp.nstr(value - exact_volume, 3)}")
    assert abs(value - exact_volume) < mp.mpf("1e-10")

print("numeric values with f = y^2 * z^2")
for name, order in orders.items():
    value = evaluate(order, lambda point: point["y"] ** 2 * point["z"] ** 2)
    print(f"  {name}: {mp.nstr(value, 15)}  deviation {mp.nstr(value - exact_second, 3)}")
    assert abs(value - exact_second) < mp.mpf("1e-10")

print("all twelve numerical values match the symbolic results")
