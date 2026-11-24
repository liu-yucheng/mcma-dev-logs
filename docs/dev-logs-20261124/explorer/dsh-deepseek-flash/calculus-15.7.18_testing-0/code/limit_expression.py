"""Hold the small limit expressions that Part 2 evaluates and prints.

One object produces both the number and the LaTeX source, so a printed limit cannot differ
from the limit that the script evaluates.
"""

from __future__ import annotations

import numpy as np


class ConstantLimit:
    """A bound that is one number."""

    variables: tuple[str, ...] = ()

    def __init__(self, value: float) -> None:
        """Store the number of the bound."""
        self.value = value

    @property
    def latex(self) -> str:
        """Return the LaTeX source of the number."""
        return f"{self.value:g}"

    def evaluate(self, values: dict[str, np.ndarray]) -> np.ndarray:
        """Return the number as an array of the shape of the sample.

        Args:
            values: Arrays of the coordinates of the sample.
        """
        shape = next(iter(values.values())).shape
        return np.full(shape, self.value)


class SqrtRemainder:
    """The bound sqrt(radicand minus the square of one coordinate)."""

    def __init__(self, radicand: float, variable: str) -> None:
        """Store the radicand and the coordinate under the square root."""
        self.radicand = radicand
        self.variable = variable
        self.variables = (variable,)

    @property
    def latex(self) -> str:
        """Return the LaTeX source of the square root."""
        return f"\\sqrt{{{self.radicand:g} - {self.variable}^{{2}}}}"

    def evaluate(self, values: dict[str, np.ndarray]) -> np.ndarray:
        """Return the square root at each sample point.

        Args:
            values: Arrays of the coordinates of the sample.
        """
        return np.sqrt(np.maximum(self.radicand - values[self.variable] ** 2, 0.0))


class LinearShare:
    """The bound of one coordinate divided by a divisor."""

    def __init__(self, variable: str, divisor: float) -> None:
        """Store the coordinate and the divisor."""
        self.variable = variable
        self.divisor = divisor
        self.variables = (variable,)

    @property
    def latex(self) -> str:
        """Return the LaTeX source of the quotient."""
        return f"\\dfrac{{{self.variable}}}{{{self.divisor:g}}}"

    def evaluate(self, values: dict[str, np.ndarray]) -> np.ndarray:
        """Return the quotient at each sample point.

        Args:
            values: Arrays of the coordinates of the sample.
        """
        return values[self.variable] / self.divisor


class LinearMultiple:
    """The bound of a factor times one coordinate."""

    def __init__(self, factor: float, variable: str) -> None:
        """Store the factor and the coordinate."""
        self.factor = factor
        self.variable = variable
        self.variables = (variable,)

    @property
    def latex(self) -> str:
        """Return the LaTeX source of the product."""
        return f"{self.factor:g}{self.variable}"

    def evaluate(self, values: dict[str, np.ndarray]) -> np.ndarray:
        """Return the product at each sample point.

        Args:
            values: Arrays of the coordinates of the sample.
        """
        return self.factor * values[self.variable]


class ScaledLimit:
    """The bound of a factor times another limit expression."""

    def __init__(self, factor: float, expression: SqrtRemainder) -> None:
        """Store the factor and the inner expression."""
        self.factor = factor
        self.expression = expression
        self.variables = expression.variables

    @property
    def latex(self) -> str:
        """Return the LaTeX source of the scaled expression."""
        return f"{self.factor:g}\\,{self.expression.latex}"

    def evaluate(self, values: dict[str, np.ndarray]) -> np.ndarray:
        """Return the scaled value at each sample point.

        Args:
            values: Arrays of the coordinates of the sample.
        """
        return self.factor * self.expression.evaluate(values)


class QuotientLimit:
    """The bound of another limit expression divided by a divisor."""

    def __init__(self, expression: SqrtRemainder, divisor: float) -> None:
        """Store the inner expression and the divisor."""
        self.expression = expression
        self.divisor = divisor
        self.variables = expression.variables

    @property
    def latex(self) -> str:
        """Return the LaTeX source of the quotient."""
        return f"\\dfrac{{{self.expression.latex}}}{{{self.divisor:g}}}"

    def evaluate(self, values: dict[str, np.ndarray]) -> np.ndarray:
        """Return the quotient at each sample point.

        Args:
            values: Arrays of the coordinates of the sample.
        """
        return self.expression.evaluate(values) / self.divisor
