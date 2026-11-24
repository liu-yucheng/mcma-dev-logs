# Problem: Mass, Center of Mass, and Moment of Inertia of a Solid in the First Octant

- Source image: `problem/source/problem.png`
- Dataset name: `calculus-15.7.49`
- Dataset root:
  `D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261124/mcma-dataset-20261124/training/problems/`
- Original image, relative to the dataset root: `calculus-15.7.49/problem.png`
- Textbook location that the image header shows:
  Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 49
- SHA-256 of the source image: `74112856cdba12d9083c199e7849180a508e44b55e3cf1884d86a9810872a674`
- Transcription method: a direct read of the raster image. The image holds no machine-readable
  text layer.

## Statement

> Let E be the solid in the first octant bounded by the cylinder x^2 + y^2 = 1 and the planes
> y = z, x = 0, and z = 0 with the density function
> rho(x, y, z) = 1 + x + y + z. Use a computer algebra system to find the exact values of the
> following quantities for E.
>
> (a) The mass
>
> (b) The center of mass
>
> (c) The moment of inertia about the z-axis

## Given Data

| Item | Value | Source of the fact |
| --- | --- | --- |
| Solid | `E` | Statement, `problem/source/problem.png` |
| Position of the solid | First octant | Statement, `problem/source/problem.png` |
| Boundary surface 1 | Cylinder `x^2 + y^2 = 1` | Statement, `problem/source/problem.png` |
| Boundary surface 2 | Plane `y = z` | Statement, `problem/source/problem.png` |
| Boundary surface 3 | Plane `x = 0` | Statement, `problem/source/problem.png` |
| Boundary surface 4 | Plane `z = 0` | Statement, `problem/source/problem.png` |
| Density function | `rho(x, y, z) = 1 + x + y + z` | Statement, `problem/source/problem.png` |
| Required precision | Exact values | Statement, `problem/source/problem.png` |
| Permitted tool | A computer algebra system | Statement, `problem/source/problem.png` |
| Meaning of "first octant" | `x >= 0`, `y >= 0`, and `z >= 0` | Standard definition of the term |

The image is the only source of a statement fact. The statement gives four boundary surfaces
and no inequality list. The next stage must read the inner limit and the outer limit of each
coordinate from these four surfaces and from the first-octant condition. The statement gives no
numeric parameter value.

## Quantity Asked

| Part | Quantity | Symbol that this document uses |
| --- | --- | --- |
| (a) | The mass of `E` | `m` |
| (b) | The center of mass of `E` | `(x_bar, y_bar, z_bar)` |
| (c) | The moment of inertia of `E` about the `z`-axis | `I_z` |

## What This Stage Did Not Do

This stage recorded the statement only. It did not derive a limit of integration, did not
compute `m`, did not compute a first moment, and did not compute `I_z`. Every numeric value of
the tutorial belongs to a later stage.

## Source Files

| File | Role | Change that this stage made |
| --- | --- | --- |
| `problem/source/problem.png` | The only source of the statement | None. The file is a byte copy. |
