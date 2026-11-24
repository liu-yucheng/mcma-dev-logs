# Part 4, Step 1: Decide the rules of the drawing before drawing

## The reason

The exercise asks for a sketch. A sketch is not a free picture: it must show the shape that the
limits describe, and a reader must be able to read the equations from it. So the drawing needs
rules, and each rule must come from Part 1 to Part 3 and not from taste.

## The computation

The rules follow from the facts that the earlier parts established.

1. **Frame.** The box is $[0,4] \times [0,2] \times [0,2]$, from Part 1, Step 2. The axes carry one
   arrow and one letter each, and no second mark for the same axis.
2. **Patches.** The drawing shows the five patches of Part 3, Step 1, and no other surface. Each
   patch is a graph over a parameter rectangle, so the drawing samples each patch on a grid.
3. **Opacity.** A patch that stands in front of the body must stay above one half in opacity, so
   the body reads as a closed body. The near face may go below one half, so that the interior stays
   visible through it.
4. **Labels.** The label of a patch hangs from a point that lies on that patch. A label that floats
   near a surface but does not touch it gives a false position.
5. **Corners.** The five corners of Part 3, Step 2 carry their letters, and the letters are the
   letters of the corner table.
6. **Cut.** One horizontal cut is drawn, because the cut is the reason for the shape of the
   boundary. The cut is the rectangle of Part 2, Step 1.

These rules are the same for the reader and for the check. The check of Part 4, Step 2 measures the
drawn mesh, so a rule that the drawing ignores also fails the check.

## The result

The drawing obeys six rules: the box and one arrow per axis, the five patches, an opacity above
one half for the four far patches, one label per patch at a point of that patch, the five corner
letters, and one drawn cut. The scripts `code/part4_figure1.py` and `code/part4_figure2.py` build
the drawing from these rules.

## The check

`code/part4_verify.py`, section "labels". For every label point, the script computes the residual of
its own equation, the smallest residual over the other four equations, and the test of membership
in the solid. The residual of its own equation is $0$, the smallest other residual is at least
$0.354$, and the point is inside the solid. So each label sits on exactly one patch and inside the
solid. The label of the patch $y = 0$ is not drawn in the assembled figure, because that patch is
the far face in the chosen point of view and its label would fall on a nearer patch.
