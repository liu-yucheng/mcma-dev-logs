"""Compose `report.html` from the step files, the figure files, and the recorded checks.

The composer reads one Markdown file for each step under `steps/`, one figure for each part under
`code/figures/`, and one JSON record for each part under `code/results/`.  It writes the page
`report.html` at the root of the problem workspace.  Each figure is embedded as a Base64 data
uniform resource identifier, so the page needs no other file.

Run this script with the interpreter of `code/.venv`.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

STEPS_DIRECTORY = WORKSPACE / "steps"
"""Directory of the step files."""

FIGURES_DIRECTORY = WORKSPACE / "code" / "figures"
"""Directory of the figure files."""

RESULTS_DIRECTORY = WORKSPACE / "code" / "results"
"""Directory of the recorded checks."""

REPORT_PATH = WORKSPACE / "report.html"
"""Path of the composed page."""

TUTORIAL_PATH = WORKSPACE / "tutorial.html"
"""Path of the same page under the tutorial name of the stage brief."""

PART_TITLES = {
    1: "The solid and its volume",
    2: "The section at a fixed x: two orders",
    3: "The section at a fixed y: two orders",
    4: "The section at a fixed z: two orders",
    5: "The six orders agree on one function",
    6: "Why there are exactly six orders",
}
"""Title of each part."""

PART_STEP_COUNTS = {1: 3, 2: 3, 3: 3, 4: 3, 5: 2, 6: 2}
"""Number of steps of each part."""

PART_FIGURES = {
    1: ("part1_figure1.png", "The solid, the section at x = 0, and the projection on the plane z = 0."),
    2: ("part2_figure1.png", "Two directions of strips on the same disk: the inner integral in z, "
                             "and the inner integral in y."),
    3: ("part3_figure1.png", "The section at a fixed y is a rectangle whose height is the chord of "
                             "the disk."),
    4: ("part4_figure1.png", "The section at a fixed z is the same rectangle, with y and z exchanged."),
}
"""Figure file and caption of each part."""

PART_ANSWERS = {
    1: (
        "The solid is $E=\\{(x,y,z): -2\\leq x\\leq 2,\\ y^2+z^2\\leq 9\\}$, and its volume is "
        "$36\\pi$. The projection on the plane $x=0$ is the disk $y^2+z^2\\leq 9$, and the "
        "projection on the plane $z=0$ is the rectangle $[-2,2]\\times[-3,3]$."
    ),
    2: (
        "$\\displaystyle\\int_{-2}^{2}\\int_{-3}^{3}\\int_{-\\sqrt{9-y^2}}^{\\sqrt{9-y^2}}"
        "f\\,dz\\,dy\\,dx$ and "
        "$\\displaystyle\\int_{-2}^{2}\\int_{-3}^{3}\\int_{-\\sqrt{9-z^2}}^{\\sqrt{9-z^2}}"
        "f\\,dy\\,dz\\,dx$."
    ),
    3: (
        "$\\displaystyle\\int_{-3}^{3}\\int_{-2}^{2}\\int_{-\\sqrt{9-y^2}}^{\\sqrt{9-y^2}}"
        "f\\,dz\\,dx\\,dy$ and "
        "$\\displaystyle\\int_{-3}^{3}\\int_{-\\sqrt{9-y^2}}^{\\sqrt{9-y^2}}\\int_{-2}^{2}"
        "f\\,dx\\,dz\\,dy$."
    ),
    4: (
        "$\\displaystyle\\int_{-3}^{3}\\int_{-2}^{2}\\int_{-\\sqrt{9-z^2}}^{\\sqrt{9-z^2}}"
        "f\\,dy\\,dx\\,dz$ and "
        "$\\displaystyle\\int_{-3}^{3}\\int_{-\\sqrt{9-z^2}}^{\\sqrt{9-z^2}}\\int_{-2}^{2}"
        "f\\,dx\\,dy\\,dz$."
    ),
    5: (
        "All six orders give $198\\pi\\approx 622.035345$ for $f=1+x+y^2+z^2$, and all six give "
        "$36\\pi$ for $f=1$. The largest difference between two orders is "
        "$3.4\\times10^{-13}$."
    ),
    6: (
        "There are $3!=6$ orders. One bound rule produces all six: $x$ always runs over $[-2,2]$, "
        "and the variable of the pair $y,z$ that is integrated first takes the cylinder bound."
    ),
}
"""Final answer of each part."""

STYLE = """
:root {
  --ink: #1f2933;
  --muted: #52606d;
  --line: #d9e2ec;
  --accent: #1f3b57;
  --wash: #f5f8fb;
}
html { font-size: 17px; }
body {
  margin: 0 auto;
  max-width: 60rem;
  padding: 2.6rem 1.6rem 4rem;
  font-family: Cambria, "Cambria Math", Georgia, serif;
  color: var(--ink);
  line-height: 1.62;
  background: #ffffff;
}
h1 { font-size: 1.85rem; line-height: 1.24; margin: 0 0 0.4rem; letter-spacing: -0.01em; }
h2 {
  font-size: 1.3rem;
  margin: 2.6rem 0 0.9rem;
  padding-bottom: 0.35rem;
  border-bottom: 2px solid var(--accent);
}
h3 { font-size: 1.05rem; margin: 1.8rem 0 0.5rem; color: var(--accent); }
p { margin: 0.55rem 0; }
.lede { color: var(--muted); font-size: 1.02rem; margin-bottom: 1.6rem; }
.lede code, .muted { color: var(--muted); }
.statement {
  background: var(--wash);
  border-left: 3px solid var(--accent);
  padding: 1rem 1.2rem;
  margin: 1.2rem 0 1.8rem;
}
.label {
  font-variant: small-caps;
  letter-spacing: 0.06em;
  font-size: 0.82rem;
  color: var(--muted);
  display: block;
  margin-bottom: 0.2rem;
}
.step { margin: 1.4rem 0 1.8rem; }
.display { overflow-x: auto; margin: 0.9rem 0; }
.answer {
  background: #eef4fa;
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  padding: 0.85rem 1.1rem;
  margin: 1.4rem 0 0.6rem;
}
.check { background: var(--wash); border: 1px solid var(--line); padding: 0.55rem 0.9rem;
         font-size: 0.95rem; }
