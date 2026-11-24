# Step 1.1: Read the three surfaces

## Reason

We must know the shape and the position of each surface before we write an integral. The form of each
equation gives that information.

## Computation

1. The equation $x^2+z^2=4$ contains no $y$. Thus every plane $y=c$ cuts the surface in the same circle
   of radius $2$. The surface is a circular cylinder, its axis is the $y$ axis, and its radius is $2$.
2. The equation $y=-1$ contains no $x$ and no $z$. Thus the surface is the horizontal plane through
   $y=-1$.
3. The equation $y+z=4$, that is $y=4-z$, contains no $x$. Thus the surface is a plane parallel to the
   $x$ axis, and it tilts in the $z$ direction.

## Check

The point $(2,0,0)$ satisfies $x^2+z^2=4$, and the point $(2.1,0,0)$ does not. The normal vector of
$y=-1$ is $(0,1,0)$, and the normal vector of $y+z=4$ is $(0,1,1)$. The two vectors are not parallel, so
the two planes are not parallel. The solid is therefore not a prism, and a slice of the solid can
differ in shape from the circle of the cylinder.

## Result

The solid is bounded by one circular cylinder of radius $2$ and two planes that are not parallel.

## Verification

`code/part1_verify.py` measures the radius of the cylinder two ways. The largest $|x|$ on a fine grid
of the disk is $2.000000$, and the positive root of $x^2-4=0$ is $2.000000$. The accepted difference is
$0.0025$.
