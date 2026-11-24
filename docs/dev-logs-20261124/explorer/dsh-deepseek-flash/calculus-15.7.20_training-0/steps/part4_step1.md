# Step 4.1 Check the volume with horizontal slices

## Reason

An answer is credible only when a second method gives the same value.
Slice the solid by horizontal planes instead of vertical lines.
Each slice is an annulus, because the solid is a region between two surfaces of the height $y$.
The sum of the slice volumes is a single integral in the variable $y$, so a different formula must give the
same number.

## Computation

At the height $y$, the upper surface has the squared radius $8-y$, and the lower surface has the squared
radius $y$.
The slice is an annulus with the area

$$
A(y)=\pi\left(8-y\right)-\pi y=\pi\left(8-2y\right).
$$

The height runs from $0$ to $4$, so

$$
V=\int_{0}^{4}\pi\left(8-2y\right) dy
=\pi\left[8y-y^{2}\right]_{0}^{4}
=\pi\left(32-16\right)=16\pi .
$$

## Result

The washer method gives $16\pi$, which agrees with the triple integral.
The largest slice area is $A(0)=8\pi$ at the bottom of the solid, and the smallest slice area is
$A(4)=0$ at the meeting circle.

## Check

`code/part4_verify.py` integrates the slice area with `scipy.integrate.quad` and prints
`volume from the washer method: computed = 50.265482457437, expected = 50.265482457437`.
It also prints `largest cross section area: computed = 25.132741228718` for $8\pi$ and
`smallest cross section area: computed = 0.000000000000` for the area at the meeting circle,
and it asserts that no slice area is negative.
