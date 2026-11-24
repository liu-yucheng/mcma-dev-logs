## Step 5.2 Check the answer and reject the wrong ones

**Reason.** An answer is acceptable only when it passes three tests. Each coordinate must lie in the range of its
axis, each value must equal the value of an independent route, and each wrong value must differ from the answer.

**Computation.** The checks of `code/part5_verify.py` compare the mass and the three coordinates with the stored
values of Parts 2, 3 and 4, and they compare the answer with the three naive values of Steps 2.3 and 3.3.

**Result.** The mass {{p5_mass}} and the center {{p5_center}} lie inside the solid, and every stored value of Parts
2, 3 and 4 agrees with them. A reader may take the prism mass {{p5_naive_prism_mass}} or the narrow mass
{{p5_naive_narrow_mass}}, but the limits give the mass {{p5_mass}}. A reader may take the first coordinate as
{{p5_naive_center_x}}, but the definition divides by the mass and gives {{p3_xbar}}. Verified by
`code/part5_verify.py`.
