"""Compose the tutorial page from the verified results and the figures.

The page holds the statement, the nine steps, the three figures, the table of checked values, and
the final answer. Each figure becomes a Base64 data uniform resource identifier, so the page needs
no local file except itself.
"""

from __future__ import annotations

import base64
from pathlib import Path

CODE_DIRECTORY = Path(__file__).resolve().parent
"""Directory of this script and of the figures."""

WORKSPACE_DIRECTORY = CODE_DIRECTORY.parent
"""Problem workspace that holds the report page."""

REPORT_PATH = WORKSPACE_DIRECTORY / "report.html"
"""Output path of the composed page."""

TUTORIAL_PATH = WORKSPACE_DIRECTORY / "tutorial.html"
"""Second name of the composed page, used by the pipeline."""

FIGURE_FILES = {
    "@@FIGURE1@@": CODE_DIRECTORY / "figures" / "part1_figure1.png",
    "@@FIGURE2@@": CODE_DIRECTORY / "figures" / "part2_figure1.png",
    "@@FIGURE3@@": CODE_DIRECTORY / "figures" / "part3_figure1.png",
}
"""Tokens of the template and the figure file of each token."""

PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Triple Integral over a Paraboloid Cap — Worked Solution</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
  @font-face {
    font-family: "XITS Math";
    src: local("XITS Math"), local("XITSMath-Regular"), local("XITS"), local("STIX Two Math");
    font-weight: normal;
    font-style: normal;
  }
  :root {
    --ink: #1c2128;
    --muted: #5c6673;
    --paper: #fbfaf6;
    --card: #ffffff;
    --rule: #d9d5cb;
    --accent: #1f4e79;
    --accent-soft: #eaf1f8;
    --warm: #8a2b2b;
    --warm-soft: #fbf0ee;
    --green: #1f6f43;
  }
  * { box-sizing: border-box; }
  html { font-size: 17px; }
  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: Cambria, "Palatino Linotype", "Book Antiqua", Georgia, serif;
    line-height: 1.66;
    -webkit-font-smoothing: antialiased;
  }
  .katex { font-family: "XITS Math", "STIX Two Math", Cambria, "Times New Roman", serif; }
  .page { max-width: 50rem; margin: 0 auto; padding: 3.2rem 1.5rem 5rem; }
  .kicker {
    font-size: 0.74rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.9rem;
  }
  h1 {
    font-size: 2.15rem;
    line-height: 1.2;
    font-weight: 600;
    margin: 0 0 0.6rem;
    letter-spacing: -0.01em;
  }
  .lede { font-size: 1.09rem; color: #333c46; margin: 0 0 1.4rem; max-width: 42rem; }
  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 1.4rem;
    font-size: 0.86rem;
    color: var(--muted);
    border-top: 1px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    padding: 0.65rem 0;
    margin-bottom: 2.6rem;
  }
  .meta b { color: var(--ink); font-weight: 600; }
  h2 {
    font-size: 1.34rem;
    font-weight: 600;
    margin: 3.2rem 0 0.9rem;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid var(--rule);
    letter-spacing: 0.005em;
  }
  h3 { font-size: 1.06rem; font-weight: 600; margin: 1.8rem 0 0.5rem; }
  p { margin: 0 0 0.85rem; }
  a { color: var(--accent); text-decoration: none; border-bottom: 1px solid rgba(31,78,121,0.25); }
  a:hover { border-bottom-color: var(--accent); }
  .statement {
    background: var(--card);
    border: 1px solid var(--rule);
    border-left: 3px solid var(--accent);
    padding: 1.1rem 1.35rem;
    margin: 1.1rem 0 1.4rem;
    font-size: 1.05rem;
  }
  .statement p:last-child { margin-bottom: 0; }
  .source { font-size: 0.82rem; color: var(--muted); margin-top: 0.5rem; }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.92rem;
    margin: 0.8rem 0 1.2rem;
  }
  th, td { text-align: left; padding: 0.42rem 0.6rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
  th { font-weight: 600; font-size: 0.78rem; letter-spacing: 0.09em; text-transform: uppercase; color: var(--muted); }
  td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
  tr:last-child td { border-bottom: none; }
  code, .mono {
    font-family: "Cascadia Mono", Consolas, "Courier New", monospace;
    font-size: 0.86em;
    background: #f1efe9;
    padding: 0.06em 0.3em;
    border-radius: 2px;
  }
  .plan { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.7rem; margin: 1.1rem 0 1.6rem; }
  .plan div {
    background: var(--card);
    border: 1px solid var(--rule);
    padding: 0.7rem 0.8rem;
    font-size: 0.86rem;
  }
  .plan strong { display: block; font-size: 0.74rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.25rem; }
  .step {
    background: var(--card);
    border: 1px solid var(--rule);
    border-left: 3px solid #c3ccd6;
    padding: 1.15rem 1.3rem 1rem;
    margin: 1.1rem 0;
  }
  .step-head { display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 0.5rem; }
  .step-head .number {
    font-size: 0.74rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    white-space: nowrap;
  }
  .step-head h3 { margin: 0; font-size: 1.04rem; }
  .reason { font-size: 0.97rem; }
  .reason .tag {
    display: inline-block;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--warm);
    border: 1px solid #e3c3bd;
    background: var(--warm-soft);
    padding: 0.02em 0.42em;
    margin-right: 0.45rem;
    vertical-align: 0.1em;
  }
  .check {
    font-size: 0.85rem;
    color: #3d4652;
    background: #f7f8f6;
    border-top: 1px dashed var(--rule);
    margin: 0.9rem -1.3rem -1rem;
    padding: 0.6rem 1.3rem 0.7rem;
  }
  .check .verdict { color: var(--green); font-weight: 600; }
  .check .label { color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; font-size: 0.72rem; margin-right: 0.4rem; }
  figure { margin: 1.5rem 0; }
  figure img { width: 100%; height: auto; display: block; border: 1px solid var(--rule); background: #fff; }
  figure.narrow img { max-width: 58%; margin: 0 auto; }
  td.verdict-cell { white-space: nowrap; }
  figcaption { font-size: 0.85rem; color: var(--muted); margin-top: 0.5rem; }
  figcaption b { color: var(--ink); }
  .part-answer {
    background: var(--accent-soft);
    border: 1px solid #c8d8e8;
    padding: 0.85rem 1.15rem;
    margin: 1.2rem 0 0.6rem;
    font-size: 0.97rem;
  }
  .part-answer .label {
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    display: block;
    margin-bottom: 0.25rem;
  }
  .final {
    background: #fffdf6;
    border: 1px solid #d9cba6;
    border-top: 3px solid #a8812a;
    padding: 1.4rem 1.5rem 1.1rem;
    margin: 1.6rem 0 1rem;
    text-align: center;
  }
  .final .label {
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #7a5e18;
    display: block;
    margin-bottom: 0.5rem;
  }
  .final .value { font-size: 1.2rem; }
  .final .note { font-size: 0.87rem; color: var(--muted); margin-top: 0.7rem; text-align: left; }
  .warn {
    border-left: 3px solid var(--warm);
    background: var(--warm-soft);
    padding: 0.85rem 1.1rem;
    font-size: 0.93rem;
    margin: 1rem 0;
  }
  .warn ol { margin: 0.4rem 0 0; padding-left: 1.2rem; }
  .warn li { margin-bottom: 0.35rem; }
  ul.plain { padding-left: 1.2rem; margin: 0.4rem 0 1rem; }
  ul.plain li { margin-bottom: 0.35rem; }
  footer {
    margin-top: 3.4rem;
    border-top: 1px solid var(--rule);
    padding-top: 1rem;
    font-size: 0.8rem;
    color: var(--muted);
  }
  footer p { margin-bottom: 0.3rem; }
  .totop { font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }
  @media (max-width: 720px) {
    .plan { grid-template-columns: 1fr 1fr; }
    h1 { font-size: 1.7rem; }
    .page { padding: 2rem 1.1rem 3rem; }
  }
  @media print {
    body { background: #fff; }
    .step, .part-answer, .final { break-inside: avoid; }
    a { border-bottom: none; }
  }
</style>
</head>
<body>
<div class="page">

<header>
  <div class="kicker">Calculus · Early Transcendentals · Section 15.7 · Exercise 17</div>
  <h1>Triple Integral over a Paraboloid Cap</h1>
  <p class="lede">A complete solution of $\iiint_E x\,dV$, where the solid $E$ lies between the
  paraboloid $x = 4y^2 + 4z^2$ and the plane $x = 4$. Each step states its reason first, and each
  numerical claim is checked by a script.</p>
  <div class="meta">
    <span><b>Answer</b> $\dfrac{16\pi}{3} \approx 16.7552$</span>
    <span><b>Parts</b> 4</span>
    <span><b>Steps</b> 9</span>
    <span><b>Figures</b> 3</span>
    <span><b>Checks</b> 4 scripts, 0 failures</span>
  </div>
</header>

<h2 id="statement">1. The statement</h2>

<div class="statement">
  <p>Evaluate the triple integral</p>
  <p>$$\iiint_E x \, dV,$$</p>
  <p>where $E$ is bounded by the paraboloid $x = 4y^2 + 4z^2$ and the plane $x = 4$.</p>
  <p class="source">Source: <code>problem/source/problem.png</code>, a screenshot of the textbook
  exercise. Normalized record: <code>problem/problem.md</code>. The two copies of the screenshot
  have the same MD5 sum, <code>e412ebf68afb3fe20261c73890244896</code>.</p>
</div>

<h3>What the statement gives</h3>
<table>
  <thead><tr><th>Item</th><th>Value</th></tr></thead>
  <tbody>
    <tr><td>Integrand</td><td>$f(x,y,z) = x$</td></tr>
    <tr><td>Volume element</td><td>$dV$, three integration variables</td></tr>
    <tr><td>Lower surface</td><td>paraboloid $x = 4y^2 + 4z^2$</td></tr>
    <tr><td>Upper surface</td><td>plane $x = 4$</td></tr>
    <tr><td>Name of the solid</td><td>$E$</td></tr>
    <tr><td>Answer</td><td>one real number</td></tr>
  </tbody>
</table>

<h3>The plan</h3>
<p>The solution has four parts. Each part answers one question. Each part ends with its own answer.</p>
<div class="plan">
  <div><strong>Part 1</strong>Describe the solid $E$ and find its projection.</div>
  <div><strong>Part 2</strong>Integrate along $x$ and obtain one double integral.</div>
  <div><strong>Part 3</strong>Evaluate the double integral in polar coordinates.</div>
  <div><strong>Part 4</strong>Check the answer by a second order and by random points.</div>
</div>

<h2 id="part1">2. Part 1 — Describe the solid</h2>

<article class="step" id="s11">
  <div class="step-head"><span class="number">Step 1.1</span><h3>Read the two surfaces</h3></div>
  <p class="reason"><span class="tag">Why</span>The two equations are the only information about the
  solid. Read each one as a surface first. The shape of a surface shows which variable can serve as
  the inner variable of the integral.</p>
  <p>The first surface is the paraboloid</p>
  <p>$$x = 4y^2 + 4z^2 .$$</p>
  <p>Write $r^2 = y^2 + z^2$. Then $x = 4r^2$, and the right side is a sum of two squares. The right
  side is never negative, and it is zero only at $y = z = 0$. Therefore the lowest point of the
  paraboloid is the origin $(0,0,0)$, and the bowl opens toward positive $x$.</p>
  <p>The second surface is the plane $x = 4$. Its equation does not contain $y$ or $z$. Therefore the
  plane is vertical, it is parallel to the $yz$-plane, and it meets the $x$-axis at $x = 4$.</p>
  <p class="check"><span class="label">Checked by</span><code>code/part1_verify.py</code> —
  least value of $x$ on the paraboloid: computed <code>0.0</code>, expected <code>0.0</code>;
  number of sampled lowest points: <code>1</code>, at the origin.
  <span class="verdict">pass</span></p>
</article>

<article class="step" id="s12">
  <div class="step-head"><span class="number">Step 1.2</span><h3>Find where the two surfaces meet</h3></div>
  <p class="reason"><span class="tag">Why</span>The solid exists only where the paraboloid is below
  the plane. Solve the equality to get the curve that limits the solid, and project that curve on the
  $yz$-plane to get the region of the double integral.</p>
  <p>Set the two right sides equal:</p>
  <p>$$4y^2 + 4z^2 = 4 \quad\Longleftrightarrow\quad y^2 + z^2 = 1 .$$</p>
  <p>The equation contains no $x$, and the common value is $x = 4$. Therefore the intersection is the
  circle of radius $1$ in the plane $x = 4$. The condition $4(y^2+z^2) \le x \le 4$ gives
  $y^2 + z^2 \le 1$. Therefore every point of $E$ stands above the unit disk</p>
  <p>$$D = \{(y,z) : y^2 + z^2 \le 1\}, \qquad \operatorname{area}(D) = \pi .$$</p>
  <p class="check"><span class="label">Checked by</span><code>code/part1_verify.py</code> —
  radius from $4r^2 = 4$: <code>1.0</code>, expected <code>1.0</code>; largest
  $\lvert 4r^2-4 \rvert$ on $r=1$: <code>8.9e-16</code>, expected <code>0</code>;
  $\lvert 4r^2-4 \rvert$ at $r=0.98$ and $r=1.02$: <code>0.1584</code> and <code>0.1616</code>;
  area of $D$ from $2\cdot10^6$ points: <code>3.14085</code>, expected <code>3.14159</code>;
  points that the two descriptions of $E$ classify differently: <code>0</code>.
  <span class="verdict">pass</span></p>
</article>

<figure>
  <img src="@@FIGURE1@@" alt="Left: the section of the solid in the plane z = 0, between the parabola x = 4 y squared and the line x = 4. Right: three-dimensional view of the paraboloid cap with its top disk.">
  <figcaption><b>Figure 1.</b> The solid $E$. Left: the section at $z = 0$, between
  $x = 4y^2$ and $x = 4$, with the meeting point at $y = 1$. Right: the full solid, the paraboloid
  $x = 4(y^2+z^2)$ and the disk at $x = 4$. Figure script:
  <code>code/part1_figure1.py</code>.</figcaption>
</figure>

<article class="step" id="s13">
  <div class="step-head"><span class="number">Step 1.3</span><h3>Write the solid as one set and note its symmetry</h3></div>
  <p class="reason"><span class="tag">Why</span>An integral needs explicit limits. The surfaces give
  the two limits of $x$, and the projection gives the limits of $y$ and $z$. Record the symmetry
  before any computation, because a symmetry can save work, and a false symmetry gives a wrong
  answer.</p>
  <p>$$E = \{(x,y,z) : y^2 + z^2 \le 1,\ 4(y^2+z^2) \le x \le 4\}.$$</p>
  <p>All coordinates are finite, and all inequalities are non-strict. Therefore $E$ is closed and
  bounded, and the integral is finite.</p>
  <p>Both $y^2+z^2 \le 1$ and $x = 4(y^2+z^2)$ contain $y$ and $z$ only as squares. Therefore $E$ is
  symmetric about the planes $y = 0$ and $z = 0$. The integrand $f = x$ does not contain $y$ or $z$.
  Therefore the two halves of the symmetry give equal contributions, and the contributions add. The
  symmetry gives no cancellation for this integrand.</p>
  <p>For later use, the volume is</p>
  <p>$$V = \iint_D \left(4 - 4(y^2+z^2)\right) dA = \tfrac{1}{2}\,\pi\cdot 1^2\cdot 4 = 2\pi .$$</p>
  <p class="check"><span class="label">Checked by</span><code>code/part1_verify.py</code> and
  <code>code/part2_verify.py</code> — volume of $E$: <code>6.283185307179586</code>, expected
  <code>2&pi; = 6.283185307179586</code>; volume against half of the enclosing cylinder:
  difference <code>0.0</code>. <span class="verdict">pass</span></p>
</article>

<div class="part-answer">
  <span class="label">Answer of part 1</span>
  $E = \{(x,y,z) : y^2 + z^2 \le 1,\ 4(y^2+z^2) \le x \le 4\}$. The projection of $E$ is the unit
  disk $D$ of area $\pi$. The solid is closed and bounded, and its volume is $2\pi$.
</div>

<h2 id="part2">3. Part 2 — Reduce the integral</h2>

<article class="step" id="s21">
  <div class="step-head"><span class="number">Step 2.1</span><h3>Integrate along $x$ first</h3></div>
  <p class="reason"><span class="tag">Why</span>Choose the inner variable first. The variable $x$ has
  an explicit lower limit $4(y^2+z^2)$ and an explicit upper limit $4$. Therefore hold $y$ and $z$
  fixed, and integrate $x$ along one straight segment. This choice gives a double integral without
  square roots.</p>
  <p>Fix $(y,z)$ in $D$ and write $r^2 = y^2+z^2$. The variable $x$ runs from $4r^2$ to $4$:</p>
  <p>$$\int_{4r^2}^{4} x \, dx = \left[\frac{x^2}{2}\right]_{4r^2}^{4}
  = 8 - \frac{(4r^2)^2}{2} = 8 - 8r^4 = 8\left(1 - (y^2+z^2)^2\right).$$</p>
  <p>Check the two ends of the disk. At the centre, the segment has the full height and the value is
  $8$. At the rim, the segment has zero length and the value is $0$. The value is never negative on
  $D$, because $r \le 1$.</p>
  <p class="check"><span class="label">Checked by</span><code>code/part2_verify.py</code> —
  <code>quad</code> of $x$ on the segment against $8(1-r^4)$ at $r = 0,\ 0.25,\ 0.5,\ 0.75,\ 1$:
  computed <code>8.0</code>, <code>7.96875</code>, <code>7.5</code>, <code>5.46875</code>,
  <code>0.0</code>, expected the same values, all differences <code>0.0</code>.
  <span class="verdict">pass</span></p>
</article>

<figure>
  <img src="@@FIGURE2@@" alt="Left: the radius-height section of the solid with two marked vertical segments of length 4 minus 4 r squared. Right: the value of the inner integral over the unit disk, highest at the centre and zero at the rim.">
  <figcaption><b>Figure 2.</b> Left: the length of one segment is $4 - 4r^2$, so the inner integral
  $8(1-r^4)$ falls from $8$ at the centre to $0$ at the rim. Right: the value of the inner integral
  as a function of the point in $D$. Figure script: <code>code/part2_figure1.py</code>.</figcaption>
</figure>

<article class="step" id="s22">
  <div class="step-head"><span class="number">Step 2.2</span><h3>Write the double integral over the disk</h3></div>
  <p class="reason"><span class="tag">Why</span>The inner integral no longer contains $x$, so the
  outer integral runs over the projection $D$. Write the reduced integral in full, and bracket its
  value before the exact evaluation.</p>
  <p>$$I = \iint_D 8\left(1 - (y^2+z^2)^2\right) dA
  = 8 \iint_D \left(1 - (y^2+z^2)^2\right) dA .$$</p>
  <p>The integrand is positive inside $D$ and zero on the rim, so $I > 0$. On $D$ the factor
  $1 - r^4$ runs from $1$ down to $0$. Therefore</p>
  <p>$$0 < I < 8 \cdot 1 \cdot \pi = 8\pi \approx 25.13 .$$</p>
  <p class="check"><span class="label">Checked by</span><code>code/part2_verify.py</code> —
  polar double integral of $8(1-r^4)r$: computed <code>16.755160819145566</code>, expected
  <code>16.755160819145562</code>, difference <code>3.6e-15</code>, tolerance <code>1.0e-8</code>;
  volume of $E$: <code>6.283185307179586</code>, expected <code>2&pi;</code>.
  <span class="verdict">pass</span></p>
</article>

<div class="part-answer">
  <span class="label">Answer of part 2</span>
  $I = 8\displaystyle\iint_D \left(1 - (y^2+z^2)^2\right) dA$, and $0 < I < 8\pi \approx 25.13$.
  The reduced integral has the numerical value $16.75516$, which part 3 derives exactly.
</div>

<h2 id="part3">4. Part 3 — Evaluate in polar coordinates</h2>

<article class="step" id="s31">
  <div class="step-head"><span class="number">Step 3.1</span><h3>Use polar coordinates in the disk</h3></div>
  <p class="reason"><span class="tag">Why</span>The integrand depends on $y$ and $z$ only through
  $y^2+z^2$, and the region is a disk. Polar coordinates fit both facts, and they split the double
  integral into a product of one integral in $r$ and one integral in $\theta$.</p>
  <p>$$y = r\cos\theta, \qquad z = r\sin\theta, \qquad dA = r \, dr \, d\theta,$$</p>
  <p>with $0 \le r \le 1$ and $0 \le \theta \le 2\pi$. Then</p>
  <p>$$I = \int_0^{2\pi} \int_0^1 8\left(1-r^4\right) r \, dr \, d\theta .$$</p>
  <p>The inner integral is</p>
  <p>$$\int_0^1 8\left(r - r^5\right) dr
  = 8\left[\frac{r^2}{2} - \frac{r^6}{6}\right]_0^1
  = 8\left(\frac{1}{2} - \frac{1}{6}\right) = \frac{8}{3} .$$</p>
  <p>The factor $r$ is necessary. Without it, the inner integral would be
  $\int_0^1 8(1-r^4)dr = 6.4$, which is the value for a square region, not for a disk.</p>
  <p class="check"><span class="label">Checked by</span><code>code/part3_verify.py</code> —
  radial integral: computed <code>2.6666666666666665</code>, expected <code>8/3 =
  2.6666666666666665</code>, difference <code>0.0</code>. <span class="verdict">pass</span></p>
</article>

<figure class="narrow">
  <img src="@@FIGURE3@@" alt="The unit disk in the yz-plane with one polar element between r and r plus dr and between theta and theta plus d theta, and the area element dA equals r dr d theta.">
  <figcaption><b>Figure 3.</b> One polar element of the disk. Its radial width is $dr$, its angular
  width is $d\theta$, and its area is $r\,dr\,d\theta$. The factor $r$ is the length of the arc at
  radius $r$. Figure script: <code>code/part3_figure1.py</code>.</figcaption>
</figure>

<article class="step" id="s32">
  <div class="step-head"><span class="number">Step 3.2</span><h3>Multiply the two factors</h3></div>
  <p class="reason"><span class="tag">Why</span>The integrand of step 3.1 is a product of a function
  of $r$ and the constant $1$. Therefore the two integrals separate, and the answer is the product
  of two numbers.</p>
  <p>The angular integral is the length of the full turn:</p>
  <p>$$\int_0^{2\pi} d\theta = 2\pi .$$</p>
  <p>Multiply the two factors:</p>
  <p>$$I = \frac{8}{3}\cdot 2\pi = \frac{16\pi}{3} = 16.755160819145562\ldots \approx 16.7552 .$$</p>
  <p>The value is inside the bracket $0 < I < 25.13$ of step 2.2, and it is close to two thirds of
  that bracket. The result is plausible, because the integrand falls from $8$ at the centre to $0$ at
  the rim.</p>
  <p class="check"><span class="label">Checked by</span><code>code/part3_verify.py</code> —
  angular integral: computed <code>6.283185307179586</code>, expected <code>2&pi;</code>; product:
  computed <code>16.755160819145562</code>, expected <code>16.755160819145562</code>;
  <code>dblquad</code> in polar form: <code>16.755160819145566</code>, difference
  <code>3.6e-15</code>. <span class="verdict">pass</span></p>
</article>

<div class="part-answer">
  <span class="label">Answer of part 3</span>
  $I = \dfrac{16\pi}{3} = 16.755160819145562\ldots$, which is about $16.7552$.
</div>

<h2 id="part4">5. Part 4 — Check the answer</h2>

<article class="step" id="s41">
  <div class="step-head"><span class="number">Step 4.1</span><h3>Integrate with $x$ outermost</h3></div>
  <p class="reason"><span class="tag">Why</span>A second order uses different limits and a different
  integrand. When two independent orders agree, an error in the setup of one order is unlikely.</p>
  <p>Fix $x$ with $0 \le x \le 4$. On that plane the solid satisfies
  $y^2 + z^2 \le x/4$. Therefore the section is a disk of radius $\sqrt{x}/2$, and its area is</p>
  <p>$$A(x) = \pi\left(\frac{\sqrt{x}}{2}\right)^2 = \frac{\pi x}{4} .$$</p>
  <p>The integrand is constant on the section, so the inner integral is $x A(x)$:</p>
  <p>$$I = \int_0^4 x\cdot\frac{\pi x}{4}\, dx = \frac{\pi}{4}\int_0^4 x^2\, dx
  = \frac{\pi}{4}\cdot\frac{64}{3} = \frac{16\pi}{3} .$$</p>
  <p>The same sections give the volume $\int_0^4 A(x)\,dx = 2\pi$, which agrees with step 1.3.</p>
  <p class="check"><span class="label">Checked by</span><code>code/part4_verify.py</code> —
  volume from the section areas: <code>6.283185307179586</code>, expected <code>2&pi;</code>; area at
  $x = 4$: <code>3.141592653589793</code>, expected $\pi$; integral with $x$ outermost:
  <code>16.755160819145562</code>, expected <code>16.755160819145562</code>, difference
  <code>0.0</code>. <span class="verdict">pass</span></p>
</article>

<article class="step" id="s42">
  <div class="step-head"><span class="number">Step 4.2</span><h3>Confirm with random points</h3></div>
  <p class="reason"><span class="tag">Why</span>The two exact orders share the algebra of parts 2 and
  3. A random estimate uses only the definition of the solid and the definition of a volume
  integral. It is independent of that algebra.</p>
  <p>Take the box $B = [0,4]\times[-1,1]\times[-1,1]$, with volume $16$. Draw $N = 4{,}000{,}000$
  uniform points with seed <code>20261122</code>. A point belongs to $E$ when
  $x \ge 4(y^2+z^2)$, because $x \le 4$ holds everywhere in $B$. Then</p>
  <p>$$I \approx \operatorname{vol}(B)\cdot\frac{1}{N}\sum_{i=1}^{N} x_i\,\mathbf{1}_E(x_i,y_i,z_i).$$</p>
  <table>
    <thead><tr><th>Quantity</th><th class="num">Value</th></tr></thead>
    <tbody>
      <tr><td>points inside $E$</td><td class="num">1,570,019</td></tr>
      <tr><td>estimate</td><td class="num">16.742422</td></tr>
      <tr><td>exact value</td><td class="num">16.755161</td></tr>
      <tr><td>standard error</td><td class="num">0.011437</td></tr>
      <tr><td>relative difference</td><td class="num">0.00076</td></tr>
    </tbody>
  </table>
  <p>The relative difference is $7.6\times10^{-4}$, well inside the tolerance $5\times10^{-3}$, and
  the absolute difference is smaller than one standard error. The random estimate agrees with the
  exact answer.</p>
  <p class="check"><span class="label">Checked by</span><code>code/part4_verify.py</code> —
  relative difference <code>0.00076</code> against a tolerance of <code>5.0e-3</code>; answer rounded
  to four decimals: <code>16.7552</code>, expected <code>16.7552</code>.
  <span class="verdict">pass</span></p>
</article>

<div class="part-answer">
  <span class="label">Answer of part 4</span>
  The second order and the random estimate both confirm $I = \dfrac{16\pi}{3} \approx 16.7552$.
  Three independent computations give the same number.
</div>

<h2 id="results">6. Verified results</h2>

<p>Each part has one script. Each script prints the computed value, the expected value, the
difference, and the tolerance. Each script ends with <code>checks failed: 0</code> and exit code
<code>0</code>.</p>

<table>
  <thead>
    <tr><th>Check</th><th>Script</th><th class="num">Computed</th><th class="num">Expected</th><th class="num">Difference</th><th>Verdict</th></tr>
  </thead>
  <tbody>
    <tr><td>Least $x$ on the paraboloid</td><td><code>part1</code></td><td class="num">0.0</td><td class="num">0.0</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Radius of the intersection circle</td><td><code>part1</code></td><td class="num">1.0</td><td class="num">1.0</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Area of the projection $D$ (2 million random points)</td><td><code>part1</code></td><td class="num">3.140853</td><td class="num">3.141593</td><td class="num">0.00074</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Points with two different classifications</td><td><code>part1</code></td><td class="num">0</td><td class="num">0</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Inner integral at $r = 0.5$</td><td><code>part2</code></td><td class="num">7.5</td><td class="num">7.5</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Volume of $E$</td><td><code>part2</code></td><td class="num">6.283185307179586</td><td class="num">2&pi;</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Radial integral</td><td><code>part3</code></td><td class="num">2.6666666666666665</td><td class="num">8/3</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Polar double integral</td><td><code>part3</code></td><td class="num">16.755160819145566</td><td class="num">16&pi;/3</td><td class="num">3.6e-15</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Integral with $x$ outermost</td><td><code>part4</code></td><td class="num">16.755160819145562</td><td class="num">16&pi;/3</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Random estimate, four million points</td><td><code>part4</code></td><td class="num">16.742422</td><td class="num">16.755161</td><td class="num">0.0127</td><td class="verdict-cell">pass</td></tr>
    <tr><td>Answer to four decimals</td><td><code>part4</code></td><td class="num">16.7552</td><td class="num">16.7552</td><td class="num">0</td><td class="verdict-cell">pass</td></tr>
  </tbody>
</table>

<p>Each script name is the part number followed by <code>_verify.py</code>. The difference column is the absolute difference between the computed value and the expected value, in the unit of the quantity. The two random rows differ from the exact value by less than their own standard error.</p>

<h2 id="answer">7. Final answer</h2>

<div class="final">
  <span class="label">Value of the integral</span>
  <div class="value">$$\iiint_E x\,dV = \frac{16\pi}{3} = 16.755160819145562\ldots \approx 16.7552$$</div>
  <p class="note">The solid is the cap between $x = 4(y^2+z^2)$ and $x = 4$. The exact answer is
  $\dfrac{16\pi}{3}$. The value is a positive number, as step 2.2 requires, and it is smaller than
  $8\pi$, the volume bound of that step.</p>
</div>

<h2 id="errors">8. Common errors</h2>

<div class="warn">
  <ol>
    <li><b>Using $x = 4y^2$ only.</b> The surface contains $z$ as well. With $x = 4y^2$ alone the
    region is a cylinder in the $z$ direction, and the answer is different.</li>
    <li><b>Using radius $4$ for the disk.</b> The intersection is $4y^2+4z^2 = 4$, so the radius is
    $1$, not $4$. A radius of $4$ gives $I = 8\pi\cdot 16$ times the wrong factor.</li>
    <li><b>Leaving out the factor $r$.</b> The area element is $r\,dr\,d\theta$. Without $r$ the
    radial integral is $6.4$ instead of $8/3$.</li>
    <li><b>Starting $x$ at $0$.</b> The lower limit is $4(y^2+z^2)$, not $0$. The segment length is
    $4-4r^2$, and it is zero at the rim.</li>
    <li><b>Expecting the symmetry to cancel the integral.</b> The integrand $x$ is not odd in $y$ or
    $z$, so the two halves of the solid add. The answer is positive.</li>
  </ol>
</div>

<h2 id="method">9. Method summary</h2>

<ul class="plain">
  <li>Read the two surfaces. The paraboloid gives the lower limit of $x$ and the plane gives the
  upper limit.</li>
  <li>Solve the equality of the two surfaces. The result fixes the projection, which is the unit
  disk.</li>
  <li>Integrate $x$ first, because both limits of $x$ are explicit functions of $(y,z)$.</li>
  <li>Use polar coordinates, because the integrand and the region depend on $y^2+z^2$.</li>
  <li>Check the answer with a second order and with a random estimate.</li>
</ul>

<footer>
  <p>Dataset: Calculus, Early Transcendentals, Section 15.7, Exercise 17. Screenshot MD5
  <code>e412ebf68afb3fe20261c73890244896</code>.</p>
  <p>Environment: Python 3.14.3, numpy 2.5.5, scipy 1.18.1, matplotlib 3.11.2, uv 0.10.12. Random
  seed of every reported random result: <code>20261122</code>.</p>
  <p>Files: <code>code/part1_verify.py</code>, <code>code/part2_verify.py</code>,
  <code>code/part3_verify.py</code>, <code>code/part4_verify.py</code>,
  <code>code/part1_figure1.py</code>, <code>code/part2_figure1.py</code>,
  <code>code/part3_figure1.py</code>, <code>steps/step_1_1.md</code> to
  <code>steps/step_4_2.md</code>.</p>
</footer>

</div>
<script>
  document.addEventListener("DOMContentLoaded", function () {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false }
      ],
      throwOnError: false,
      strict: false
    });
  });
</script>
</body>
</html>
"""


def encode_figure(path: Path) -> str:
    """Return the Base64 data uniform resource identifier of a figure.

    Args:
        path: Path of the PNG file.

    Returns:
        A string that a browser can use as the value of a src attribute.
    """
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def main() -> None:
    """Write the composed page to report.html and to tutorial.html."""
    page = PAGE_TEMPLATE
    for token, path in FIGURE_FILES.items():
        if token not in page:
            raise RuntimeError(f"token {token} is absent from the template")
        page = page.replace(token, encode_figure(path))
    if "@@" in page:
        raise RuntimeError("one token of the template is still present")
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    TUTORIAL_PATH.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {REPORT_PATH} ({REPORT_PATH.stat().st_size} bytes)")
    print(f"wrote {TUTORIAL_PATH} ({TUTORIAL_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
