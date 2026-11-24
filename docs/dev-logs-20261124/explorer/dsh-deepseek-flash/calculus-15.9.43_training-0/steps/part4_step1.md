# Part 4, Step 1: The area of each face

## Reason

A drawing shows surfaces, not only the outline, so the areas of the three faces belong to the
solution. Each area is a surface integral, and a surface integral needs a parametrization and the
length of the cross product of its two tangent vectors. That length turns the integral into a
product of factors when the limits are constant.

## Computation

The lateral face has the parametrization
$\mathbf{r}(\theta,z)=(3\cos\theta,3\sin\theta,z)$ with $0\le\theta\le 2\pi$ and
$0\le z\le 10$. Its tangent vectors are $(-3\sin\theta,3\cos\theta,0)$ and $(0,0,1)$, and the
length of their cross product is $3$. Then

$$A_{\text{lateral}}=\int_{0}^{2\pi}\int_{0}^{10}3\,dz\,d\theta=3\cdot 10\cdot 2\pi=60\pi .$$

The cap has the parametrization of Step 3.2 with $\rho=3$ fixed:
$\mathbf{r}(\varphi,\theta)=3\sin\varphi\cos\theta,3\sin\varphi\sin\theta,10+3\cos\varphi$. The
length of the cross product is $9\sin\varphi$. Then

$$A_{\text{cap}}=\int_{0}^{2\pi}\int_{0}^{\pi/2}9\sin\varphi\,d\varphi\,d\theta
=9\cdot 1\cdot 2\pi=18\pi .$$

The lower disk has the polar parametrization $(r\cos\theta,r\sin\theta,0)$ with $0\le r\le 3$,
and the length of the cross product is $r$. Then

$$A_{\text{base}}=\int_{0}^{2\pi}\int_{0}^{3}r\,dr\,d\theta
=\frac{9}{2}\cdot 2\pi=9\pi .$$

## Result

$$A_{\text{lateral}}=60\pi=188.495559215,\quad
A_{\text{cap}}=18\pi=56.5486677646,\quad
A_{\text{base}}=9\pi=28.2743338823 .$$

The drawn area, the sum of the three faces, is $87\pi=273.318560862$.

## Common mistake

A reader may add the disk at $z=10$ as a fourth surface, but that disk is interior; the three
faces give $87\pi$, and the check prints that sum.

## Verification

Verification script: `code/part4_verify.py` check C1 multiplies the three factors of the lateral integral and prints
$188.495559215$ against $2\pi RH$. Check C2 integrates $9\sin\varphi$ numerically over the two
angle limits and prints $56.5486677646$ against $2\pi R^{2}$. Check C3 integrates $r$ and prints
$28.2743338823$ against $\pi R^{2}$. Check C4 adds the three numerical integrals and prints
$273.318560862$ against $87\pi$. Each reference value is a closed form that the script builds
from the radius and the height, so no check compares a printed number with itself.
