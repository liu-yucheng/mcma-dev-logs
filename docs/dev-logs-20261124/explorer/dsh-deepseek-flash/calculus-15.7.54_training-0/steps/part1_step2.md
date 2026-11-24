## Part 1, Step 2: project the body on the plane $z = 0$

**Goal.** Find the projection $D$ and its area, because every later integral uses $D$ as its outer region.

**Reason.** A projection onto the plane $z = 0$ drops the coordinate $z$ and keeps the coordinates $x$ and $y$. The projection of $E$ is therefore the set of pairs $(x, y)$ that occur in at least one point of $E$. Step 1 shows that a pair occurs in a point of $E$ exactly when $x^2 + y^2 \leq 1$, and the height range of that pair is not empty then.

**Computation.** Drop $z$ from the three inequalities of $E$. The inequalities $0 \leq z \leq 1 - x^2 - y^2$ hold for some $z$ exactly when $0 \leq 1 - x^2 - y^2$, that is exactly when $x^2 + y^2 \leq 1$.

$$D = \left\{(x, y) : x^2 + y^2 \leq 1\right\}, \qquad \operatorname{area}(D) = \pi \cdot 1^2 = \pi$$

**Result.** The projection is the closed unit disk in the plane $z = 0$, and its area is $\pi$. Figure 1 right panel draws it. The vertical line above each interior point of $D$ meets the body in one segment, so $D$ is also the region of the outer two integrals.

**Verification.** The check `[[check:part1:projection_membership]]` builds the boundary polygon from a root search and asks the polygon and the inequality about the same $231361$ plane points. The two answers disagree on $0$ points. The check `[[check:part1:projection_area]]` measures the area of the polygon by the shoelace sum, $3.1415527794$, and the radial trapezoid sum, and both agree with $\pi$ inside $1.0 \times 10^{-4}$. The check `[[check:part1:volume_by_cell_count]]` counts the columns above $D$ and returns $1.5707932$ for the volume, which matches the value of Part 2 before Part 2 is written.

**Common mistake.** A reader may call this projection the projection on the plane $x = 0$, because the figure shows the disk in the plane of the page. The pair that survives is $(x, y)$, so the projection lies on the plane $z = 0$; a projection that kept $x$ and $z$ would lie on the plane $y = 0$ and would be a different region.
