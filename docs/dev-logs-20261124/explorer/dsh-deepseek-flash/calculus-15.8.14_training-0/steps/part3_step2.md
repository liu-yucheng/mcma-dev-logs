## Step 3.2 - Find the vertical extent and cross-check the description

**Reason.** The drawing needs the lowest and the highest height of the body, because those two heights fix the height of the drawn frame.
The lowest point sits in the middle of the footprint and the highest point sits in the middle as well, because both surfaces grow away from the vertical axis.
A volume computed from the description is a cross-check of the description, and the problem does not ask for a volume.

**Computation.** The lowest height is the smallest value of the lower surface over the footprint, and the highest height is the largest value of the upper surface over the footprint.

$$ z_{\min} = \min_{r^{2} \le 5/2} r^{2} = 0, \qquad z_{\max} = \max_{r^{2} \le 5/2} \left(5 - r^{2}\right) = 5 $$

The vertical bar at the squared distance $r^{2}$ has the length $5 - 2 r^{2}$, so the volume follows from a sweep of that bar over the footprint.

$$ V = \int_{0}^{\sqrt{5/2}} \left(5 - 2 r^{2}\right) 2 \pi r \, dr = \pi \left(\frac{5}{2}\right)^{2} = \frac{25 \pi}{4} = 19.634954084936 $$

**Result.** The check finds the rim of the body where the bar length falls to zero, and it compares the two heights with a bounded search [scan [[check:part3:vertical_extent]]].
The rim squared radius is $2.500000000$ against $\frac{5}{2} = 2.5$, the lowest height is $0.000000000000$ against $0$, and the highest height is $5.000000000000$ against $5$.
A sample of 5001 points of the two surfaces prints the same extent $0$ and $5$, and the bar at the middle of the footprint has the length $5.000000$.
The volume from the cylinder sweep is $19.634954084936$, the volume from the two slice ranges is $19.634954084936$, and the closed form $\frac{25 \pi}{4}$ is $19.634954084936$ [scan [[check:part3:volume_two_methods]]].
Random sampling of the box gives $19.632512$ against $19.634954$, with a standard error of $0.017603$, so the gap is $0.139$ standard errors.

**Common mistake.** A reader may take the highest point of the body for a point on the meeting circle, but the meeting circle sits at $z = \frac{5}{2}$, and the highest point of the body sits on the vertical axis at $z = 5$.

**Answer of Part 3.** The body is $E = \{(x, y, z) : x^{2} + y^{2} \le z \le 5 - x^{2} - y^{2}\}$, it is closed, and it spans the heights $0 \le z \le 5$.
