## Part 2, Step 1: add the areas of the horizontal sections

**Goal.** Compute $V(E)$ by slicing the body at fixed heights.

**Reason.** Step 1.3 gives the area of every horizontal section as a function of the height alone, $\pi (1 - z)$. The slice method applies when the section at height $z$ has a known area for every height in the height range of the body, and here that range is $0 \leq z \leq 1$.

**Computation.** The volume is the integral of the section area over the height range.

$$V(E) = \int_{0}^{1} \pi (1 - z)\, dz = \pi \left[ z - \frac{z^2}{2} \right]_{0}^{1} = \pi \left(1 - \frac{1}{2}\right) = \frac{\pi}{2}$$

Figure 2 shows the section at $y = 0$ and the three chords whose lengths are the diameters of three sections. Each chord of length $2\sqrt{1 - z}$ gives the section area $\pi (1 - z)$.

**Result.** $V(E) = \dfrac{\pi}{2} = 1.5707963268$.

**Verification.** The check `[[check:part2:slice_areas]]` compares $\pi (1 - z)$ with a grid count at three heights. The check `[[check:part2:volume_height_integral]]` integrates the same area with the composite Simpson rule. The check `[[check:part2:volume_cartesian_quadrature]]` integrates the constant $1$ over $E$ by two nested adaptive quadratures, once in Cartesian order and once in polar order, and both give $1.5707963268$ inside $1.0 \times 10^{-6}$.

**Common mistake.** A reader may add the section areas without the factor $dz$, which would add $1$ for every height and would return a number of the size of the height range. The slice formula is an integral of the area over the height, $V = \int A(z)\, dz$, and not a sum of areas.
