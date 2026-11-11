"""Evaluate the volume of the pyramid with mpmath in three orders of integration.

Each order of integration gives the same number. The exact value 2/3 supplies the
reference, and the differences are printed to show the size of the round-off.
"""

from mpmath import mp, mpf, quad

mp.dps = 30


def main():
    """Print the three numerical values and their differences from 2/3."""
    order_one = quad(
        lambda x_value: quad(
            lambda z_value: quad(lambda y_value: mpf(1), [0, 2 - 2 * z_value]),
            [0, 1 - x_value],
        ),
        [0, 1],
    )
    order_two = quad(
        lambda z_value: quad(
            lambda x_value: quad(lambda y_value: mpf(1), [0, 2 - 2 * z_value]),
            [0, 1 - z_value],
        ),
        [0, 1],
    )
    order_three = quad(
        lambda z_value: quad(
            lambda y_value: quad(lambda x_value: mpf(1), [0, 1 - z_value]),
            [0, 2 - 2 * z_value],
        ),
        [0, 1],
    )
    exact = mpf(2) / mpf(3)
    print(f"order dy dz dx: {mp.nstr(order_one, 18)}")
    print(f"order dy dx dz: {mp.nstr(order_two, 18)}")
    print(f"order dx dy dz: {mp.nstr(order_three, 18)}")
    print(f"exact value 2/3: {mp.nstr(exact, 18)}")
    print(f"first difference:  {mp.nstr(abs(order_one - exact), 3)}")
    print(f"second difference: {mp.nstr(abs(order_two - exact), 3)}")
    print(f"third difference:  {mp.nstr(abs(order_three - exact), 3)}")


if __name__ == "__main__":
    main()
