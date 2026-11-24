# Step 1.3: The vertical thickness of the solid

## Reason

The first integration will be in $y$. An inner integral in $y$ needs the length of the interval of $y$
above each point $(x,z)$ of the disk.

## Computation

For a point $(x,z)$ with $x^2+z^2\le 4$, the two plane inequalities allow every $y$ with
$-1\le y\le 4-z$. The interval is not empty exactly when $4-z\ge -1$, that is $z\le 5$. Every point of
the disk has $z\le 2$, so the interval is never empty. Its length is

$$h(x,z)=(4-z)-(-1)=5-z.$$

On the disk, $z$ runs from $-2$ to $2$. Thus $h$ runs from $5-2=3$ at $z=2$ to $5-(-2)=7$ at $z=-2$,
and

$$3\le h\le 7.$$

The smallest thickness is positive, so no vertical line meets the solid in an empty set. The thickness
does not depend on $x$, so every line parallel to the $y$ axis has the same length above two points of
the disk with the same $z$.

## Check

The disk has the area $4\pi$. The volume is therefore between $4\pi\cdot 3=12\pi$ and
$4\pi\cdot 7=28\pi$. This bound will check the answer of Part 2; it is not the answer.

## Result

The thickness is $h=5-z$, and it runs from $3$ to $7$ over the disk.

## Verification

`code/part1_verify.py` measures the thickness two ways. It scans $y$ in steps of $0.001$ at $200$
random points of the disk and takes the length of the scanned interval; the largest difference from
$5-z$ is $0.000999$, against the accepted difference $2\cdot 0.001=0.002000$. The script also takes the
smallest and the largest value of $5-z$ over a grid of the disk; they are $3.000000$ and $7.000000$,
and the values from the two plane equations are $5-2$ and $5+2$.
