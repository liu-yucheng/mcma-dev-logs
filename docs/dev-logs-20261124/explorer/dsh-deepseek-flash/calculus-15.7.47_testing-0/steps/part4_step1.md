# Part 4. The center of mass

## Step 4.1. Use the symmetry in $x$

### Reason
The solid and the density are unchanged by the reflection $x \mapsto -x$, and the integrand $x\sqrt{x^{2} + y^{2}}$ changes sign under the same reflection. An integral of a function that changes sign over a region that does not change is zero. A reader may take the center of mass off the plane $x = 0$, but the odd integrand over the symmetric region gives a zero first moment, so the first coordinate of the center is zero.

### Computation
$$M_{yz} = \int_{D} x\sqrt{x^{2} + y^{2}}\,dV = 0.$$

### Result
The first moment is {{p4_moment_x}}, which is zero at the resolution of the quadrature, so $\bar{x} = $ {{p4_xbar}}.
`code/part4_verify.py` prints the moment and the coordinate.
