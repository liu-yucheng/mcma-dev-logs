# Step 2 — Find the circle where the surfaces meet

## Reason

The region ends where the two surfaces meet. The curve of intersection is also the boundary of the shadow that $E$ casts on the $yz$ plane. The next step needs that shadow.

## Computation

Set the two expressions for $x$ equal:

$$
4\left(y^{2} + z^{2}\right) = 4.
$$

Divide both sides by $4$:

$$
y^{2} + z^{2} = 1.
$$

This is a circle of radius $1$. The circle lies in the plane $x = 4$, because $x = 4$ on the plane.

Two height checks confirm the equation. At $r = 0.5$ the paraboloid has $x = 4 \cdot 0.25 = 1$, which is below the plane. At $r = 1$ the paraboloid has $x = 4$, which is on the plane.

Every point $(y, z)$ with $y^{2} + z^{2} \le 1$ gives a nonempty segment $4r^{2} \le x \le 4$. Every point with $y^{2} + z^{2} > 1$ gives an empty segment, because $4r^{2} > 4$.

## Result

The surfaces meet on the circle $y^{2} + z^{2} = 1$ in the plane $x = 4$.

The projection of $E$ onto the $yz$ plane is the closed unit disk

$$
D = \left\{(y, z) : y^{2} + z^{2} \le 1\right\}.
$$

## Verification

`code/part1_verify.py` compares the membership of $200000$ random points with the rule $r \le 1$. The agreement is $1.000000$. The same script counts the volume of $E$ and reports $6.2755$ against the exact value $6.2832$.
