# Step 3.2: integrate in $x$ and then in $y$

## Reason

The middle integral holds $y$ fixed and integrates the result of Step 3.1 over $x$ from zero to $y/3$. That integrand does not depend on $x$, so the middle integral is the integrand multiplied by the width of the interval. The outer integral then holds one variable only.

A reader may take $x$ from $0$ to $1$ at every $y$, but at a fixed $y$ the plane gives $x \le y/3$, and that choice gives ${{p3_wrong_value_decimal}}$, which is ${{p3_wrong_ratio_decimal}}$ times the answer, as `code/part3_verify.py` prints.

## Computation

$$\int_{0}^{y/3} {{p3_inner_latex}}\,dx = {{p3_middle_latex}}$$

$$\int_{0}^{3} {{p3_middle_latex}}\,dy = \left[{{p3_antiderivative_latex}}\right]_{0}^{3} = {{p3_answer_latex}} = {{p3_answer_decimal}}$$

## Result

The value of the integral is ${{p3_answer_latex}} = {{p3_answer_decimal}}$. The solid has the volume ${{p1_volume_latex}}$, so the mean height of a point of the solid is ${{p3_mean_height_latex}} = {{p3_mean_height_decimal}}$. Figure 5 shows the outer integrand with its area and the antiderivative with its change from zero to three.

## Verification

`code/part3_verify.py` differentiates the antiderivative by a central difference at many points and compares the derivative with the integrand, with the largest relative gap ${{p3_derivative_gap}}$. It also evaluates the full nested integral by quadrature and compares the result with the closed form.
