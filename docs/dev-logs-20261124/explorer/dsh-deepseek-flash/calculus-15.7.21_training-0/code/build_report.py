"""Compose the tutorial page of the session from the step files.

The script reads every step file below ``steps/`` in file name order, converts the
Markdown subset that the step files use to HTML, inserts the two figures as Base64
data uniform resource identifiers, and writes ``report.html`` at the workspace root.

Run this script with: code/.venv/Scripts/python.exe code/build_report.py
"""

from __future__ import annotations

import base64
import html
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
"""Root directory of the problem workspace."""

STEPS_DIRECTORY = WORKSPACE / "steps"
"""Directory that holds one Markdown file for each step."""

FIGURES_DIRECTORY = WORKSPACE / "code" / "figures"
"""Directory that holds one portable network graphic for each figure."""

REPORT_PATH = WORKSPACE / "report.html"
"""Path of the composed tutorial page."""

FIGURE_WIDTH_3D = "920"
"""Display width in pixels of the solid figure."""

FIGURE_WIDTH_PANELS = "1080"
"""Display width in pixels of the three panel figure."""

PART_TITLES = {
    1: "Part 1. What the solid is",
    2: "Part 2. The shadow and the vertical column",
    3: "Part 3. The slice at a fixed x",
    4: "Part 4. The volume and its checks",
}
"""Heading of each part of the solution."""

PART_ANSWERS = {
    1: (
        "The solid is the closed set $y \\geq x^{2}$, $z \\geq 0$, $y + z \\leq 1$. "
        "It lies inside the box $-1 \\leq x \\leq 1$, $0 \\leq y \\leq 1$, $0 \\leq z \\leq 1$, "
        "whose volume is $2$."
    ),
    2: (
        "The shadow is $D = \\{(x, y) : -1 \\leq x \\leq 1,\\; x^{2} \\leq y \\leq 1\\}$ and the "
        "column height is $1 - y$, so "
        "$V = \\int_{-1}^{1} \\int_{x^{2}}^{1} \\int_{0}^{1 - y} dz\\, dy\\, dx$."
    ),
    3: (
        "The slice at $x = a$ is a right isosceles triangle with both legs $1 - a^{2}$, so "
        "$A(a) = \\frac{(1 - a^{2})^{2}}{2}$. The largest slice has area $0.5$ at $a = 0$, and the "
        "slice closes to a point at $a = \\pm 1$."
    ),
    4: (
        "The volume is $V = \\frac{8}{15} = 0.533333\\ldots$ cubic units. "
        "Five independent methods give the same value."
    ),
}
"""Answer of each part of the solution."""

FIGURES_AFTER_HEADING = {
    "Part 1. What the solid is": [
        ("part1_figure1.png", FIGURE_WIDTH_3D,
         "The solid with the cylinder $y = x^{2}$ as its wall, the plane $z = 0$ as its floor, "
         "and the plane $y + z = 1$ as its roof. The dashed line is the sharp edge at $y = 1$, "
         "where the floor meets the roof. The red triangle is the slice at $x = 0.5$."),
    ],
    "Part 3. The slice at a fixed x": [
        ("part3_figure2.png", FIGURE_WIDTH_PANELS,
         "Left: the shadow $D$ in the $xy$ plane. Middle: the slice at $x = 0.5$, a right triangle "
         "with both legs $0.75$. Right: the slice area $A(x)$ over the whole $x$ range, with values "
         "at $x = 0$, $x = 0.5$, and $x = 0.9$."),
    ],
}
"""Figures that belong to a part, with their display width and their caption."""

VERIFIED_RESULTS = [
    ("Part 1", "Membership of the five points on the boundary", "1 at each point", "1", "PASS"),
    ("Part 1", "Membership of the four points just outside", "0 at each point", "0", "PASS"),
    ("Part 1", "Disagreement between the two descriptions", "0 of 200000", "0", "PASS"),
    ("Part 1", "Volume of the bounding box", "2", "2", "PASS"),
    ("Part 2", "Smallest and largest admissible $y$ at $x = 0.6$", "0.36 and 0.99999", "0.36 and 1", "PASS"),
    ("Part 2", "Smallest roof height on the shadow", "0", "0", "PASS"),
    ("Part 2", "Largest $x$ at $y = 0.9998$", "0.99989", "0.999899994999", "PASS"),
    ("Part 3", "Corners of the sampled slice at three abscissas", "3", "3", "PASS"),
    ("Part 3", "Area at $x = 0$, by rejection sample", "0.4999255", "0.5", "PASS"),
    ("Part 3", "Area at $x = 0.5$, by rejection sample", "0.28100221875", "0.28125", "PASS"),
    ("Part 3", "Area at $x = 0.9$, by rejection sample", "0.018048917", "0.01805", "PASS"),
    ("Part 3", "Largest slice area, and its abscissa", "0.5 at 0", "0.5 at 0", "PASS"),
    ("Part 4", "Antiderivative, exact rational arithmetic", "0.533333333333333", "$8/15$", "PASS"),
    ("Part 4", "Two dimensional quadrature over the shadow", "0.533333333333333", "$8/15$", "PASS"),
    ("Part 4", "Quadrature of the slices at a fixed $y$", "0.533333333333333", "$8/15$", "PASS"),
    ("Part 4", "Trapezoid rule on 1600000 intervals", "0.533333333333333", "$8/15$", "PASS"),
    ("Part 4", "Rejection sample of the bounding box", "0.5334815", "$8/15$", "PASS"),
    ("Part 4", "Inner box is a subset of the solid", "1", "1", "PASS"),
    ("Part 4", "Volume above the inner box of volume 0.125", "0.533333333333333", "$V > 0.125$", "PASS"),
    ("Part 4", "Volume below the shadow area times height 1", "0.533333333333333", "$V < 1.333$", "PASS"),
]
"""One row for each check that a verification script printed, with its verdict."""

