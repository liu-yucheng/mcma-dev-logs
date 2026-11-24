# Part 2, Step 1: adding a positive point never lowers the value

**Reason.** A region that maximizes an integral must be saturated: no point outside it may carry a positive
integrand, and no point inside it may carry a negative integrand. This statement is the exchange argument that
justifies the candidate of Part 1, and it also excludes every smaller region inside the ellipsoid.

A reader may take a smaller region inside the ellipsoid as equally good, but the limits give a strictly larger
value for the full ellipsoid, because the integrand is positive on the whole interior except the boundary.

**Computation.** Let $E$ be any bounded region and let $P$ be the positive part $\{Q<1\}$. Split the integral.

$$\iiint_{E} f\,dV=\iiint_{E\cap P} f\,dV+\iiint_{E\setminus P} f\,dV .$$

The first term is at most $\iiint_{P} f\,dV$, because $f\ge 0$ on $P$ and $E\cap P\subseteq P$. The second term
is at most 0, because $f\le 0$ outside $P$. Therefore

$$\iiint_{E} f\,dV\le \iiint_{P} f\,dV,$$

The equality holds exactly when $E$ differs from $P$ by a set of zero volume.

**Result.** The positive part $P$ is a maximizer, and every maximizer agrees with $P$ up to a set of zero
volume, so the maximum value is the integral over $P$ alone.

**Verification.** `code/part2_verify.py` splits the unit ball into the part inside $P$ and the part outside $P$.
The check `ball_split_sum_against_direct_quadrature` prints the sum {{part2.ball_inside}} plus
{{part2.ball_outside}} against the direct quadrature of the whole ball. The check
`ball_part_outside_P_is_negative` prints {{part2.ball_outside}} against the expected bound 0.
