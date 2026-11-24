"""Compose the tutorial page report.html from the step files and the figures.

The composer reads steps/part<part>_step<step>.md in order, reads the PNG files under
code/figures/, and writes one page with the statement, the steps, the figures as Base64
data identifiers, the table of results, and the KaTeX renderer. It also checks that the
composed page holds no control character and that each inline code element holds a name.
"""

from __future__ import annotations

import base64
import html
import re
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent.parent
"""The problem workspace that holds the step files and the figures."""

STEP_DIRECTORY = WORKSPACE / "steps"
"""The directory that holds the step files."""

FIGURE_DIRECTORY = WORKSPACE / "code" / "figures"
"""The directory that holds the figures."""

REPORT_PATH = WORKSPACE / "report.html"
"""The composed product page."""

CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
"""The control characters that a composed page must not hold."""

STATEMENT = r"""Find the mass and center of mass of the solid $E$ with the given density function
$\rho$. $E$ is the solid that lies under the plane $z = 1 + x + y$ and above the region in the
$xy$-plane bounded by the curves $y = \sqrt{x}$, $y = 0$, and $x = 1$; $\rho(x, y, z) = 2$."""

PARTS = (
    (1, "The planar region $D$", "Read the base of the solid and compute its area."),
    (2, "The height and the volume of $E$", "Integrate the height of the ceiling over the base."),
    (3, "The mass of $E$", "Multiply the volume by the constant density."),
    (4, "The moment $M_{yz}$ and the coordinate $\\bar{x}$", "Integrate $x\\rho$ over $E$."),
    (5, "The moment $M_{xz}$ and the coordinate $\\bar{y}$", "Integrate $y\\rho$ over $E$."),
    (6, "The moment $M_{xy}$ and the coordinate $\\bar{z}$", "Integrate $z\\rho$ over $E$ and answer."),
)

FIGURES = {
    1: ("part1_figure1.png", "Figure 1. The planar region $D$ with the curve $y = \\sqrt{x}$, "
                            "the line $x = 1$, and the line $y = 0$."),
    2: ("part6_figure2.png", "Figure 2. The solid $E$, its ceiling $z = 1 + x + y$, its two "
                            "vertical walls, its floor $z = 0$, the center of mass, and the "
                            "projection of the center of mass on the floor."),
}

FIGURE_AFTER_STEP = {2: 1, 6: 2}
"""The figure number that each part shows after its last step."""

RESULTS = (
    ("Area of $D$", r"\frac{2}{3}", "0.666667"),
    ("Volume $V$", r"\frac{79}{60}", "1.316667"),
    ("Mass $m$", r"\frac{79}{30}", "2.633333"),
    ("$M_{yz}$", r"\frac{179}{105}", "1.704762"),
    ("$\\bar{x}$", r"\frac{358}{553}", "0.647378"),
    ("$M_{xz}$", r"\frac{11}{10}", "1.100000"),
    ("$\\bar{y}$", r"\frac{33}{79}", "0.417722"),
    ("$M_{xy}$", r"\frac{571}{210}", "2.719048"),
    ("$\\bar{z}$", r"\frac{571}{553}", "1.032550"),
)


def inline_markup(text: str) -> str:
    """Return one text run with escaped HTML and inline code spans rendered."""
    pieces = re.split(r"(`[^`]+`)", text)
    output = []
    for piece in pieces:
        if len(piece) >= 2 and piece.startswith("`") and piece.endswith("`"):
            output.append("<code>" + html.escape(piece[1:-1]) + "</code>")
        else:
            output.append(html.escape(piece, quote=False))
    return "".join(output)


def render_block(block: str) -> str:
    """Return the HTML of one block of a step file."""
    stripped = block.strip()
    if not stripped:
        return ""
    if stripped.startswith("$$") and stripped.endswith("$$"):
        return f'<div class="display">{html.escape(stripped, quote=False)}</div>'
    if stripped.startswith("### "):
        return f"<h3>{inline_markup(stripped[4:])}</h3>"
    if stripped.startswith("## "):
        return f"<h2>{inline_markup(stripped[3:])}</h2>"
    if stripped.startswith("# "):
        return f'<h2 class="step-title">{inline_markup(stripped[2:])}</h2>'
    lines = stripped.split("\n")
    if all(line.lstrip().startswith("- ") for line in lines):
        items = "".join(f"<li>{inline_markup(line.lstrip()[2:])}</li>" for line in lines)
        return f'<ul class="tight">{items}</ul>'
    joined = " ".join(line.strip() for line in lines)
    return f"<p>{inline_markup(joined)}</p>"


def markdown_to_html(source: str) -> str:
    """Return the HTML of a Markdown step file, with display mathematics preserved."""
    blocks = re.split(r"\n\s*\n", source)
    rendered = [render_block(block) for block in blocks]
    return "\n".join(item for item in rendered if item)


