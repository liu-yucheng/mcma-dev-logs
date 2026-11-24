# Problem statement

## Source

- Source file of this stage: `problem/source/problem.png`.
- Original path of the file: the path below. This path is one line of 137 characters. A path cannot
  break across two lines, so this one line is longer than the limit of 119 characters.

```
D:/Program-Files/MCMA-Toolchain/dev-logs/.raw_data/dev-logs-20261124/mcma-dataset-20261124/training/problems/calculus-15.7.46/problem.png
```

- The file is a screenshot of one textbook exercise page. The breadcrumb of the page reads
  "Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 46".
- The image has 979 pixels of width and 175 pixels of height.
- The copy in `problem/source/problem.png` is byte-identical to the original file. See the section
  "Source integrity".

## Statement

Assume that the solid has constant density $k$. Find the moment of inertia about the $z$-axis of the
solid cone

$$\sqrt{x^{2}+y^{2}} \le z \le h.$$

The two sentences above transcribe the one sentence of the image and the inequality below it. The
transcription adds no condition and removes no condition.

## Transcription of the whole image

The image holds three text elements. No other text is on the page.

1. Breadcrumb: "Home > Calculus, Early Transcendentals > 15.7 Triple Integrals > Exercise: 46".
2. Button in the upper right corner: "Bookmark this page".
3. Exercise body: "Assume that the solid has constant density *k*. Find the moment of inertia about the
   *z*-axis of the solid cone $\sqrt{x^{2}+y^{2}} \le z \le h$."

## Given data

| Item | Value | Source of the fact |
| --- | --- | --- |
| Density of the solid | constant, equal to $k$ | the first sentence of the exercise body |
| Lower boundary of the solid | the cone $z = \sqrt{x^{2}+y^{2}}$ | the left member of the displayed inequality |
| Upper boundary of the solid | the plane $z = h$ | the right member of the displayed inequality |
| Shape name | solid cone | the second sentence of the exercise body |
| Height symbol | $h$ | the right member of the displayed inequality |
| Bounds on $x$ and on $y$ | none beyond the inequality | the statement names no other bound |
| Chapter and section | 15.7, Triple Integrals | the breadcrumb |

The statement prints no numerical value for $k$ and no numerical value for $h$. The answer is
therefore an expression in the symbols $k$ and $h$.

The statement prints no sign condition on $k$. The words "constant density $k$" make $k$ a constant.
This file records no sign for $k$, because the statement prints none.

The chain $\sqrt{x^{2}+y^{2}} \le z \le h$ means that both inequalities hold at the same time. The
set-builder form of the same condition is

$$E = \left\{\, (x,y,z) : \sqrt{x^{2}+y^{2}} \le z \ \text{and}\ z \le h \,\right\}.$$

This set-builder form restates the printed inequality. It is not a new condition.

$h$ is the height of the cone. The inequality describes a solid body with a positive volume only
when $h > 0$. At $h = 0$ the inequality forces $z = 0$ and $x^{2}+y^{2} \le 0$, so the set is the
single point $(0,0,0)$. At $h < 0$ the set is empty. The statement does not print the condition
$h > 0$.
This file records the condition as an implicit consequence of the words "solid cone", and it records
that the statement does not print it.

## Quantity asked

The question asks for the moment of inertia of the solid about the $z$-axis.

Section 15.7 defines the moment of inertia of a solid $E$ with density $\rho$ about the $z$-axis as

$$I_{z} = \iiint_{E} (x^{2}+y^{2})\,\rho(x,y,z)\,dV.$$

This formula is the textbook definition of the words of the question. It is not a result of this
problem. This stage computes no value and derives no bound.

## Naming of the solid

- The exercise calls the body a cone. The equation $z = \sqrt{x^{2}+y^{2}}$ is the upper nappe of a
  circular cone with apex at the origin and axis along the $z$-axis.
- The plane $z = h$ cuts the cone. The body $E$ is the part of the cone between the apex and the
  cutting plane, and the problem calls this part a solid cone.

These two statements read the printed equation and the printed plane. A later stage derives the
cross sections and the integration bounds from the set-builder form above.

## Source of each fact

| Fact | Source |
| --- | --- |
| The solid has constant density $k$. | `problem/source/problem.png`, first sentence |
| The question asks for the moment of inertia about the $z$-axis. | `problem/source/problem.png`, second sentence |
| The solid is the cone $\sqrt{x^{2}+y^{2}} \le z \le h$. | `problem/source/problem.png`, displayed inequality |
| The section is 15.7, Triple Integrals. | `problem/source/problem.png`, breadcrumb |
| The moment of inertia has the integral form quoted above. | the definition of Section 15.7 |
| $h > 0$ holds for a body of positive volume. | implicit in the words "solid cone"; the statement does not print it |

## Source integrity

- File name: `problem.png`.
- Size: 10533 bytes.
- SHA-256: `dc1a12df6dc173ccea7fd85772dc92e3887651b94fff05269bb8db9e360e331a`.
- The SHA-256 of the copy in `problem/source/problem.png` is the same value.
- Command that checked the copy: `cmp` returned no difference, and `sha256sum` printed the same digest
  for the original file and for the copy.

## Scope of this stage

This stage reads the problem, transcribes it, and copies the source file. It solves no part of the
problem, derives no bound, and grades nothing.
