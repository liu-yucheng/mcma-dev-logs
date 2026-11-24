# Part 2, Step 2: Derive the three pairs of limits

## Reason

Fix the pair $(r,\theta)$. The vertical line through the point $(r\cos\theta, r\sin\theta, 0)$ meets
the solid exactly where both inequalities of the statement hold. The first inequality gives
$z \ge r$ and the second gives $z \le h$, so the line enters the body at the wall $z = r$ and leaves
it at the base $z = h$. This interval is empty unless $r \le h$, and $r$ is a distance, so
$0 \le r \le h$. The angle covers one full turn, $0 \le \theta \le 2\pi$.

## Computation

The three pairs of limits follow from the two inequalities without a guess. In the order
$dz\,dr\,d\theta$ they are

$$I_{z} = \int_{\theta = 0}^{2\pi} \int_{r = 0}^{h} \int_{z = r}^{h} k\,r^{3}\,dz\,dr\,d\theta .$$

The inner integral is taken over $z$ from $r$ to $h$ at fixed $r$ and fixed $\theta$. Its lower limit
is the variable $r$ of the middle integral and its upper limit is the constant $h$. The middle
integral is taken
over $r$ from $0$ to $h$ at fixed $\theta$. The outer integral is taken over $\theta$ from $0$ to
$2\pi$.

## Result

The bounds are $r \le z \le h$, then $0 \le r \le h$, then $0 \le \theta \le 2\pi$, in that order.
The inner integral carries the length $h - r$ of the vertical chord, and the order $dz$ first is the
order that computes this length before any other integration. Figure 2 shows the triangle of the
pairs $(r,z)$ and the two segments whose lengths the first two integrations use.

![Figure 2: The cross section of the solid in the $rz$ half plane. The shaded triangle holds the pairs $(r,z)$ of the solid. The vertical segment at $r = r_{0}$ runs from $z = r_{0}$ to $z = h$ and shows the inner limits. The dashed segment at $z = z_{0}$ runs from $r = 0$ to $r = z_{0}$ and shows the radius of one slice.](figures/part2_figure1.png)

Verification: `code/part2_verify.py` integrates the volume element $r\,dz\,dr\,d\theta$ over these
three pairs of limits by adaptive quadrature and gets 1.047197551 at $h = 1$. A second method in the
same script stacks the disks of radius $z$ from $z = 0$ to $z = h$ and gets 1.047197551, and the
formula $\pi h^{3}/3$ gives 1.047197551. `code/part2_figure1.py` prints the limits of the two drawn
segments: the vertical segment runs from $z = 0.4500$ to $z = 1.0000$ at $r = 0.4500$, and the
horizontal segment runs from $r = 0.0000$ to $r = 0.7200$ at $z = 0.7200$.

> **Part 2 answer.** In the order $dz\,dr\,d\theta$ the limits are $r \le z \le h$, $0 \le r \le h$,
> and $0 \le \theta \le 2\pi$, so
> $I_{z} = \int_{0}^{2\pi}\int_{0}^{h}\int_{r}^{h} k\,r^{3}\,dz\,dr\,d\theta$.