def figure_data_identifier(file_name: str) -> str:
    """Return the Base64 data identifier of one PNG file."""
    payload = (FIGURE_DIRECTORY / file_name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(payload).decode("ascii")


def read_steps() -> dict[tuple[int, int], str]:
    """Return the HTML of each step file, keyed by part number and step number."""
    steps: dict[tuple[int, int], str] = {}
    for path in sorted(STEP_DIRECTORY.glob("part*_step*.md")):
        match = re.fullmatch(r"part(\d+)_step(\d+)\.md", path.name)
        if match is None:
            continue
        steps[(int(match.group(1)), int(match.group(2)))] = markdown_to_html(
            path.read_text(encoding="utf-8")
        )
    return steps


def figure_html(figure_number: int) -> str:
    """Return the HTML of one figure with its data identifier and its caption."""
    file_name, caption = FIGURES[figure_number]
    identifier = figure_data_identifier(file_name)
    return (
        f'<figure><img alt="Figure {figure_number}" src="{identifier}">'
        f"<figcaption>{caption}</figcaption></figure>"
    )


def results_table() -> str:
    """Return the HTML table of the verified results."""
    rows = []
    for label, exact, decimal in RESULTS:
        rows.append(
            f"<tr><td>{label}</td><td class=\"math\">${exact}$</td>"
            f"<td class=\"math\">${decimal}$</td></tr>"
        )
    header = (
        "<thead><tr><th>Quantity</th><th>Exact value</th><th>Decimal value</th></tr></thead>"
    )
    return f'<table class="results">{header}<tbody>{"".join(rows)}</tbody></table>'


def main() -> None:
    """Write report.html and check the composed page."""
    steps = read_steps()
    expected_keys = {(part, step) for part in range(1, 7) for step in (1, 2)}
    missing = sorted(expected_keys - set(steps))
    print(f"step files read: computed = {len(steps)}, expected = {len(expected_keys)}")
    assert not missing, f"missing step files: {missing}"

    body = []
    body.append("<h2>Statement</h2>")
    body.append(f'<blockquote class="statement">{STATEMENT}</blockquote>')
    body.append(
        "<p>All numbers in this page come from the six verification scripts under "
        "<code>code/</code>. Each script prints the computed value beside the expected value "
        "and asserts the two values against the tolerance that its method supports.</p>"
    )
    for part, title, note in PARTS:
        body.append(f'<h2 class="part">Part {part}. {title}</h2>')
        body.append(f'<p class="note">{note}</p>')
        for step in (1, 2):
            body.append(f'<div class="step">{steps[(part, step)]}</div>')
        if part in FIGURE_AFTER_STEP:
            body.append(figure_html(FIGURE_AFTER_STEP[part]))

    body.append("<h2>Table of verified results</h2>")
    body.append(results_table())
    body.append(
        "<h2>Scripts</h2><ul class=\"tight\">"
        "<li><code>code/part1_verify.py</code> checks the area of $D$.</li>"
        "<li><code>code/part2_verify.py</code> checks the slice area and the volume.</li>"
        "<li><code>code/part3_verify.py</code> checks the mass.</li>"
        "<li><code>code/part4_verify.py</code> checks $M_{yz}$ and $\\bar{x}$.</li>"
        "<li><code>code/part5_verify.py</code> checks $M_{xz}$ and $\\bar{y}$.</li>"
        "<li><code>code/part6_verify.py</code> checks $M_{xy}$, $\\bar{z}$, and the three "
        "coordinates together.</li>"
        "<li><code>code/part1_figure1.py</code> draws Figure 1.</li>"
        "<li><code>code/part6_figure2.py</code> draws Figure 2.</li></ul>"
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Mass and center of mass of the solid E</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
  body {{ font-family: Cambria, "Times New Roman", serif; max-width: 52rem; margin: 2rem auto;
         padding: 0 1.25rem; color: #1b1b1b; line-height: 1.62; font-size: 1.06rem; }}
  h1 {{ font-size: 1.75rem; border-bottom: 2px solid #12457a; padding-bottom: .4rem; }}
  h2 {{ font-size: 1.22rem; margin-top: 2.1rem; color: #12457a; }}
  h3 {{ font-size: 1.02rem; margin-top: 1.3rem; color: #333; text-transform: uppercase;
        letter-spacing: .04em; }}
  .step-title {{ font-size: 1.06rem; color: #0d2f52; margin-top: 1.5rem; }}
  .part {{ border-left: 5px solid #7fb3e8; padding-left: .7rem; }}
  .note {{ color: #555; font-style: italic; margin-top: -.3rem; }}
  .step {{ margin-left: 1rem; }}
  .display {{ margin: .7rem 0; overflow-x: auto; }}
  blockquote.statement {{ background: #f3f7fb; border-left: 5px solid #12457a;
                          margin: 1rem 0; padding: .8rem 1rem; }}
  code {{ font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: .92em;
          background: #f1f3f5; padding: .08em .3em; border-radius: 3px; }}
  figure {{ margin: 1.4rem 0; text-align: center; }}
  figure img {{ max-width: 100%; border: 1px solid #d6d9dd; border-radius: 4px; }}
  figcaption {{ color: #444; font-size: .95rem; margin-top: .45rem; }}
  table.results {{ border-collapse: collapse; margin: 1rem 0; width: 100%; }}
  table.results th, table.results td {{ border-bottom: 1px solid #dfe3e8; padding: .42rem .6rem;
                                       text-align: left; }}
  table.results thead th {{ background: #eef3f8; }}
  ul.tight {{ margin: .5rem 0; }}
  .katex {{ font-family: XITS, "Cambria Math", serif; }}
</style>
</head>
<body>
<h1>Mass and center of mass of the solid $E$</h1>
{chr(10).join(body)}
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
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")

    control_count = len(CONTROL_CHARACTERS.findall(page))
    empty_code = page.count("<code></code>")
    print(f"control characters in the page: computed = {control_count}, expected = 0")
    assert control_count == 0
    print(f"empty inline code elements: computed = {empty_code}, expected = 0")
    assert empty_code == 0

    names = re.findall(r"<code>([^<]*)</code>", page)
    blank_names = [name for name in names if not name.strip()]
    print(f"inline code elements: computed = {len(names)}, expected at least 12 "
          f"(one check sentence for each step)")
    assert len(names) >= 12
    print(f"inline code elements without a name: computed = {len(blank_names)}, expected = 0")
    assert not blank_names
    print(f"page written: {REPORT_PATH}")


if __name__ == "__main__":
    main()