MATH_OR_CODE = re.compile(r"(\$\$.+?\$\$|\$.+?\$|`[^`]+`)")
"""Pattern that splits one line into plain text, mathematics, and inline code."""

INLINE_CODE = re.compile(r"`([^`]+)`")
"""Pattern of one inline code span."""

NUMBERED_ITEM = re.compile(r"^(\d+)\.\s+(.*)$")
"""Pattern of one item of an ordered list."""

HEADING = re.compile(r"^(#{1,3})\s+(.*)$")
"""Pattern of one Markdown heading."""


def escape_plain_text(text: str) -> str:
    """Escape one plain text fragment for HTML, and keep mathematics unchanged.

    Args:
        text: Fragment of a line that holds no mathematics and no inline code.

    Returns:
        The fragment as HTML text.
    """
    return html.escape(text, quote=False)


def render_inline(text: str) -> str:
    """Convert one line of Markdown to HTML, and keep mathematics for KaTeX.

    Args:
        text: One line of a step file.

    Returns:
        The line as HTML, with inline code in a code element.
    """
    pieces: list[str] = []
    for fragment in MATH_OR_CODE.split(text):
        if not fragment:
            continue
        if fragment.startswith("$") or fragment.startswith("`"):
            code = INLINE_CODE.fullmatch(fragment)
            if code is not None:
                pieces.append(f"<code>{html.escape(code.group(1), quote=False)}</code>")
            else:
                pieces.append(fragment)
        else:
            pieces.append(escape_plain_text(fragment))
    return "".join(pieces)


def convert_step(markdown: str) -> str:
    """Convert the Markdown subset of one step file to HTML.

    The converter supports headings, paragraphs, unordered lists, ordered lists,
    quoted blocks, display mathematics, inline mathematics, and inline code.

    Args:
        markdown: Complete text of one step file.

    Returns:
        The step as HTML.
    """
    lines = markdown.replace("\r\n", "\n").split("\n")
    blocks: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None
    list_items: list[str] = []

    def close_paragraph() -> None:
        """Flush the paragraph buffer into the block list."""
        if paragraph:
            text = " ".join(item.strip() for item in paragraph)
            if text.startswith("$$") and text.endswith("$$"):
                blocks.append(f'<div class="display-math">{text}</div>')
            else:
                blocks.append(f"<p>{render_inline(text)}</p>")
            paragraph.clear()

    def close_list() -> None:
        """Flush the list buffer into the block list."""
        nonlocal list_kind
        if list_kind is not None:
            tag = "ul" if list_kind == "unordered" else "ol"
            body = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            blocks.append(f"<{tag}>{body}</{tag}>")
            list_items.clear()
            list_kind = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            close_paragraph()
            close_list()
            continue
        heading = HEADING.match(stripped)
        if heading is not None:
            close_paragraph()
            close_list()
            level = len(heading.group(1)) + 1
            blocks.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            continue
        if stripped.startswith("> "):
            close_paragraph()
            close_list()
            blocks.append(f'<blockquote><p>{render_inline(stripped[2:])}</p></blockquote>')
            continue
        if stripped.startswith("- "):
            close_paragraph()
            if list_kind not in (None, "unordered"):
                close_list()
            list_kind = "unordered"
            list_items.append(stripped[2:])
            continue
        numbered = NUMBERED_ITEM.match(stripped)
        if numbered is not None:
            close_paragraph()
            if list_kind not in (None, "ordered"):
                close_list()
            list_kind = "ordered"
            list_items.append(numbered.group(2))
            continue
        if list_kind is not None:
            close_list()
        paragraph.append(stripped)
    close_paragraph()
    close_list()
    return "\n".join(blocks)


