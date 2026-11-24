# Step 1.1 Find the height where the two surfaces meet

## Reason

The solid ends where the two surfaces meet. At a meeting point the two surfaces have the same height.
Set the right side of the lower surface equal to the right side of the upper surface.
This equation gives the height of the meeting curve and the radius of that curve.

## Computation

The two heights are equal at a meeting point.

$$
x^{2}+z^{2}=8-x^{2}-z^{2}
$$

Move the two squared terms to the left side.

$$
2\left(x^{2}+z^{2}\right)=8
$$

Divide both sides by 2.

$$
x^{2}+z^{2}=4
$$

Substitute this value into the lower surface.

$$
y=x^{2}+z^{2}=4
$$

## Result

The two surfaces meet on the circle $x^{2}+z^{2}=4$ in the plane $y=4$.
The radius of the circle is $2$. The height of the circle is $4$.
The highest point of the solid is $y=8$ above the origin, and the lowest point is $y=0$ above the origin.

## Check

`code/part1_verify.py` finds the meeting radius as the root of the thickness $8-2r^{2}$.
It prints `meeting radius: computed = 2.0, expected = 2.0, difference = 0.000e+00`.
It also prints `lower surface at radius 2: computed = 4.0` and `upper surface at radius 2: computed = 4.0`,
and it confirms that eight points of the meeting curve satisfy both surface equations.
