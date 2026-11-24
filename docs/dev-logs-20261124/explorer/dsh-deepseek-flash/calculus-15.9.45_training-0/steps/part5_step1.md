# Part 5, Step 1: Count the peaks and the valleys

## Reason

A single number describes the volume, but the reader also wants to know what the number measures. The surface has peaks where the radius is largest and valleys where it is smallest, and the count of those directions explains why the volume lands between the volume of the unit ball and the volume of the sphere of radius $\frac{6}{5}$. The count also tests the parameters $m = 6$ and $n = 5$ of the statement against the drawing of Figure 1.

## Computation

The radius is largest where $\sin 6\theta\,\sin 5\varphi = 1$. The sine of $5\varphi$ reaches $1$ at three values of $\varphi$ in the interval $0 \le \varphi \le \pi$, and the sine of $6\theta$ reaches $1$ at six values of $\theta$ in the interval $0 \le \theta \le 2\pi$, so the number of peaks is

$$
3 \times 6 = 18 .
$$

The radius is smallest where $\sin 6\theta\,\sin 5\varphi = -1$. The sine of $5\varphi$ reaches $-1$ at two values of $\varphi$, because the value $\varphi = \pi$ is the pole and not a minimum of the sine, so the number of valleys is

$$
2 \times 6 = 12 .
$$

Six of the eighteen peaks lie on the equator $\varphi = \frac{\pi}{2}$, where the drawing of Figure 1 shows them as the bright band around the middle of the body.

## Result

The script reports $18$ peak directions, three polar bands of peaks at $\varphi = 0.314159$, $1.570796$, and $2.827433$, two polar bands of valleys at $\varphi = 0.942478$ and $2.199115$, and six peaks on the equator. The marked peak sits at $\left(0.358185,\,0.095975,\,1.141268\right)$ with length $1.2$, and the marked valley sits at $\left(0.167511,\,0.625160,\,0.470228\right)$ with length $0.8$. The radius on the drawn map grid runs from $0.800122$ to $1.199878$, which are the two bounds of Step 1.1 seen through the resolution of the grid.

## Common mistake

A reader may count the valleys as three bands per pole, but the sine of $5\varphi$ reaches $-1$ only twice in the interval $0 \le \varphi \le \pi$, so the count of valleys is $12$ and not $18$. A reader may also take the extremes of the drawn grid as exact bounds, but the grid samples the angles at a finite step, so its extremes fall short of $\frac{4}{5}$ and $\frac{6}{5}$ by $1.218 \times 10^{-4}$.

## Verification

The script `code/part5_verify.py` scans the angles for the extremes, compares the count of the peak directions with the count that the scan finds, checks the length of each marked point against its radius, and measures the extremes of the drawn grid. The rows of `code/outputs/part5_summary.md` report $18$ peak directions, three polar bands of peaks against three from the scan, two polar bands of valleys against two, the lengths $1.2$ and $0.8$ of the marked points with differences of $2.220 \times 10^{-16}$ and $1.110 \times 10^{-16}$, and the grid extremes $0.800122$ and $1.199878$ against $\frac{4}{5}$ and $\frac{6}{5}$ with a difference of $1.218 \times 10^{-4}$ each.
