# Step 2.3: Evaluate the double integral

## Reason

The integral of a difference is the difference of the integrals. The first integral has the constant
integrand $5$ and needs only the area of the disk. The second integral has the integrand $z$, and the
disk is symmetric about the line $z=0$.

## Computation

The area of the disk of radius $2$ is $4\pi$, so

$$\iint_{D}5\,dA=5\cdot 4\pi=20\pi.$$

The disk is symmetric under the map $z\mapsto -z$, and the integrand $z$ changes sign under that map,
so $\iint_{D}z\,dA=0$. Therefore

$$V=20\pi-0=20\pi.$$

A second route integrates in $z$ first. With $a=\sqrt{4-x^2}$,

$$\int_{-a}^{a}(5-z)\,dz=\Big[5z-\frac{z^2}{2}\Big]_{-a}^{a}=10a,\qquad
V=\int_{-2}^{2}10\sqrt{4-x^2}\,dx.$$

The integral of $\sqrt{4-x^2}$ from $-2$ to $2$ is the area of the upper half of the disk of radius $2$,
which is $\frac{1}{2}\pi\cdot 2^2=2\pi$. Thus

$$V=10\cdot 2\pi=20\pi.$$

## Check

The value lies between $12\pi\approx 37.7$ and $28\pi\approx 88.0$, as Step 1.3 requires. Two different
orders give the same value.

## Result

$$V=20\pi\approx 62.831853071796.$$

## Verification

`code/part2_verify.py` prints the double integral $62.831853071796$ and $20\pi=62.831853071796$; the
accepted difference is $10^{-8}$. The script computes the area of the half disk by quadrature as
$6.283185307180$ and by the formula $\pi\cdot 2^2/2$ as $6.283185307180$, against the accepted
difference $10^{-9}$. Ten times the quadrature area is $62.831853071796$, and it agrees with the double
integral to $10^{-8}$.
