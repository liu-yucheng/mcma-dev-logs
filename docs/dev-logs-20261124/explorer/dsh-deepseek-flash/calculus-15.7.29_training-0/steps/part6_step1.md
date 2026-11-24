# Part 6, Step 6.1: The table of the six forms

Part goal: Collect the six forms, then check that all six agree for five test functions with an exact value.

## Reason

A table lets the reader compare the six orders. The innermost integral always reads the chain; the outer two integrals read the projection or the height range.

## Computation

The six forms, with the innermost integral first in each label:

$$\begin{aligned}dy\,dz\,dx &: \int_{-2}^{2} \int_{-\frac{1}{2}\sqrt{4 - x^{2}}}^{\frac{1}{2}\sqrt{4 - x^{2}}} \int_{0}^{4 - x^{2} - 4z^{2}} f\, dy\, dz\, dx,\\dy\,dx\,dz &: \int_{-1}^{1} \int_{-2\sqrt{1 - z^{2}}}^{2\sqrt{1 - z^{2}}} \int_{0}^{4 - x^{2} - 4z^{2}} f\, dy\, dx\, dz,\\dz\,dy\,dx &: \int_{-2}^{2} \int_{0}^{4 - x^{2}} \int_{-\frac{1}{2}\sqrt{4 - x^{2} - y}}^{\frac{1}{2}\sqrt{4 - x^{2} - y}} f\, dz\, dy\, dx,\\dz\,dx\,dy &: \int_{0}^{4} \int_{-\sqrt{4 - y}}^{\sqrt{4 - y}} \int_{-\frac{1}{2}\sqrt{4 - y - x^{2}}}^{\frac{1}{2}\sqrt{4 - y - x^{2}}} f\, dz\, dx\, dy,\\dx\,dz\,dy &: \int_{0}^{4} \int_{-\frac{1}{2}\sqrt{4 - y}}^{\frac{1}{2}\sqrt{4 - y}} \int_{-\sqrt{4 - y - 4z^{2}}}^{\sqrt{4 - y - 4z^{2}}} f\, dx\, dz\, dy,\\dx\,dy\,dz &: \int_{-1}^{1} \int_{0}^{4 - 4z^{2}} \int_{-\sqrt{4 - 4z^{2} - y}}^{\sqrt{4 - 4z^{2} - y}} f\, dx\, dy\, dz.\end{aligned}$$

## Result

Six forms, one for each order of the three differentials. No form uses a split, because every outer region is one piece.

## Verification

`code/part6_verify.py` evaluates all six forms for five test functions. `code/figures/part6_figure1.png` prints the same six limit sets as a picture, and every string of that picture is copied from the docstring of the matching function.
