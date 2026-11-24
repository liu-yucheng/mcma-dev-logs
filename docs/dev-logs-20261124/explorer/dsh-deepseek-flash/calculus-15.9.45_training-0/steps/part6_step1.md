# Part 6, Step 1: State the answer and read it as a computer algebra session

## Reason

The statement asks for a computer algebra system, so the page must show the session that the reader would type and the answer that the session returns. Writing the session also makes the structure of the solution visible: one definition, one integral, one closed form, and one comparison with the unit ball. The comparison is the part a reader remembers, because it says how much the bumps matter.

## Computation

The session has four lines. The first line defines the radius. The second line integrates the volume element of Step 1.2 with the limits of Step 1.1. The third line simplifies the result. The fourth line divides by the volume of the unit ball.

$$
\rho = 1 + \frac{1}{5}\sin 6\theta\,\sin 5\varphi,
$$

$$
V = \int_{0}^{2\pi}\int_{0}^{\pi}\frac{\rho^{3}}{3}\sin\varphi\,d\varphi\,d\theta,
$$

$$
V = \frac{136\pi}{99},
\qquad
\frac{V}{4\pi/3} = \frac{34}{33} = 1 + \frac{1}{33}.
$$

The two linear terms of the expansion vanish inside the session for the reason of Step 2.1, so the session returns a closed form in $\pi$ and not a special function.

## Result

The volume of the body is  = \frac{136\pi}{99} = 4.31572324130$ cubic length units. The body encloses $3.03030303$ percent more volume than the unit ball, and the excess itself is $\frac{4\pi}{99} = 0.126933036509$. The four numerical methods of Part 4 agree with this value within their own errors, and Figure 1 shows the body whose volume it is.

## Common mistake

A reader may report the excess $\frac{4\pi}{99}$ as the volume and leave out the unit ball, but the volume is the sum of both terms. A reader may also report $4.32$ and stop, but the exact value $\frac{136\pi}{99}$ is available and the decimal is only its shadow; the statement asks for the exact answer.

## Verification

The scripts `code/part3_verify.py` and `code/part4_verify.py` both reach $\frac{136}{99}$ for the quotient $V/\pi$, one from the exact expansion and one from the quotient of the numerical volume and $\pi$. The row `volume over pi: full expansion against the single surviving correction` of `code/outputs/part4_summary.md` reports $\frac{136}{99}$ against $\frac{136}{99}$ with a difference of $0$, and the row `volume: exact polynomial against adaptive quadrature` reports $4.3157232413$ against $4.3157232413$ with a difference of $8.882 \times 10^{-16}$.