def data_uri(path: Path) -> str:
    """Build a Base64 data uniform resource identifier for one figure.

    Args:
        path: Path of a portable network graphic.

    Returns:
        The data uniform resource identifier of the image.
    """
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def render_figure(file_name: str, width: str, caption: str) -> str:
    """Render one figure as a figure element with a Base64 image.

    Args:
        file_name: Name of the image below the figure directory.
        width: Display width in pixels.
        caption: Caption of the figure, in the language of the page.

    Returns:
        The figure as HTML.
    """
    source = data_uri(FIGURES_DIRECTORY / file_name)
    return (
        f'<figure><img src="{source}" width="{width}" '
        f'alt="{html.escape(caption, quote=True)}">'
        f"<figcaption>{render_inline(caption)}</figcaption></figure>"
    )


def read_step_files() -> list[tuple[int, str, str]]:
    """Read every step file, and group the files by part.

    Returns:
        One tuple for each step file: the part number, the step number, and the HTML.
    """
    steps: list[tuple[int, str, str]] = []
    for path in sorted(STEPS_DIRECTORY.glob("part*_step*.md")):
        match = re.fullmatch(r"part(\d)_step(\d+)\.md", path.name)
        if match is None:
            raise SystemExit(f"unexpected step file name: {path.name}")
        steps.append((int(match.group(1)), match.group(2), convert_step(path.read_text(encoding="utf-8"))))
    if not steps:
        raise SystemExit("no step file found")
    return steps


def render_part(part: int, steps: list[tuple[int, str, str]]) -> str:
    """Render one part of the solution with its steps, its figure, and its answer.

    Args:
        part: Number of the part.
        steps: Step tuples of this part, in step number order.

    Returns:
        The part as HTML.
    """
    title = PART_TITLES[part]
    pieces = [f'<section class="part"><h2>{html.escape(title, quote=False)}</h2>']
    for figure in FIGURES_AFTER_HEADING.get(title, []):
        pieces.append(render_figure(*figure))
    for _, _, body in steps:
        pieces.append(body)
    pieces.append(
        '<div class="answer"><strong>Answer of ' + f"Part {part}.</strong> "
        + render_inline(PART_ANSWERS[part]) + "</div>"
    )
    pieces.append("</section>")
    return "\n".join(pieces)


