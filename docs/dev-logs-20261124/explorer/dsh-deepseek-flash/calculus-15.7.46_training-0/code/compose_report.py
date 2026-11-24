"""Compose the tutorial page from the step files and the figures.

The module reads one markdown file for each step from ``steps/``, replaces each figure with a
Base64 data uniform resource identifier, and writes ``report.html``. The page holds the statement,
the steps in order, the figures, and a table of the checked values. The composition asserts that
the page holds no control character, no empty inline code element, and one heading for each step
file.
"""

from __future__ import annotations

import base64
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
"""The workspace of the session."""

STEP_DIRECTORY = WORKSPACE / "steps"
"""The directory of the step files."""

REPORT_PATH = WORKSPACE / "report.html"
"""The output path of the composed page."""

PART_TITLES = {
    1: "Part 1. Read the solid and the quantity",
    2: "Part 2. Choose coordinates and derive the limits",
    3: "Part 3. Integrate and get the value",
    4: "Part 4. Check the value by horizontal slices",
    5: "Part 5. State the answer in terms of the mass",
}
"""The title of each part of the solution."""

PART_SUMMARIES = {
    1: "The body is a right circular cone, and the answer is the integral of the density times the squared distance to the z-axis.",
    2: "Cylindrical coordinates turn the shape into the limits r ≤ z ≤ h, then 0 ≤ r ≤ h, then 0 ≤ θ ≤ 2π.",
    3: "Two integrations give I = π k h⁵/10.",
    4: "A second route stacks the moments of the horizontal slices and gives the same value.",
    5: "The mass of the cone turns the answer into (3/10) M h².",
}
"""One sentence for each part, used in the outline of the page."""

STATEMENT_HTML = """
<p class="statement">Assume that the solid has constant density $k$. Find the moment of inertia
about the $z$-axis of the solid cone</p>
$$\\sqrt{x^{2}+y^{2}} \\le z \\le h .$$
<p>The statement prints no numerical value for $k$ and no numerical value for $h$, so the answer is
an expression in these two symbols. The words "solid cone" carry the condition $h &gt; 0$, which a
body of positive volume needs.</p>
"""
"""The statement of the problem, quoted from the exercise and from the intake note."""

RESULT_ROWS = [
    ("Volume at $h = 1$", "adaptive quadrature of the volume element", "1.047197551"),
    ("Volume at $h = 1$", "$\\pi h^{3}/3$", "1.047198"),
    ("Volume at $h = 1$", "Monte Carlo over 2000000 points", "1.046738 $\\pm$ 0.001243"),
    ("Jacobian determinant", "finite difference against $r$", "gap 2.581e-10"),
    ("Inner integral, $r = 0.3$, $h = 1$", "symbolic, exact fraction, quadrature", "189/10000"),
    ("Middle integral, $h = 1$", "symbolic, exact fraction, quadrature, Simpson", "0.05000000"),
    ("Middle integral, $h = 1.7$", "formula $h^{5}/20$, quadrature, Simpson", "0.7099285000"),
    ("$I_{z}$ at $k = 1$, $h = 1$", "triple adaptive quadrature", "0.314159265359"),
    ("$I_{z}$ at $k = 1$, $h = 1$", "stack of the slice moments", "0.314159265359"),
    ("$I_{z}$ at $k = 1$, $h = 1$", "Monte Carlo over 2000000 points", "0.313724 $\\pm$ 0.000408"),
    ("Mass $M$ at $k = 1$, $h = 1$", "stack of the slice masses", "1.047197551"),
    ("Mass $M$ at $k = 1$, $h = 1$", "Monte Carlo over 2000000 points", "1.045362 $\\pm$ 0.001243"),
    ("$I_{z}$ at $k = 2.3$, $h = 1.7$", "formula $\\pi k h^{5}/10$", "10.2594083368"),
    ("$I_{z}$ at $k = 2.3$, $h = 1.7$", "triple adaptive quadrature", "10.2594083368"),
    ("Ratio $I_{z}(2h)/I_{z}(h)$", "quadrature and formula", "32.0000000000"),
]
"""Each checked quantity with the method that produced it and the value that it printed."""

KATEX_STYLE = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
"""The style sheet of KaTeX."""

KATEX_SCRIPT = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"
"""The main script of KaTeX."""

