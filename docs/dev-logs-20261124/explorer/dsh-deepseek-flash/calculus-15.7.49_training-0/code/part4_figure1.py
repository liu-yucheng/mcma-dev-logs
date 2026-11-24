"""Draw Figure 2: the eight monomial integrals of the moment of inertia.

Each bar is one monomial integral of `part4_verify.py`. The label of a bar is the exact value of
that same integral, which the script computes again with `sympy`, so no label comes from a
literal. The dashed line marks the sum of the eight values. The script writes
`code/figures/part4_figure1.png` and it asserts that every label lies inside the axes box.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import sympy

import common_region as region

X, Y, Z = sympy.symbols("x y z")
"""Symbols of the Cartesian coordinates."""

RHO = 1 + X + Y + Z
"""The density function of the statement."""

OUTER = sympy.sqrt(1 - X**2)
"""The largest y of E at a fixed x."""

MONOMIALS = (X**2, Y**2, X**3, X**2 * Y, X**2 * Z, Y**3, X * Y**2, Y**2 * Z)
"""The eight monomials of the product (x^2 + y^2) (1 + x + y + z)."""


def exact_integral(monomial: sympy.Expr) -> sympy.Expr:
    """Return the exact integral of one monomial over E."""
    return sympy.simplify(sympy.integrate(monomial, (Z, 0, Y), (Y, 0, OUTER), (X, 0, 1)))


def main() -> None:
    """Draw the bar chart, check each label, and write the figure."""
    values = [exact_integral(monomial) for monomial in MONOMIALS]
    total = sympy.simplify(sum(values))
    labels = [f"${sympy.latex(monomial)}$" for monomial in MONOMIALS]
    exact_text = [f"${sympy.latex(value)}$" for value in values]
    decimals = [float(value) for value in values]

    figure = plt.figure(figsize=(9.2, 4.4))
    axes = figure.add_subplot(1, 1, 1)
    position = range(len(MONOMIALS))
    axes.barh(list(position), decimals, color="#4c78a8", height=0.62)
    axes.set_yticks(list(position))
    axes.set_yticklabels(labels, fontsize=11)
    axes.invert_yaxis()
    axes.set_xlabel("value of the integral")
    axes.set_xlim(0.0, float(total) * 1.45)
    axes.set_title(
        "The eight monomial integrals of $I_z$ and their sum " + f"${sympy.latex(total)}$",
        fontsize=11,
    )
    for index, (decimal_value, text) in enumerate(zip(decimals, exact_text)):
        axes.text(
            decimal_value + max(decimals) * 0.04,
            index,
            f"{text} $={decimal_value:.6f}$",
            va="center",
            fontsize=9,
        )
    axes.axvline(float(total), color="#e45756", linestyle="--", linewidth=1.4)
    axes.text(
        float(total) * 0.96,
        -0.30,
        f"sum $={float(total):.6f}$",
        ha="right",
        va="center",
        fontsize=9,
        color="#e45756",
    )
    axes.grid(axis="x", color="#e6e6e6", linewidth=0.8)
    axes.set_axisbelow(True)
    figure.tight_layout()
    figure.canvas.draw()

    renderer = figure.canvas.get_renderer()
    axes_box = axes.get_window_extent(renderer=renderer)
    for index, text in enumerate(axes.texts):
        box = text.get_window_extent(renderer=renderer)
        inside = box.x0 >= axes_box.x0 and box.x1 <= axes_box.x1 and box.y0 >= axes_box.y0 and box.y1 <= axes_box.y1
        print(f"[place] text {index} {text.get_text()!r} inside the axes box: {inside}")
        if not inside:
            raise AssertionError(f"text {index} leaves the axes box: {box} against {axes_box}")

    region.FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = region.FIGURE_DIRECTORY / "part4_figure1.png"
    figure.savefig(path, dpi=170)
    print(f"[figure] wrote {path}")
    print(f"[check] the eight bars add to ${sympy.latex(total)}$ with decimal {float(total):.6f}")
    plt.close(figure)


if __name__ == "__main__":
    main()
