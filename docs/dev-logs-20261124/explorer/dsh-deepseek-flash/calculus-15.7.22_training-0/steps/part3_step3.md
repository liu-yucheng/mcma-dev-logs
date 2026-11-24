# Step 3.3: Integrate the area of the slice

## Reason

The volume is the integral of the areas of the slices that are perpendicular to the outer axis. Here
the slices are perpendicular to the $y$ axis, so the outer variable is $y=c$.

## Computation

The height of the solid covers $-1\le c\le 6$, and the formula of $A$ changes at $c=2$:

$$V=\int_{-1}^{2}4\pi\,dc+\int_{2}^{6}A(c)\,dc=12\pi+\int_{2}^{6}A(c)\,dc.$$

With $u=c-4$,

$$\int_{2}^{6}A(c)\,dc=\int_{-2}^{2}\left(4\arccos\frac{u}{2}-u\sqrt{4-u^2}\right)du.$$

The term $u\sqrt{4-u^2}$ is odd, so its integral over the symmetric interval is $0$. With $u=2t$,

$$\int_{-2}^{2}\arccos\frac{u}{2}\,du=2\int_{-1}^{1}\arccos t\,dt
=2\Big[t\arccos t-\sqrt{1-t^2}\Big]_{-1}^{1}=2(\pi-0)=2\pi.$$

Thus the curved part is $4\cdot 2\pi=8\pi$, and

$$V=12\pi+8\pi=20\pi.$$

## Check

The flat part $12\pi$ counts the slices from $c=-1$ to $c=2$, which is a length of $3$ times the area
$4\pi$. The curved part $8\pi$ counts the segments from $c=2$ to $c=6$. The sum agrees with Part 2.

## Result

$$V=20\pi\approx 62.831853071796.$$

## Verification

`code/part3_verify.py` integrates the area with adaptive quadrature from $-1$ to $6$ and prints
$62.831853071796$. It also adds the flat part and the curved part and prints $62.831853071796$. It
prints the closed form $20\pi=62.831853071796$, the flat part $37.699111843078$, and the curved part
$25.132741228718$, equal to $8\pi$. The accepted difference is $10^{-8}$ for each assertion.
