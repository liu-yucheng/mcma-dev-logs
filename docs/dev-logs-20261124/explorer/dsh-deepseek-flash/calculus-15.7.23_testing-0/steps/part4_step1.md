# Part 4. A second order and a grid rule

## Reason

One number from one order of integration is weak evidence, because a wrong limit still gives a
finite number. Compute the volume again with a different order and with a rule that uses no
limit at all. A value that two independent methods produce is a value that the page can state.

## Computation

Integrate $y$ first. At a fixed pair $(x,z)$ the inequality $y^{2}+z^{2}\le 1$ gives
$y\le\sqrt{1-z^{2}}$ and the inequality $x\le y$ gives $y\ge x$. A point exists only when
$x\le\sqrt{1-z^{2}}$, that is $x^{2}+z^{2}\le 1$. The projection of the solid on the plane $y=0$
is the quarter disk of radius $1$.

$$V=\iint_{x^{2}+z^{2}\le 1,\,x\ge 0,\,z\ge 0}\left(\sqrt{1-z^{2}}-x\right)\,dx\,dz .$$

With $x=r\cos t$ and $z=r\sin t$ the integral is

$$V=\int_{0}^{\pi/2}\int_{0}^{1}\left(\sqrt{1-r^{2}\sin^{2}t}-r\cos t\right)r\,dr\,dt .$$

The second method is a midpoint rule on a grid of {{p4_grid}} cells per axis of the unit cube. A
cell counts when its center satisfies $x\le y$ and $y^{2}+z^{2}\le 1$. The rule uses the
membership test only, and it needs no limit.

## Common mistake

A reader may take the projection on the plane $y=0$ as the square $0\le x\le 1$, $0\le z\le 1$,
but the limits give the quarter disk $x^{2}+z^{2}\le 1$, $x\ge 0$, $z\ge 0$, whose area is
{{p4_disk_area}}.

## Result

The polar rule gives {{p4_polar}}, the midpoint rule gives {{p4_midpoint}}, and the exact value is
{{p4_exact}}. The three values agree to the accuracy that each method supports, so the volume of
the wedge is $1/3$.

Verification: `code/part4_verify.py`.
