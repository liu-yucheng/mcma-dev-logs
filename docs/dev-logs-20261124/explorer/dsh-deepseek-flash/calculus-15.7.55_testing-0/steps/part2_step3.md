# Part 2, Step 3: no scaling of the region improves the value

**Reason.** The exchange argument uses only the sign of the integrand. A second test follows from the scale of
the region: multiply the whole body by a factor $t$ and ask how the integral changes at $t=1$. When that
derivative is zero at $t=1$, the unit scale is a stationary point of the family, and the sign of the second
change shows that the value falls on both sides.

A reader may take the derivative at $t=1$ as positive because the body grows with $t$, but the limits give a
derivative that vanishes at $t=1$ and is negative on both sides, because the integrand is zero on the boundary
surface and the new shell carries no positive amount.

**Computation.** Write the scaled integral as a function of the factor.

$$F(t)=\iiint_{tP}\left(1-Q ight)dV=t^{3}\iiint_{P}\left(1-t^{2}Q ight)dV .$$

Collect the two moments $V(P)=\iiint_{P}dV$ and $M(P)=\iiint_{P}Q\,dV$. Then

$$F(t)=t^{3}V(P)-t^{5}M(P).$$

With $V(P)={{part1.ellipsoid_volume}}$ and $M(P)={{part2.quadratic_moment}}$ the derivative at $t=1$ is
$3V-5M=0$. That identity is the statement $5M=3V$, and it holds for every ellipsoid, because the mean value of
$Q$ over $P$ is $3/5$.

**Result.** The derivative at $t=1$ is {{part2.scaled_derivative}}, that is, zero to the printed accuracy. The value over
$0.80P$ is {{part2.candidate_rows.3.value}} and the value over $1.25P$ is {{part2.candidate_rows.4.value}}, so
both scales stay below the maximum {{part2.maximum_value}}. The unit scale is therefore a maximum of the family
and not a saddle point.

**Verification.** `code/part2_verify.py` computes the derivative by quadrature and compares it with zero. The
check `scaled_family_derivative_at_one` prints {{part2.scaled_derivative}} against 0, and the check
`stationarity_three_volume_against_five_moment` prints $5M$ against $3V$ with $M={{part2.quadratic_moment}}$.
