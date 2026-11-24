## Step 4.1: The angle integral gives $\pi - \frac{4}{3}$

**Reason.** The function $1 - |\sin\theta|^{3}$ is even, so its integral over the symmetric range is
twice its integral over $[0, \pi/2]$. The antiderivative of $\sin^{3}\theta$ is
$-\cos\theta + \frac{1}{3}\cos^{3}\theta$, and on $[0, \pi/2]$ its difference is
$0 - \left(-1 + \frac{1}{3}\right) = \frac{2}{3}$. The whole integral is therefore
$2\left(\frac{\pi}{2} - \frac{2}{3}\right) = \pi - \frac{4}{3}$.

**Computation.** The quadrature of $1 - |\sin\theta|^{3}$ over the range gives
$1.808259320256$, and $\pi - \frac{4}{3}$ is also $1.808259320256$. The quadrature of
$\sin^{3}\theta$ over the first quadrant is $0.666666666667$, and twice the half interval is
$1.808259320256$, which is the whole interval.

**Common mistake.** A reader may drop the absolute value and use the fact that $\sin^{3}\theta$ is
odd, but the integrand carries $|\sin\theta|^{3}$: `code/part3_verify.py` prints
$0.902368927062$ for the signed form at $\theta = -\pi/4$ against $0.430964406271$ for the correct
form, so the sign does not cancel.

**Result.** The angle integral is $\pi - \frac{4}{3} = 1.808259320256$, so
$$V = \frac{2}{3}a^{3}\left(\pi - \frac{4}{3}\right).$$

**Verification.** `code/part4_verify.py` prints `angle_integral_matches_quadrature` as
$1.8082593202564599$ against $\pi - \frac{4}{3}$, `sin_cubed_matches_quadrature` as
$0.6666666666666666$ against the antiderivative difference, `sin_cubed_matches_two_thirds` as
$0.6666666666666666$, `symmetry_doubles_half_interval` as $1.8082593202564599$, and the four checks
`angle_antiderivative_slope_at_0.1` to `angle_antiderivative_slope_at_1.3` with a tolerance of
$1.0\times10^{-7}$.
