## Step 5.1: Check the volume with horizontal slices

**Reason.** A second route to the same number does not use the angle integral. At the height $z$ the
slice of the solid is the set of base points that lie inside the sphere and inside the cylinder at
once. The sphere keeps the disk of radius $\sqrt{a^{2} - z^{2}}$ about the origin, and the cylinder
keeps the disk of radius $a/2$ about $(a/2, 0)$. The slice is the lens where the two disks overlap,
and the volume is the integral of the lens area over $z$ from $-a$ to $a$.

**Computation.** Take $a = 1$. The lens area is $0.785398163397$ at $z = 0$, $0.699791506351$ at
$z = 0.5$, and $0.242119161289$ at $z = 0.9$. The integral of the lens area over the whole range of
$z$ is $1.205506213504$, which is the volume of step 4.2.

**Common mistake.** A reader may take a slice for the disk of the sphere alone, but the cylinder
keeps only the part of that disk inside its own disk: `code/part5_verify.py` prints
$0.699817782211$ for a grid count of the lens at $z = 0.5$ against $0.699791506351$ for the lens
formula, so the slice is smaller than the sphere disk.

**Result.** The slice construction gives $1.205506213504$ at $a = 1$, which agrees with
$\frac{6\pi - 8}{9}$.

**Verification.** `code/part5_verify.py` prints `horizontal_slices_match_closed_form` as
$1.205506213504$ against the closed form with a tolerance of $1.0\times10^{-7}$, and
`lens_area_at_z_0.5` as $0.699791506351$ against the grid value $0.699817782211$ with a tolerance of
$3.0\times10^{-3}$.
