## Step 4.2 Mass and moments from the shadow

**Reason.** A volume integral over the solid equals an integral over the shadow of the integrand times the height,
because the fibre above each shadow point is the interval from $z = 0$ to $z = h(x, y)$. For the moment about the
plane $z = 0$ the inner integral of $z$ over that interval is $\frac{h^{2}}{2}$.

$$M = \int_{\text{shadow}} 4 h \, dA, \qquad M_{yz} = \int_{\text{shadow}} 4 x h \, dA, \qquad
  M_{xy} = \int_{\text{shadow}} 2 h^{2} \, dA$$

**Computation.** The three integrals over the rectangle give {{p4_shadow_mass}},
{{p4_shadow_moment_yz}} and {{p4_shadow_moment_xy}}. A sampling of {{p4_accepted_points}} accepted points inside
the solid gives the center {{p4_sampled_center}}.

**Result.** The mass from the shadow is {{p4_shadow_mass}}, the moment about the plane $x = 0$ is
{{p4_shadow_moment_yz}}, and the moment about the plane $z = 0$ is {{p4_shadow_moment_xy}}. Each value equals the
value of Parts 2 and 3, so the shadow method confirms the earlier integrals by a different route. Verified by
`code/part4_verify.py`.
