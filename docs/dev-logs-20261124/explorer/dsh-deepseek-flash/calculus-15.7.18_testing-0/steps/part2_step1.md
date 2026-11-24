# Step 2.1: choose one order and write the three pairs of limits

## Reason

An order of integration reads the solid from the inside out. The inner variable runs between two surfaces, the middle variable runs between two curves of a projection, and the outer variable runs between two numbers. Here the inner variable is $z$, because the cylinder gives $z$ as a function of $y$ alone, and $y$ then runs over one interval.

A reader may take $x$ from $0$ to $1$ in the middle integral, because the projection of the solid reaches $x = 1$, but the limit of $x$ is written at one fixed value of $y$, and there the plane gives $x \le y/3$.

## Computation

The inner pair comes from the cylinder at a fixed $y$: $0 \le z \le \sqrt{9 - y^{2}}$. The middle pair comes from the plane $y = 3x$: $0 \le x \le \dfrac{y}{3}$. The outer pair comes from the two ends of the disk: $0 \le y \le 3$.

The integral of the density $z$ over the solid is therefore

$$\iiint_{E} z\,dV = \int_{0}^{3} \int_{0}^{y/3} \int_{0}^{\sqrt{9 - y^{2}}} z\,dz\,dx\,dy.$$

## Result

The order is $dz\,dx\,dy$ with the limits $0 \le z \le \sqrt{9 - y^{2}}$, $0 \le x \le \dfrac{y}{3}$ and $0 \le y \le 3$. At the height $y = {{p2_demo_height}}$ the inner limit gives $z \le {{p2_demo_z_high}}$ and the middle limit gives $x \le {{p2_demo_x_high}}$. Figure 4 shows both limits at that height.

## Verification

`code/part2_verify.py` samples ${{p2_membership_sample_count}}$ points with the limits of this order and with the inequalities of Step 1.1, and it finds no point that one test accepts and the other test rejects. It integrates the same limits and compares the result ${{p2_volume}}$ with the volume of Part 1.
