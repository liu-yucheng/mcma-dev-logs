"""Data of the two tables of the product page.

`SIX_FORMS` holds one row for each order of the three differentials. `VERIFIED_CHECKS` holds
one row for each comparison that a verification script asserts. The values of
`VERIFIED_CHECKS` are copies of the values that the scripts print, so the page and the scripts
cannot drift apart without a visible difference.
"""

from __future__ import annotations

# One row for each order: the label, then the iterated integral.
SIX_FORMS = (
    (
        r"$dy\,dz\,dx$",
        r"$\int_{-2}^{2} \int_{-\frac{1}{2}\sqrt{4 - x^{2}}}^{\frac{1}{2}\sqrt{4 - x^{2}}}"
        r" \int_{0}^{4 - x^{2} - 4z^{2}} f\, dy\, dz\, dx$",
    ),
    (
        r"$dy\,dx\,dz$",
        r"$\int_{-1}^{1} \int_{-2\sqrt{1 - z^{2}}}^{2\sqrt{1 - z^{2}}}"
        r" \int_{0}^{4 - x^{2} - 4z^{2}} f\, dy\, dx\, dz$",
    ),
    (
        r"$dz\,dy\,dx$",
        r"$\int_{-2}^{2} \int_{0}^{4 - x^{2}} \int_{-\frac{1}{2}\sqrt{4 - x^{2} - y}}"
        r"^{\frac{1}{2}\sqrt{4 - x^{2} - y}} f\, dz\, dy\, dx$",
    ),
    (
        r"$dz\,dx\,dy$",
        r"$\int_{0}^{4} \int_{-\sqrt{4 - y}}^{\sqrt{4 - y}} \int_{-\frac{1}{2}\sqrt{4 - y - x^{2}}}"
        r"^{\frac{1}{2}\sqrt{4 - y - x^{2}}} f\, dz\, dx\, dy$",
    ),
    (
        r"$dx\,dz\,dy$",
        r"$\int_{0}^{4} \int_{-\frac{1}{2}\sqrt{4 - y}}^{\frac{1}{2}\sqrt{4 - y}}"
        r" \int_{-\sqrt{4 - y - 4z^{2}}}^{\sqrt{4 - y - 4z^{2}}} f\, dx\, dz\, dy$",
    ),
    (
        r"$dx\,dy\,dz$",
        r"$\int_{-1}^{1} \int_{0}^{4 - 4z^{2}} \int_{-\sqrt{4 - 4z^{2} - y}}"
        r"^{\sqrt{4 - 4z^{2} - y}} f\, dx\, dy\, dz$",
    ),
)

# One row for each verified comparison: the check number, the quantity, the value, the margin.
VERIFIED_CHECKS = (
    ("5.1 (Part 1)", "disagreements of the two membership tests, 200 000 points", "0",
     "51 959 points inside"),
    ("5.2 (Part 1)", "base area, quadrature against the semi-axes", "6.283185307",
     "difference 2.867E-12"),
    ("5.3 (Part 1)", "largest height from a grid against the apex", "4.000000000",
     "difference 0"),
    ("5.4 (Part 2)", "section area at y = 0, three formulas", "6.283185307",
     "largest difference 7.105E-15"),
    ("5.5 (Part 2)", "section area at y = 2, three formulas", "3.141592654",
     "largest difference 3.997E-15"),
    ("5.6 (Part 2)", "distinct corner positions at y = 4", "1", "single point"),
    ("5.7 (Part 3)", "orders dy dz dx and dy dx dz, two test functions", "12.566370614",
     "largest difference 1.315E-13"),
    ("5.8 (Part 4)", "orders dz dy dx and dz dx dy, two test functions", "8.377580410",
     "largest difference 6.573E-13"),
    ("5.9 (Part 5)", "orders dx dz dy and dx dy dz, two test functions", "2.094395102",
     "largest difference 6.573E-13"),
    ("5.10 (Part 6)", "spread over the six orders of f = x squared", "7.105E-14",
     "largest spread 6.590E-13"),
    ("5.11 (Part 6)", "largest difference over 30 pairs of an order and a function",
     "6.573E-13", "exact value from algebra"),
)