KATEX_AUTO_RENDER = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
"""The script that renders the mathematics of the page."""

FIGURE_PATTERN = re.compile(r"^!\[(?P<alt>[^\]]+)\]\((?P<path>[^)]+)\)$")
"""The pattern of a figure line in a step file."""

STEP_NAME_PATTERN = re.compile(r"^part(?P<part>\d+)_step(?P<step>\d+)\.md$")
"""The pattern of the file name of a step file."""

VERIFICATION_PATTERN = re.compile(r"Verification:\s+`(code/[A-Za-z0-9_]+\.py)`")
"""The pattern that names the script which verifies a step."""

CSS = """
:root { color-scheme: light; }
body { margin: 0; background: #f7f8fa; color: #1c2430;
  font-family: Cambria, "Cambria Math", Georgia, serif; line-height: 1.62; }
main { max-width: 52rem; margin: 0 auto; padding: 3rem 1.6rem 5rem; }
header.page { border-bottom: 2px solid #d7dde6; padding-bottom: 1.4rem; margin-bottom: 2rem; }
h1 { font-size: 1.85rem; margin: 0 0 0.4rem; letter-spacing: 0.01em; }
p.subtitle { margin: 0; color: #5b6878; font-size: 0.98rem; }
nav.outline { background: #fff; border: 1px solid #dde3ec; border-radius: 10px;
  padding: 1rem 1.3rem; margin: 1.6rem 0 2.2rem; font-size: 0.95rem; }
nav.outline h2 { font-size: 1rem; margin: 0 0 0.6rem; color: #33445a; }
nav.outline ol { margin: 0; padding-left: 1.25rem; }
nav.outline li { margin: 0.25rem 0; }
section.part { margin: 2.6rem 0 0; }
h2.part-title { font-size: 1.28rem; color: #14375e; border-left: 5px solid #2f6fa8;
  padding-left: 0.7rem; margin: 0 0 1rem; }
p.part-summary { color: #4d5b6d; margin: 0 0 1.2rem; }
article.step { background: #fff; border: 1px solid #e1e7ef; border-radius: 12px;
  padding: 1.2rem 1.4rem 1.3rem; margin: 1.1rem 0; box-shadow: 0 1px 2px rgba(20,55,94,0.05); }
h3.step-title { font-size: 1.08rem; margin: 0 0 0.7rem; color: #1f4e79; }
h4.section { font-size: 0.92rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: #6a7787; margin: 1.1rem 0 0.35rem; }
p { margin: 0.55rem 0; }
ul { margin: 0.5rem 0 0.5rem 1.1rem; padding: 0; }
li { margin: 0.25rem 0; }
div.math { overflow-x: auto; overflow-y: hidden; padding: 0.35rem 0; }
code { background: #eef2f7; border: 1px solid #dde4ee; border-radius: 4px; padding: 0.05em 0.3em;
  font-family: "Cascadia Mono", Consolas, monospace; font-size: 0.86em; color: #1a3d63; }
figure { margin: 1.3rem 0; text-align: center; background: #fbfcfe; border: 1px solid #e4e9f1;
  border-radius: 10px; padding: 0.8rem; }
figure img { max-width: 100%; height: auto; }
figcaption { margin-top: 0.5rem; font-size: 0.88rem; color: #55637a; text-align: left; }
div.answer { margin: 1.1rem 0 0.2rem; background: #eef5fb; border: 1px solid #c6dbee;
  border-left: 5px solid #2f6fa8; border-radius: 8px; padding: 0.75rem 1rem; }
div.answer p { margin: 0.2rem 0; }
div.final { background: #f2f8f3; border: 1px solid #c9e2cd; border-left: 5px solid #3a7d44; }
table { border-collapse: collapse; width: 100%; font-size: 0.92rem; margin: 1rem 0 0; }
caption { caption-side: top; text-align: left; color: #3f4c5c; font-size: 0.92rem;
  padding-bottom: 0.5rem; }
th, td { border-bottom: 1px solid #e2e7ee; padding: 0.45rem 0.6rem; text-align: left;
  vertical-align: top; }
th { background: #f0f4f9; color: #26374d; font-weight: 600; }
footer { margin-top: 3rem; border-top: 1px solid #dde3ec; padding-top: 1rem; font-size: 0.85rem;
  color: #6a7787; }
.katex { font-family: "XITS Math", "XITS", "STIX Two Math", "Cambria Math", serif; }
@media print { body { background: #fff; } article.step { box-shadow: none; } }
"""
"""The style sheet of the page."""


