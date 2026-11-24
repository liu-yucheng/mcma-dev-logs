# Part 3, Step 1: a linear change of variable turns the ellipsoid into a ball

**Reason.** The integrand is a quadratic form and the region is the level set of the same form. A linear map
that sends the ellipsoid to the unit ball also sends the quadratic form to the squared radius. The integral then
has a constant factor, the absolute value of the determinant of the map, and a simpler integrand.

A reader may take the factor as 1 because the map only rescales, but the limits give the determinant
$1/\sqrt{6}$, because the three rescale factors are $1$, $1/\sqrt{2}$, and $1/\sqrt{3}$ and their product is the
determinant.

**Computation.** Put $x=u$, $y=v/\sqrt{2}$, $z=w/\sqrt{3}$. Then

$$Q=x^{2}+2y^{2}+3z^{2}=u^{2}+v^{2}+w^{2},\qquad \left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|=\frac{1}{\sqrt{6}}={{part3.jacobian}}.$$

The ellipsoid becomes the unit ball $B$, and the integral becomes

$$\iiint_{P}\left(1-Q\right)dV=\frac{1}{\sqrt{6}}\iiint_{B}\left(1-u^{2}-v^{2}-w^{2}\right)dV .$$

**Result.** The map carries the boundary of the ball onto the boundary of $P$ with a residual of zero, and the
volume factor is {{part3.jacobian}}.

**Verification.** `code/part3_verify.py` compares the determinant with the closed form and checks the boundary
map. The check `jacobian_determinant_against_closed_form` prints {{part3.jacobian}} against the closed form
{{part3.jacobian}}, the check `pointwise_transformation_mismatch` prints the worst mismatch of the transformed
integrand against 0, and the check `unit_sphere_maps_to_boundary_of_P` prints the largest boundary residual
against 0.
