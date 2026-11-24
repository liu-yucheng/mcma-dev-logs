# Part 1, Step 1: Read the solid from the two inequalities

## Reason

The symbol $\sqrt{x^{2}+y^{2}}$ is the distance from the point $(x,y,z)$ to the $z$-axis. The
inequality $\sqrt{x^{2}+y^{2}} \le z$ says that the height of a point is at least this distance.
The inequality $z \le h$ says that the height is at most $h$. Together the two inequalities cut one
solid body out of the space.

## Computation

Hold the height at the value $z = c$ with $0 \le c \le h$. At this height the condition
$\sqrt{x^{2}+y^{2}} \le c$ describes the closed disk

$$x^{2}+y^{2} \le c^{2}$$

of radius $c$ in the plane $z = c$. At $c = h$ the disk has radius $h$. At $c = 0$ the disk shrinks
to the single point $(0,0,0)$.

## Result

The solid $E$ is a right circular cone. The apex is the origin, the base is the disk of radius $h$
in the plane $z = h$, and the wall is the cone $z = \sqrt{x^{2}+y^{2}}$. The height is $h$.
Figure 1 shows the body, the axis of rotation, and one horizontal slice.

![Figure 1: The solid cone $\sqrt{x^{2}+y^{2}} \le z \le h$, its base disk at $z = h$, the axis, and one horizontal slice at $z = z_{0}$ of radius $r = z_{0}$.](figures/part1_figure1.png)

Verification: `code/part1_verify.py` describes the same point twice, once by the two inequalities
and once by the inequalities $r \le z \le h$ in cylindrical coordinates. The two descriptions agree
on 2000000 of 2000000 sampled points. The same script measures the volume by Monte Carlo as
1.046738 plus or minus 0.001243, and the quadrature gives 1.047198, which is $\pi h^{3}/3$ at
$h = 1$. The script also finds the radius of the base by bisection as 1.00000000 and the height of
the apex as 0.00000000. Figure 1 is drawn by `code/part1_figure1.py`.