def inline_markup(text: str) -> str:
    """Convert the inline markup of a step file to HTML.

    Args:
        text: One line or one paragraph of a step file.

    Returns:
        The text with inline code, bold words, and line breaks converted to HTML.
    """
    result = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    result = re.sub(r"`([^`]+)`", r"<code>\1</code>", result)
    return result


def figure_data_identifier(path: Path) -> str:
    """Return the Base64 data uniform resource identifier of an image file.

    Args:
        path: The path of the PNG file.

    Returns:
        The data uniform resource identifier that holds the bytes of the file.
    """
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def figure_html(alt: str, relative_path: str, workspace: Path) -> str:
    """Build the HTML of one figure from a line of a step file.

    Args:
        alt: The caption of the figure.
        relative_path: The path of the image, relative to the workspace.
        workspace: The workspace of the session.

    Returns:
        The HTML block of the figure.
    """
    image_path = workspace / relative_path
    if not image_path.is_file():
        image_path = workspace / "code" / relative_path
    if not image_path.is_file():
        raise FileNotFoundError(f"the figure file is absent: {image_path}")
    identifier = figure_data_identifier(image_path)
    plain_alt = re.sub(r"\$", "", alt)
    return (
        '<figure>\n'
        f'  <img src="{identifier}" alt="{plain_alt}">\n'
        f"  <figcaption>{inline_markup(alt)}</figcaption>\n"
        "</figure>"
    )


def block_to_html(block: list[str], workspace: Path) -> str:
    """Convert one block of a step file to HTML.

    Args:
        block: The non-empty lines of the block.
        workspace: The workspace of the session.

    Returns:
        The HTML of the block.
    """
    first = block[0]
    if first.startswith("# "):
        return f'<h3 class="step-title">{inline_markup(first[2:].strip())}</h3>'
    if first.startswith("## "):
        return f'<h4 class="section">{inline_markup(first[3:].strip())}</h4>'
    if first.startswith("$$") and first.rstrip().endswith("$$") and len(block) == 1:
        return f'<div class="math">{first.strip()}</div>'
    if first.startswith("!["):
        match = FIGURE_PATTERN.match(first.strip())
        if match is None:
            raise ValueError(f"the figure line is malformed: {first}")
        return figure_html(match.group("alt"), match.group("path"), workspace)
    if first.startswith("> "):
        lines = [line[2:].strip() if line.startswith("> ") else line.lstrip(">").strip()
                 for line in block]
        body = " ".join(inline_markup(line) for line in lines if line)
        return f'<div class="answer"><p>{body}</p></div>'
    if first.startswith("- "):
        items = []
        for line in block:
            text = line[2:].strip() if line.startswith("- ") else line.strip()
            items.append(f"<li>{inline_markup(text)}</li>")
        return "<ul>\n" + "\n".join(items) + "\n</ul>"
    body = " ".join(inline_markup(line.strip()) for line in block)
    return f"<p>{body}</p>"


def block_kind(line: str) -> str:
    """Return the kind of one non-empty line of a step file.

    Args:
        line: One non-empty line of a step file.

    Returns:
        The kind of the line: heading, display, figure, quote, list, or text.
    """
    if line.startswith("# "):
        return "heading"
    if line.startswith("## "):
        return "subheading"
    if line.startswith("$$") and line.endswith("$$"):
        return "display"
    if line.startswith("!["):
        return "figure"
    if line.startswith("> "):
        return "quote"
    if line.startswith("- "):
        return "list"
    return "text"


def markdown_to_html(text: str, workspace: Path) -> str:
    """Convert the markdown of a step file to HTML.

    A block ends at a blank line or where the kind of the line changes. A quotation keeps its
    lines together even when several lines start with the mark of a quotation.

    Args:
        text: The whole text of the step file.
        workspace: The workspace of the session.

    Returns:
        The HTML of the step.
    """
    single_line_kinds = {"heading", "subheading", "display", "figure"}
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                blocks.append(current)
                current = []
            continue
        kind = block_kind(stripped)
        if current and (kind != block_kind(current[0]) or kind in single_line_kinds):
            blocks.append(current)
            current = []
        current.append(stripped)
        if kind in single_line_kinds:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return chr(10).join(block_to_html(block, workspace) for block in blocks)


