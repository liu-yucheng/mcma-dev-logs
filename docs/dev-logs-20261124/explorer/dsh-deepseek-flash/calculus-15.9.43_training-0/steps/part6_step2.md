# Part 6, Step 2: The recipe for the graphing device, and the length of the outline

## Reason

The device needs explicit parametrizations and explicit ranges, and it needs a window that holds
the whole drawing with room for the labels. The length of the outline is a final check: it can be
computed in closed form and measured on the drawn polyline, so the drawing can be compared with
the body that it stands for.

## Computation

Give the device four objects. First, the lateral face in cylindrical coordinates:
$x=3\cos\theta$, $y=3\sin\theta$, $z=z$ with $0\le\theta\le 2\pi$ and $0\le z\le 10$. Second,
the cap in spherical coordinates about $(0,0,10)$: $x=3\sin\varphi\cos\theta$,
$y=3\sin\varphi\sin\theta$, $z=10+3\cos\varphi$ with $0\le\varphi\le\frac{\pi}{2}$ and
$0\le\theta\le 2\pi$. Third, the lower disk: $x=r\cos\theta$, $y=r\sin\theta$, $z=0$ with
$0\le r\le 3$. Fourth, the outline on the plane $y=0$: the base segment from $(-3,0)$ to
$(3,0)$, the two vertical sides up to $z=10$, and the arc $x=3\cos\alpha$, $z=10+3\sin\alpha$
with $0\le\alpha\le\pi$. Set the window to $|x|\le 4.4$, $|y|\le 4.4$, $-0.6\le z\le 15.2$, and
mark the heights $3$, $10$, and $13$ on the vertical axis.

The outline has the length

$$L=2\cdot 10+2\cdot 3+\pi\cdot 3=26+3\pi=35.4247779608 .$$

## Result

The four parametrizations above draw the silo: the lateral face, the cap, the lower disk, and the
outline of the projection. The outline closes at the length $35.4247779608$, and the window of
the recipe holds every label: the nearest data point leaves a free band of $1.4$ units and the
labels need only $0.55$ units of inset. Figure 1 shows the result, with the three faces labelled
at points of their own surfaces.

## Common mistake

A reader may take the outline as the two vertical sides and the arc only, but the base closes the
region; the closed form $26+3\pi$ includes the base of length $6$.

## Verification

Verification script: `code/part6_verify.py` check C6 measures the drawn polyline and prints $35.4247465109$ against
$26+3\pi=35.4247779608$, a difference of $3.145\times 10^{-5}$ that the polygonal arc explains.
Check C4 compares the free band of the window with the label inset and prints $1.4$ against
$0.55$. Check C5 puts the three label anchors of `code/figure_anchors.py` against the window and
prints 0 anchors outside. Check C7 compares a coarse mesh with a fine mesh and prints an error of
$5.1710659939$ for the coarse mesh against $0.145003622417$ for the fine mesh, so a coarse
drawing is visibly wrong and a fine drawing is not.
