# Part 5, Step 1: The height of the centroid

## Reason

The centroid is the point where the body balances, and its height is the first moment of volume
divided by the volume. The same sections that gave the volume give the moment, because a slab at
the height $z$ carries the moment $z\,A(z)\,dz$. A reader who averages the heights of the two
pieces ignores the volume of each piece, and the two volumes are very different.

## Computation

The volume is $V=108\pi$ from Step 2.3. The first moment about the plane $z=0$ is
$M=\int z\,A(z)\,dz$, taken over the two branches. On the lower branch $A(z)=9\pi$ and the
limits are $0\le z\le 10$:

$$\int_{0}^{10}9\pi z\,dz=9\pi\cdot\frac{100}{2}=450\pi .$$

On the upper branch, substitute $u=z-10$, so that $z=u+10$, $dz=du$, and $0\le u\le 3$:

$$\int_{0}^{3}\pi(u+10)(9-u^{2})\,du
=\pi\int_{0}^{3}\bigl(90+9u-10u^{2}-u^{3}\bigr)du .$$

The four terms integrate to $\frac{81}{2}$, $270$, $-\frac{81}{4}$, and $-90$ at the upper limit.
The sum is $\frac{162+1080-81-360}{4}=\frac{801}{4}$, so the cap contributes
$\frac{801\pi}{4}=180\pi+\frac{81\pi}{4}$.

## Result

$$M=450\pi+\frac{801\pi}{4}=\frac{2601\pi}{4}=2042.820623 .$$

The lower branch gives $450\pi=1413.71669412$ and the upper branch gives
$180\pi+\frac{81\pi}{4}=629.103928881$. The centroid height is

$$\bar z=\frac{M}{V}=\frac{2601\pi/4}{108\pi}=\frac{2601}{432}=\frac{289}{48}=6.02083333333 .$$

The centroid lies inside the cylinder, above its own half height $5$, because the cap adds mass
at the top; it lies below the rim $z=10$.

## Common mistake

A reader may average the heights $5$ and $11.5$ of the two pieces, but the moment weights each
piece by its volume; the volume-weighted height is $\frac{289}{48}$, as the check prints.

## Verification

Verification script: `code/part5_verify.py` check C1 integrates $z\cdot 9\pi$ over the lower branch and prints
$1413.71669412$ against $450\pi$. Check C2 integrates $z\,A(z)$ over $10\le z\le 13$ and prints
$629.103928881$ against $180\pi+\frac{81\pi}{4}$. Check C3 adds the two moments and prints
$2042.820623$ against $\frac{2601\pi}{4}$. Check C4 divides the moment by the volume and prints
$6.02083333333$ against $\frac{289}{48}$. Check C5 estimates the centroid height by random
sampling of the body and prints $6.02435581433$ with a standard error of $0.002054$, so the
difference $3.522\times 10^{-3}$ is inside two standard errors. Checks C6 and C7 print the mean
$x$ and the mean $y$ of the same sample as $-0.00137086207496$ and $0.000843094044807$, each
inside three standard errors of $0$, as the symmetry requires.