def read_steps(directory: Path) -> dict[tuple[int, int], tuple[Path, str]]:
    """Read every step file and key it by its part number and its step number.

    Args:
        directory: The directory of the step files.

    Returns:
        The map from the pair (part, step) to the path and the text of the file.
    """
    steps: dict[tuple[int, int], tuple[Path, str]] = {}
    for path in sorted(directory.iterdir()):
        match = STEP_NAME_PATTERN.match(path.name)
        if match is None:
            continue
        key = (int(match.group("part")), int(match.group("step")))
        steps[key] = (path, path.read_text(encoding="utf-8"))
    return steps


def results_table(rows: list[tuple[str, str, str]]) -> str:
    """Build the HTML of the table of checked values.

    Args:
        rows: One triple of quantity, method, and value for each row.

    Returns:
        The HTML of the table.
    """
    body = "\n".join(
        f"<tr><td>{inline_markup(quantity)}</td><td>{inline_markup(method)}</td>"
        f"<td>{inline_markup(value)}</td></tr>"
        for quantity, method, value in rows
    )
    return (
        "<table>\n"
        "<caption>Table 1. Each checked quantity, the method that computed it, and the value that "
        "the method printed. Every row is printed by the verification script that the step "
        "cites.</caption>\n"
        "<thead><tr><th>Quantity</th><th>Method</th><th>Value</th></tr></thead>\n"
        "<tbody>\n"
        f"{body}\n"
        "</tbody>\n"
        "</table>"
    )


def outline_html(parts: list[int]) -> str:
    """Build the outline of the page.

    Args:
        parts: The part numbers in order.

    Returns:
        The HTML of the outline.
    """
    items = "\n".join(
        f"<li><strong>{PART_TITLES[part]}</strong> {inline_markup(PART_SUMMARIES[part])}</li>"
        for part in parts
    )
    return (
        '<nav class="outline">\n<h2>What this tutorial does</h2>\n<ol>\n'
        f"{items}\n</ol>\n</nav>"
    )


