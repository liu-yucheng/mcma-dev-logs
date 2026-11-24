# Step 3.2: The area of the slice

## Reason

The area of the full disk is known, and the area of a circular segment is the area of a sector minus
the area of a triangle.

## Computation

For $-1\le c\le 2$, the slice is the disk of radius $2$, so

$$A(c)=\pi\cdot 2^2=4\pi.$$

For $2<c\le 6$, put $k=c-4$. Then $0<k\le 2$, and the line is $z=-k$, at the distance $k$ from the
center. The half angle of the segment is $\arccos(k/2)$, so the sector has the angle $2\arccos(k/2)$ and
the area $2^2\arccos(k/2)$. The triangle that the sector contains has the base $2\sqrt{4-k^2}$ and the
height $k$, so its area is $k\sqrt{4-k^2}$. Thus

$$A(c)=4\arccos\frac{c-4}{2}-(c-4)\sqrt{4-(c-4)^2}.$$

## Check

At $k=0$, that is $c=4$, the segment is the half disk: $A=4\cdot\frac{\pi}{2}=2\pi$.

At $k=2$, that is $c=6$: $A=4\arccos 1-2\cdot 0=0$.

At $k=-1$, that is $c=3$: $A=4\arccos(-\frac{1}{2})-(-1)\sqrt{3}=\frac{8\pi}{3}+\sqrt{3}\approx
10.109631$.

At $k=1$, that is $c=5$: $A=4\arccos\frac{1}{2}-1\cdot\sqrt{3}=\frac{4\pi}{3}-\sqrt{3}\approx
2.456739$.

The two formulas agree at $c=2$, because $\arccos(-1)=\pi$ and $\sqrt{0}=0$ give $4\pi$.

## Result

$$A(c)=\begin{cases}4\pi,&-1\le c\le 2,\\[2pt]
4\arccos\dfrac{c-4}{2}-(c-4)\sqrt{4-(c-4)^2},&2<c\le 6.\end{cases}$$

## Verification

`code/part3_verify.py` prints the closed form and an integration of the slice length at nine heights.
The values at $c=3$ are $10.10963122$ from both methods, and the values at $c=5$ are $2.45673940$ from
both methods. The largest difference of the nine heights is $1.4\times10^{-14}$.