def render_result_table() -> str:
    """Render the table of checked results.

    Returns:
        The table as HTML.
    """
    rows = "".join(
        f"<tr><td>{part}</td><td>{render_inline(check)}</td>"
        f"<td class=\"number\">{render_inline(measured)}</td>"
        f"<td class=\"number\">{render_inline(expected)}</td>"
        f"<td class=\"verdict\">{verdict}</td></tr>"
        for part, check, measured, expected, verdict in VERIFIED_RESULTS
    )
    return (
        '<table class="results"><thead><tr><th>Part</th><th>Checked quantity</th>'
        "<th>Measured</th><th>Expected</th><th>Verdict</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def build_page(parts_html: str, statements_html: str, answer_html: str) -> str:
    """Wrap the rendered parts in the page shell.

    Args:
        parts_html: HTML of the four parts.
        statements_html: HTML of the statement and the given data.
        answer_html: HTML of the paragraph that states the final answer.

    Returns:
        The complete page as HTML.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Volume of a solid bounded by a parabolic cylinder and two planes</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
  :root {{ color-scheme: light; }}
  body {{
    font-family: Cambria, "Cambria Math", Georgia, serif;
    max-width: 60rem;
    margin: 0 auto;
    padding: 2rem 1.25rem 4rem;
    line-height: 1.62;
    color: #1d1d1f;
    background: #fdfdfb;
  }}
  h1 {{ font-size: 1.9rem; line-height: 1.25; margin: 0 0 0.35rem; }}
  h2 {{ font-size: 1.35rem; margin: 2.4rem 0 0.8rem; border-bottom: 1px solid #d8d8d2; padding-bottom: 0.3rem; }}
  h3 {{ font-size: 1.1rem; margin: 1.8rem 0 0.5rem; color: #24384f; }}
  p {{ margin: 0.6rem 0; }}
  .subtitle {{ color: #5b5b56; margin: 0 0 1.6rem; }}
  blockquote {{
    margin: 1rem 0; padding: 0.7rem 1rem; border-left: 3px solid #2f6690; background: #f2f6fa;
  }}
  blockquote p {{ margin: 0.2rem 0; }}
  code {{ font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 0.92em;
         background: #f0f0ec; padding: 0 0.2em; }}
  .display-math {{ margin: 0.9rem 0 1rem; overflow-x: auto; }}
  .katex {{ font-family: "XITS Math", "STIX Two Math", "Cambria Math", serif; }}
  .part {{ margin-top: 1rem; }}
  .answer {{
    margin: 1.2rem 0 0.4rem; padding: 0.7rem 0.9rem;
    border: 1px solid #cfe0ef; background: #f5f9fd; border-radius: 4px;
  }}
  figure {{ margin: 1.2rem 0 1.4rem; text-align: center; }}
  figure img {{ max-width: 100%; height: auto; }}
  figcaption {{ font-size: 0.9rem; color: #4a4a46; margin-top: 0.4rem; text-align: left; }}
  table.results {{ border-collapse: collapse; width: 100%; font-size: 0.92rem; margin: 0.8rem 0 1.2rem; }}
  table.results th, table.results td {{ border: 1px solid #dcdcd6; padding: 0.32rem 0.5rem; text-align: left; }}
  table.results th {{ background: #f2f2ec; font-weight: 600; }}
  table.results td.number {{ font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 0.88rem; }}
  table.results td.verdict {{ font-weight: 600; color: #1c6b3a; }}
  footer {{ margin-top: 3rem; border-top: 1px solid #d8d8d2; padding-top: 0.8rem;
            font-size: 0.88rem; color: #5b5b56; }}
</style>
</head>
<body>

<h1>Volume of a solid bounded by a parabolic cylinder and two planes</h1>
<p class="subtitle">Tutorial for exercise 21 of section 15.7, <em>Triple Integrals</em>,
<em>Calculus: Early Transcendentals</em>. Every numerical claim below comes from a script that
the page names.</p>

<section class="statement">
<h2>The statement</h2>
<blockquote>
<p>Use a triple integral to find the volume of the given solid.</p>
<p>The solid enclosed by the cylinder $y = x^{2}$ and the planes $z = 0$ and $y + z = 1$.</p>
</blockquote>
<p>The exercise gives no length. The three equations fix the solid completely, so every bound
below is derived from them. A figure shows only one cut of the solid, so no bound of this
solution comes from the shape of a drawing.</p>
{statements_html}
</section>

<h2>The answer</h2>
{answer_html}

{parts_html}

<section class="results-section">
<h2>The checked results</h2>
<p>Each row is one line that a verification script printed. A row passes only when the script
compared the measured value with the expected value and the difference stayed inside the stated
tolerance.</p>
{render_result_table()}
</section>

<section class="reproduce">
<h2>How to reproduce the numbers</h2>
<ul>
<li>Environment: Python 3.14.3 in <code>code/.venv</code>, created with <code>uv venv</code>.</li>
<li>Packages: numpy 2.5.5, scipy 1.18.1, matplotlib 3.11.2, recorded in
<code>code/requirements.txt</code>.</li>
<li>Random seed: 20261122, in <code>code/part1_verify.py</code>, <code>code/part3_verify.py</code>,
and <code>code/part4_verify.py</code>.</li>
<li>Verification: <code>code/part1_verify.py</code>, <code>code/part2_verify.py</code>,
<code>code/part3_verify.py</code>, and <code>code/part4_verify.py</code>.</li>
<li>Figures: <code>code/part1_figure1.py</code> and <code>code/part3_figure2.py</code>, which write
the images below <code>code/figures/</code>.</li>
<li>Page: <code>code/build_report.py</code> reads the step files and writes this page.</li>
</ul>
</section>

<footer>
<p>Prepared by the Tutor stage of MCMA for session 20261122_204216_tutoring_problem_5 with
parameters version v2.</p>
</footer>

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
    """Compose the tutorial page from the step files and the figures."""
    steps = read_step_files()
    parts_html = "\n".join(
        render_part(part, [step for step in steps if step[0] == part]) for part in sorted(PART_TITLES)
    )
    statements_html = (
        "<h3>Given data</h3>\n<ul>\n"
        "<li>The cylinder $y = x^{2}$ bounds the solid.</li>\n"
        "<li>The plane $z = 0$ bounds the solid.</li>\n"
        "<li>The plane $y + z = 1$ bounds the solid.</li>\n"
        "<li>The exercise asks for the volume $V$, and it requires a triple integral.</li>\n"
        "</ul>\n"
        "<p>Source: <code>problem/problem.md</code>, which quotes the exercise text and records the "
        "origin of every fact. The source image is <code>problem/source/problem.png</code>.</p>"
    )
    answer_html = (
        "<p>$$V = \\int_{-1}^{1} \\int_{x^{2}}^{1} \\int_{0}^{1 - y} dz\\, dy\\, dx"
        " = \\frac{8}{15} \\approx 0.5333 \\text{ cubic units}.$$</p>"
    )
    REPORT_PATH.write_text(
        build_page(parts_html, statements_html, answer_html), encoding="utf-8", newline="\n"
    )
    print(f"page written to {REPORT_PATH}")
    print(f"steps written into the page: {len(steps)}")


if __name__ == "__main__":
    main()