def build_page(steps: dict[tuple[int, int], tuple[Path, str]], workspace: Path) -> str:
    """Build the whole HTML page.

    Args:
        steps: The map from the pair (part, step) to the path and the text of the file.
        workspace: The workspace of the session.

    Returns:
        The HTML text of the page.
    """
    parts = sorted({part for part, _ in steps})
    sections = []
    for part in parts:
        step_keys = sorted(step for part_number, step in steps if part_number == part)
        articles = []
        for step in step_keys:
            path, text = steps[(part, step)]
            articles.append(f'<article class="step" id="{path.stem}">\n'
                            f"{markdown_to_html(text, workspace)}\n</article>")
        sections.append(
            f'<section class="part" id="part{part}">\n'
            f'<h2 class="part-title">{PART_TITLES[part]}</h2>\n'
            f'<p class="part-summary">{inline_markup(PART_SUMMARIES[part])}</p>\n'
            + "\n".join(articles) + "\n</section>"
        )

    final_block = (
        '<section class="part" id="answer">\n'
        '<h2 class="part-title">Answer</h2>\n'
        '<div class="answer final">\n'
        "<p>The moment of inertia of the solid cone about the $z$-axis is</p>\n"
        '<div class="math">$$I_{z} = \\frac{\\pi k h^{5}}{10} = \\frac{3}{10}\\,M h^{2},'
        "\\qquad M = \\frac{\\pi k h^{3}}{3} .$$</div>\n"
        "<p>The first form holds the data of the statement, the constant density $k$ and the "
        "height $h$. The second form holds the mass $M$ of the cone. At $k = 2.3$ and $h = 1.7$ "
        "the value is $10.2594083368$.</p>\n"
        "</div>\n</section>"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moment of inertia of a solid cone about the z-axis</title>
<link rel="stylesheet" href="{KATEX_STYLE}">
<style>{CSS}</style>
</head>
<body>
<main>
<header class="page">
<h1>Moment of inertia of a solid cone about the $z$-axis</h1>
<p class="subtitle">A step-by-step solution with one verification script for each part</p>
</header>
<section class="part" id="statement">
<h2 class="part-title">Statement</h2>
{STATEMENT_HTML}
</section>
{outline_html(parts)}
{"".join(sections)}
{final_block}
<section class="part" id="checks">
<h2 class="part-title">Checked values</h2>
{results_table(RESULT_ROWS)}
</section>
<footer>
<p>The figures are Base64 data uniform resource identifiers, so the page needs no other file. The
scripts are <code>code/part1_verify.py</code>, <code>code/part2_verify.py</code>,
<code>code/part3_verify.py</code>, <code>code/part4_verify.py</code>, and
<code>code/part5_verify.py</code>. The figures are drawn by <code>code/part1_figure1.py</code>,
<code>code/part2_figure1.py</code>, and <code>code/part4_figure1.py</code>. Every script ran
with Python 3.14.3, numpy 2.5.5, scipy 1.18.1, sympy 1.14.0, and matplotlib 3.11.2, and every
random sample used the seed 20261123.</p>
</footer>
</main>
<script src="{KATEX_SCRIPT}"></script>
<script src="{KATEX_AUTO_RENDER}"></script>
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


def check_page(html: str, steps: dict[tuple[int, int], tuple[Path, str]]) -> None:
    """Check the composed page and stop on a fault.

    Args:
        html: The HTML text of the page.
        steps: The map from the pair (part, step) to the path and the text of the file.

    Returns:
        None. The function asserts each property of the page.
    """
    control_characters = [character for character in html
                          if ord(character) < 32 and character not in "\n\t"]
    print(f"control characters: computed = {len(control_characters)}, expected = 0")
    assert not control_characters, "the page holds a control character"

    empty_code = html.count("<code></code>")
    print(f"empty inline code elements: computed = {empty_code}, expected = 0")
    assert empty_code == 0, "the page holds an empty inline code element"

    code_elements = re.findall(r"<code>([^<]*)</code>", html)
    print(f"inline code elements: computed = {len(code_elements)}, expected >= 8")
    assert len(code_elements) >= 8, "the page holds too few inline code elements"
    names = [element for element in code_elements if element.startswith("code/")]
    print(f"code elements that name a script: computed = {len(names)}, expected >= 8")
    assert len(names) >= 8, "the inline code elements do not name the scripts"

    headings = html.count('<h3 class="step-title">')
    print(f"step headings: computed = {headings}, expected = {len(steps)}")
    assert headings == len(steps), "the page does not hold one heading for each step file"

    for part in sorted({part for part, _ in steps}):
        for step in sorted(step for part_number, step in steps if part_number == part):
            _, text = steps[(part, step)]
            found = VERIFICATION_PATTERN.search(text)
            assert found is not None, f"the step {part}.{step} names no verification script"
            script = found.group(1)
            assert html.count(f"<code>{script}</code>") >= 1, \
                f"the page does not cite {script} for the step {part}.{step}"

    for number in range(1, 4):
        label = f"Figure {number}"
        print(f"citation of {label}: computed = {html.count(label)}, expected >= 1")
        assert label in html, f"the page cites no {label}"

    data_identifiers = html.count("data:image/png;base64,")
    print(f"embedded figures: computed = {data_identifiers}, expected = 3")
    assert data_identifiers == 3, "the page does not embed three figures"

    assert html.count("$$") % 2 == 0, "the display mathematics is not closed"
    print(f"display math delimiters: computed = {html.count('$$')}, expected even")


def main() -> None:
    """Read the steps, compose the page, check it, and write it."""
    if not STEP_DIRECTORY.is_dir():
        raise FileNotFoundError(f"the step directory is absent: {STEP_DIRECTORY}")
    steps = read_steps(STEP_DIRECTORY)
    print(f"step files read: computed = {len(steps)}, expected = 10")
    assert len(steps) == 10, "the workspace does not hold ten step files"
    html = build_page(steps, WORKSPACE)
    check_page(html, steps)
    REPORT_PATH.write_text(html, encoding="utf-8", newline="\n")
    print(f"page written: {REPORT_PATH}")
    print(f"page size: {len(html)} characters")


if __name__ == "__main__":
    main()
