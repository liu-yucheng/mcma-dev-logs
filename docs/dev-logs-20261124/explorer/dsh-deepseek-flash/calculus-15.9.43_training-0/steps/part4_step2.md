# Part 4, Step 2: A mesh that approaches the drawn surface

## Reason

A graphing device draws triangles, not curved surfaces. If the triangles are to stand for the
three faces, their total area must approach each closed form as the triangles become small. This
step measures that approach, so the surface of the picture is the surface of the computation and
not a different shape.

## Computation

Divide each face into cells and split each cell into two triangles. Record the mesh area at the
resolutions $16$, $32$, $64$, and $128$ cells along one direction. A mesh of a curved surface is
inscribed in the surface, so its area is smaller than the closed form, and the gap must shrink
as the cells shrink.

At the resolution $128$ the mesh gives $188.476635056$ for the lateral face, $56.5330568541$ for
the cap, and $28.2629804126$ for the base. The closed forms of Step 4.1 are $188.495559215$,
$56.5486677646$, and $28.2743338823$.

## Result

Every mesh under-estimates its face, and every curve of Figure 3 falls to the closed form. At
the resolution $128$ the three relative errors are $1.004\times 10^{-4}$,
$2.761\times 10^{-4}$, and $4.016\times 10^{-4}$, all below the tolerance
$5\times 10^{-4}$ that the figure draws as a dashed line. The mesh total at that resolution is
$273.272672323$ against the closed form $273.318560862$, so a drawing at that resolution shows
the surface with an error of about one part in ten thousand.

## Common mistake

A reader may take the area of a coarse mesh as the area of the surface, but an inscribed mesh
under-estimates: at the resolution $128$ the total is $273.272672323$ against the closed form
$273.318560862$, as the print of `code/part4_figure1.py` shows.

## Verification

Verification script: `code/part4_verify.py` check C5 computes the mesh area at the four resolutions, prints the
finest values above, and requires each sequence to rise toward its closed form. Figure 3 is drawn
by `code/part4_figure1.py`, which prints the total at every resolution, asserts that the finest
relative error of each face is below $5\times 10^{-4}$, and asserts that each legend stays inside
its axes box before it writes the file. Check C4 of the same script gives the total area of the
three faces for the comparison.
