# Step 1.3 The solid, its volume, and the areas of its faces

**Reason.** Three independent methods must agree on the volume before any order of
integration can be trusted: the determinant of three edge vectors, the pyramid formula, and
an iterated integral. The volume is also the value of every one of the six integrals of
$f = 1$, so the volume is the common target of the whole exercise.

**Computation.** The edge vectors at the vertex $(2, 2, 0)$ are $(0, 0, 1)$, $(0, -2, 0)$,
and $(-2, 0, 0)$. The determinant of the three edge vectors decides the volume. Its absolute value is
$$\left| \det \begin{pmatrix} 0 & 0 & 1 \\ 0 & -2 & 0 \\ -2 & 0 & 0 \end{pmatrix} \right| = 4.$$

Hence the volume is one sixth of that absolute value, that is $4/6 = {{p1.volume_latex}}$. The face $z = 0$
is the triangle with the corners $(2, 0)$, $(0, 2)$, and $(2, 2)$, whose area is
{{p1.face_z_zero_area}}; the height above that face is {{p1.height}}, and one third of the
product of the two numbers is ${{p1.volume_latex}}$.

The iterated integral of Step 1.2 with $f = 1$ is

$$\int_{0}^{2} \int_{2-y}^{2} \int_{0}^{(x+y-2)/2} 1 \, dz \, dx \, dy = {{p2.value_dzdxdy}}.$$

The areas of the four faces are {{p1.face_z_zero_area}} on the face $z = 0$,
{{p1.face_x_two_area}} on the face $x = 2$, {{p1.face_y_two_area}} on the face $y = 2$, and
{{p1.slanted_face_area}} on the face $x + y - 2z = 2$.

Figure 1 draws the solid with its four faces and its four vertices.

!figure part1_figure1.png | The solid $E$ with the faces $z = 0$, $x = 2$, $y = 2$, and $x + y - 2z = 2$, and the vertices $A(2,2,0)$, $B(2,2,1)$, $C(2,0,0)$, and $D(0,2,0)$.

**Result.** The volume of $E$ is ${{p1.volume_latex}}$; the checker prints
{{p1.volume}} by the determinant, by the pyramid formula, and by the iterated integral, and
{{p1.volume_mc}} by a random sample of {{p1.sample_count}} points with the error
{{p1.volume_mc_error}}. Figure 1 shows the solid.

**A common mistake.** A reader may take the mirror image of the slanted plane, that is the
half space $x + y - 2z \le 2$, but the solid lies above that plane, and the check `wrong
side of the slanted plane: its volume differs from the volume of E` prints
{{p1.wrong_side_volume}} against ${{p1.volume_latex}}$.

**Check.** `code/part1_verify.py` prints the three volume values, the four face areas, and
the volume of the mirror image; {{p1.check_passed}} of its {{p1.check_count}} checks pass.
