## Step 5.2 - Collect the numbers of the answer

**Reason.** The answer of this problem is a drawing with a description, so the final step states both parts and checks that the numbers of the page agree with the numbers of the scripts.
A reader who copies one number from the page must find the same number in the check that produced it.
So the summary repeats the derivation once and prints every value beside its check.

**Computation.** The answer has four numbers: the squared radius of the meeting circle $\frac{5}{2}$, the height of the meeting circle $\frac{5}{2}$, the area of the widest section $\pi \frac{5}{2}$, and the height of the top of the body $5$.
The description has one line, and the drawing has the scale of Step 4.2.

**Result.** The check recomputes the four numbers with methods that differ from the methods of Parts 1 to 4 [scan [[check:part5:summary_numbers_agree]]].
The root search returns the squared radius $2.500000000$ against $\frac{5}{2}$, the cell count returns the area $7.854277778$ against the closed form $7.853981634$, and the relative gap of the two areas is $3.771 \times 10^{-05}$.
A quadrature of the shell volume returns $19.634954085$ against $\frac{25 \pi}{4} = 19.634954085$.

**Common mistake.** A reader may take the area of the widest section for a rounded value such as $7.85$, but the closed form is $\pi \frac{5}{2} = 7.853981634$, and the grid count differs from it only in the fifth digit.

**Answer of Part 5.** The solid that the two paraboloids enclose is $E = \{(x, y, z) : x^{2} + y^{2} \le z \le 5 - x^{2} - y^{2}\}$, a closed body whose footprint is the disk $x^{2} + y^{2} \le \frac{5}{2}$, whose rim is the circle $x^{2} + y^{2} = \frac{5}{2}$ at $z = \frac{5}{2}$, and whose heights run from $0$ to $5$.
Figure 3 draws that body with one scale on each axis, and Figure 1 and Figure 2 show the two surfaces and the sections that justify the outline.
