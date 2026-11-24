# Step 4.1: reach the answer through the second order

## Reason

The second order of Step 2.3 reads the solid in the other direction, so its algebra differs from the algebra of Part 3. A value that agrees with Part 3 checks both computations, because an error in the limits of one order would move its value away from the other one.

A reader may treat this value as a proof that the limits match the solid, but the value only checks the algebra, and the test that the limits match the solid is the membership count of `code/part2_verify.py` with ${{p2_membership_sample_count}}$ sample points.

## Computation

The outermost integral of the order $dz\,dy\,dx$ has the integrand

$${{p4_second_order_outer_latex}}$$

The integral of that quantity over $z$ from zero to three is ${{p4_second_order_answer_latex}}$. The same nested integral in the order ${{p4_second_order_latex}}$ gives the decimal value ${{p4_second_order_decimal}}$.

## Result

The second order gives ${{p4_second_order_answer_latex}} = {{p4_second_order_decimal}}$, and that value equals the answer of Part 3. The exact value comes from fraction arithmetic and not from a floating point sum.

## Verification

`code/part4_verify.py` computes the second order in exact rational arithmetic and compares the result with the answer that `code/part3_verify.py` writes to `code/outputs/part3_values.json`. The script holds no literal expected value.