figure { margin: 1.6rem 0; }
figure img { width: 100%; height: auto; border: 1px solid var(--line); }
figcaption { font-size: 0.9rem; color: var(--muted); margin-top: 0.45rem; }
table { border-collapse: collapse; width: 100%; font-size: 0.86rem; margin: 0.9rem 0 1.4rem; }
th, td { border-bottom: 1px solid var(--line); padding: 0.34rem 0.5rem; text-align: left; }
th { background: var(--wash); font-weight: 600; }
td.number { font-family: "XITS Math", "Cambria Math", Consolas, monospace; text-align: right; }
code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 0.9em;
  background: #eef2f7;
  padding: 0.06em 0.32em;
  border-radius: 3px;
  color: #243b53;
}
.katex { font-family: "XITS Math", "Cambria Math", serif; }
"""


def render_inline(text: str) -> str:
    """Render the inline Markdown of one paragraph: bold text and inline code."""
    text = re.sub(r"`([^`]+)`", lambda match: f"<code>{match.group(1)}</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", lambda match: f"<strong>{match.group(1)}</strong>", text)
    return text


def render_prose(prose_text: str) -> list[str]:
    """Render the prose part of a step file: headings and paragraphs.

    Args:
        prose_text: Text that holds no display math.

    Returns:
        The HTML blocks of the prose part.
    """
    output: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append("<p>" + render_inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    for raw_line in prose_text.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            continue
        if line.startswith("### "):
            flush_paragraph()
            output.append("<h3>" + render_inline(line[4:]) + "</h3>")
            continue
        paragraph.append(line)
    flush_paragraph()
    return output


def render_step(step_text: str) -> str:
    """Render one step file as HTML.

    A display expression starts and ends with a `$$` pair.  One display may span several lines, so
    the split on `$$` is the only reliable separator; a line-based scan loses the closing pair.

    Args:
        step_text: The Markdown content of the step file.

    Returns:
        The HTML of the step.
    """
    segments = step_text.split("$$")
    if len(segments) % 2 == 0:
        raise AssertionError("one step file holds an unpaired display delimiter")
    output: list[str] = []
    for index, segment in enumerate(segments):
        if index % 2 == 1:
            body = " ".join(part.strip() for part in segment.splitlines() if part.strip())
            if body:
                output.append('<div class="display">$$' + body + "$$</div>")
            continue
        output.extend(render_prose(segment))
    return "\n".join(output)


def figure_markup(file_name: str, caption: str) -> str:
    """Return the HTML of one figure with its image embedded as a Base64 data identifier."""
    payload = base64.b64encode((FIGURES_DIRECTORY / file_name).read_bytes()).decode("ascii")
    return (
        "<figure>\n"
        f'<img alt="{caption}" src="data:image/png;base64,{payload}">\n'
        f"<figcaption>{caption}</figcaption>\n"
        "</figure>"
    )


def format_number(value: float) -> str:
    """Return a short decimal form of one recorded number."""
    if value == 0.0:
        return "0"
    magnitude = abs(value)
    if magnitude >= 1e-3:
        return f"{value:.12g}"
    return f"{value:.3e}"


def results_table(part_number: int) -> str:
    """Return the HTML table of the recorded checks of one part."""
    path = RESULTS_DIRECTORY / f"part{part_number}_results.json"
    if not path.exists():
        return ""
    records = json.loads(path.read_text(encoding="utf-8"))
    rows = [
        "<table>",
        "<thead><tr><th>Check</th><th>Computed</th><th>Expected</th>"
        "<th>Difference</th><th>Tolerance</th></tr></thead>",
        "<tbody>",
    ]
    for record in records:
        rows.append(
            "<tr>"
            f"<td>{render_inline(record['label'])}</td>"
            f"<td class=\"number\">{format_number(record['computed'])}</td>"
            f"<td class=\"number\">{format_number(record['expected'])}</td>"
            f"<td class=\"number\">{format_number(record['difference'])}</td>"
            f"<td class=\"number\">{format_number(record['tolerance'])}</td>"
            "</tr>"
        )
    rows.append("</tbody></table>")
    return "\n".join(rows)


def build_page() -> str:
    """Return the HTML text of the composed page."""
    parts: list[str] = []

    for part_number, title in PART_TITLES.items():
        steps_html: list[str] = []
        for step_number in range(1, PART_STEP_COUNTS[part_number] + 1):
            path = STEPS_DIRECTORY / f"part{part_number}_step{step_number}.md"
            steps_html.append('<div class="step">\n'
                              + render_step(path.read_text(encoding="utf-8"))
                              + "\n</div>")

        figure_html = ""
        if part_number in PART_FIGURES:
            file_name, caption = PART_FIGURES[part_number]
            figure_html = figure_markup(file_name, f"Figure {part_number}. {caption}")

        parts.append(
            f'<section class="part" id="part{part_number}">\n'
            f"<h2>Part {part_number}. {title}</h2>\n"
            + "\n".join(steps_html)
            + "\n"
            + figure_html
            + "\n"
            + results_table(part_number)
            + "\n"
            + f'<div class="answer"><span class="label">Final answer of Part {part_number}</span>'
            + PART_ANSWERS[part_number]
            + "</div>\n</section>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Six orders for one triple integral: Stewart 15.7 Exercise 30</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>{STYLE}</style>
</head>
<body>
<header>
<span class="label">Stewart, Calculus: Early Transcendentals &middot; Section 15.7 &middot; Exercise 30</span>
<h1>Six orders for one triple integral</h1>
<p class="lede">A tutorial that writes $\\iiint_E f(x,y,z)\\,dV$ in six ways, and checks every
bound of every order with a script that the page cites.</p>
</header>

<section id="statement">
<h2>The statement</h2>
<div class="statement">
<p>Express the integral $\\displaystyle\\iiint_E f(x,y,z)\\,dV$ as an iterated integral in six
different ways, where $E$ is the solid bounded by the given surfaces.</p>
<div class="display">$$y^2+z^2=9,\\qquad x=-2,\\qquad x=2$$</div>
</div>
<p>The integrand $f$ is a general continuous function, so the answer is a list of six limit sets,
not one number. The page therefore checks two things: the volume and the sections of $E$, which are
numbers, and the agreement of the six orders on one chosen function.</p>
</section>

<section id="summary">
<h2>How the solution is organised</h2>
<p>Part 1 reads the region and measures it. Parts 2, 3, and 4 group the orders by the outer
variable: $x$ outermost, $y$ outermost, and $z$ outermost. Part 5 puts one function through all six
orders. Part 6 counts the orders and states the single rule that produces every bound.</p>
<p>Every computation of this page has a script under <code>code/</code>, and every table of this
page is the printed output of one script. Each check compares a value that one method computes with
a value that a different method computes.</p>
</section>

{"".join(parts)}

<section id="answers">
<h2>All six answers in one place</h2>
<p>With $f=f(x,y,z)$, the six orders are</p>
<div class="display">$$\\int_{{-2}}^{{2}}\\int_{{-3}}^{{3}}\\int_{{-\\sqrt{{9-y^2}}}}^{{\\sqrt{{9-y^2}}}}f\\,dz\\,dy\\,dx,\\qquad \\int_{{-2}}^{{2}}\\int_{{-3}}^{{3}}\\int_{{-\\sqrt{{9-z^2}}}}^{{\\sqrt{{9-z^2}}}}f\\,dy\\,dz\\,dx,$$</div>
<div class="display">$$\\int_{{-3}}^{{3}}\\int_{{-2}}^{{2}}\\int_{{-\\sqrt{{9-y^2}}}}^{{\\sqrt{{9-y^2}}}}f\\,dz\\,dx\\,dy,\\qquad \\int_{{-3}}^{{3}}\\int_{{-\\sqrt{{9-y^2}}}}^{{\\sqrt{{9-y^2}}}}\\int_{{-2}}^{{2}}f\\,dx\\,dz\\,dy,$$</div>
<div class="display">$$\\int_{{-3}}^{{3}}\\int_{{-2}}^{{2}}\\int_{{-\\sqrt{{9-z^2}}}}^{{\\sqrt{{9-z^2}}}}f\\,dy\\,dx\\,dz,\\qquad \\int_{{-3}}^{{3}}\\int_{{-\\sqrt{{9-z^2}}}}^{{\\sqrt{{9-z^2}}}}\\int_{{-2}}^{{2}}f\\,dx\\,dy\\,dz.$$</div>
<div class="answer"><span class="label">Final answer</span>
These six iterated integrals are the answer to the exercise.</div>
</section>

<script>
document.addEventListener("DOMContentLoaded", function () {{
  renderMathInElement(document.body, {{
    delimiters: [
      {{left: "$$", right: "$$", display: true}},
      {{left: "$", right: "$", display: false}}
    ],
    throwOnError: false
  }});
}});
</script>
</body>
</html>
"""


def main() -> None:
    """Compose the page, then check it for control characters and empty code elements."""
    page = build_page()
    REPORT_PATH.write_text(page, encoding="utf-8")
    TUTORIAL_PATH.write_text(page, encoding="utf-8")
    control_characters = [character for character in page
                          if ord(character) < 32 and character not in "\n\t"]
    empty_code = page.count("<code></code>")
    print(f"wrote {REPORT_PATH} ({len(page)} characters)")
    print(f"wrote {TUTORIAL_PATH} ({len(page)} characters)")
    print(f"control characters other than newline and tab: {len(control_characters)}")
    print(f"empty inline code elements: {empty_code}")
    if control_characters:
        raise AssertionError("the composed page holds a control character")
    if empty_code:
        raise AssertionError("the composed page holds an empty inline code element")


if __name__ == "__main__":
    main()
