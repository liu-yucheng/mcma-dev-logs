# Problem statement

This file records the problem, the given data, and the quantity that the problem asks for.
Every fact names its source.
This file gives no solution.

## Source of the problem

- Source file: `problem/source/problem.png`.
  The file is a screen capture of one exercise page.
  The copy in `problem/source/` is byte-identical to the dataset file
  `D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261124/mcma-dataset-20261124/training/problems/calculus-15.7.28/problem.png`.
  Test: `md5sum` gives `27491ce292c66a5380b7be7fa30ff95e` for both files, and `sha256sum` gives
  `ad69f55b71ecffb9042d632389ecef394cc53c26700df52bc15ebb5beb9b2338` for the copy.
- Image geometry: 988 pixels wide, 233 pixels high, 8 bits for each channel, color type 6 (red, green, blue, alpha).
  Test: the header chunk `IHDR` of the copy.
- Page address, read from the top row of the image: `Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 28`.
  Source: `problem/source/problem.png`, top row.

## Statement

Quotation of the page text, which stays in its original language:

> Sketch the solid whose volume is given by the iterated integral.

The page gives the integral below the instruction:

$$
\int_{0}^{2}\int_{0}^{\,2-y}\int_{0}^{\,4-y^{2}} dx\,dz\,dy
$$

Source: `problem/source/problem.png`, body region.

## Given data

The integral is the only data of the problem.
The data are the three pairs of limits, the order of the differentials, and the integrand.

| Item | Given value | Where the value stands in the image |
| --- | --- | --- |
| Outermost integral | The variable is `y`. The lower limit is `0`. The upper limit is `2`. | The rightmost integral sign and its limits |
| Middle integral | The variable is `z`. The lower limit is `0`. The upper limit is `2 - y`. | The middle integral sign and its limits |
| Innermost integral | The variable is `x`. The lower limit is `0`. The upper limit is `4 - y^2`. | The leftmost integral sign and its limits |
| Order of integration | The differentials read `dx`, then `dz`, then `dy`. Thus `x` is the first variable, `z` is the second variable, and `y` is the third variable. | The end of the integrand field |
| Integrand | The value `1`. The field between the last integral sign and the first differential holds no expression. | The gap before `dx` |

Source for each row of the table: `problem/source/problem.png`.

Two limits depend on a variable of an outer integral: the upper limit of `z` holds `y`, and the upper limit of `x` holds `y`.
The upper limit of `x` does not hold `z`.
Source: `problem/source/problem.png`.

## Quantity that the problem asks for

The problem asks for one product: a sketch of the solid region in three-dimensional space.
The volume of that region equals the value of the iterated integral.
Source: `problem/source/problem.png`, the instruction line.

The problem asks for no number.
The problem asks for no evaluation of the integral.
A sketch must show the region, its boundary surfaces, and the position of the region in the coordinate system.
Source: the instruction line, and the word `Sketch`.

## Facts that the stage does not settle

The stage does not derive the inequalities that describe the region.
The stage does not name the boundary surfaces.
The stage does not evaluate the integral.
These items belong to the next stage.

## Files of the workspace

| Path | Content |
| --- | --- |
| `problem/problem.md` | This file |
| `problem/source/problem.png` | The exercise page, byte-identical to the dataset file |
| `code/` | Empty at the end of this stage, apart from `code/figures/` |
| `steps/` | Absent at the end of this stage |
