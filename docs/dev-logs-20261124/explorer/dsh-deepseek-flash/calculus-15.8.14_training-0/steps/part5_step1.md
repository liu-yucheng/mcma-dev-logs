## Step 5.1 - Check that every label sits on the surface that it names

**Reason.** A label that floats beside a curve teaches a wrong reading, so each label of the drawing is tested against the equation that it names.
The drawing places three labels: one on the lower paraboloid, one on the upper paraboloid, and one on the meeting circle.
Each label points at a place, and that place must satisfy its own equation to machine precision.

**Computation.** A label of the lower surface points at a place of the form $(r \cos \theta, r \sin \theta, r^{2})$.
A label of the upper surface points at a place of the form $(r \cos \theta, r \sin \theta, 5 - r^{2})$.
A label of the meeting circle points at a place of the form $(r \cos \theta, r \sin \theta, \frac{5}{2})$ with $r^{2} = \frac{5}{2}$.

**Result.** The check reads the three anchor places from the drawing code and tests each place against both surface equations [scan [[check:part5:label_anchors_on_surfaces]]].
The lower anchor has the squared radius $1.562500000$ and the height $1.562500000$, so its gap against the lower surface is $2.220 \times 10^{-16}$ and its gap against the upper surface is $1.875$.
The upper anchor has the squared radius $1.322500000$ and the height $3.677500000$, so its gap against the lower surface is $2.355$ and its gap against the upper surface is $0.000$.
The circle anchor has the squared radius $2.500000000$ and the height $2.500000000$, so its gap against both surfaces is $4.441 \times 10^{-16}$, and the label count is $3$.

**Common mistake.** A reader may take a label for a title of the picture, but each label points with a line at a point of the surface that its equation names, and the check tests that point.
