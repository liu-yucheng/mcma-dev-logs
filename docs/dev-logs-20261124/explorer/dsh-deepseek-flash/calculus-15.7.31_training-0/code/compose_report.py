"""Compose the tutorial page of this session from the step files, the figures, and the results.

The page holds the statement, the fifteen steps in order, the four figures as Base64 data uniform
resource identifiers, and one table of verified results for each part.  KaTeX renders every
mathematical expression, and the page needs no other file.

The composer checks three properties of the page before it writes the file.  The page holds no control
character.  The page holds no empty inline code element.  Every figure of the directory is embedded.

Run this script with the interpreter of ``code/.venv``.  It writes ``report.html`` and ``tutorial.html``
in the problem workspace.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path

CODE_DIRECTORY = Path(__file__).resolve().parent
"""Directory of the Python scripts of the session."""

WORKSPACE = CODE_DIRECTORY.parent
"""Problem workspace of the session."""

STEPS_DIRECTORY = WORKSPACE / "steps"
"""Directory of the step files."""

FIGURE_DIRECTORY = CODE_DIRECTORY / "figures"
"""Directory of the figure files."""

RESULT_DIRECTORY = CODE_DIRECTORY / "results"
"""Directory of the verified results."""

REPORT_PATH = WORKSPACE / "report.html"
"""Path of the composed page."""

TUTORIAL_PATH = WORKSPACE / "tutorial.html"
"""Path of the second copy of the composed page."""

PARTS = {
    1: ("part1_step1.md", "part1_step2.md", "part1_step3.md"),
    2: ("part2_step1.md", "part2_step2.md", "part2_step3.md", "part2_step4.md"),
    3: ("part3_step1.md", "part3_step2.md"),
    4: ("part4_step1.md", "part4_step2.md"),
    5: ("part5_step1.md", "part5_step2.md"),
    6: ("part6_step1.md", "part6_step2.md"),
}
"""Step files of each part, in reading order."""

FIGURES = [
    (1, "part1_figure1.png",
     "The solid $E$ in four views. Panel (a) shows the three bounding surfaces and the three curves "
     "where two surfaces meet. Panels (b), (c), and (d) show the projection of $E$ on the plane "
     "$z = 0$, on the plane $x = 0$, and on the plane $y = 0$, with the two coordinates that each "
     "projection keeps."),
    (2, "part2_figure1.png",
     "The section of $E$ at a fixed value of one coordinate. Panel (a) is the triangle at $x = 0$, "
     "panel (b) is the rectangle at $y = 2$, and panel (c) is the parabolic segment at $z = 0.5$. "
     "Panel (d) plots the area of each section family against its parameter and marks the three "
     "heights that `code/part2_verify.py` samples."),
    (3, "part3_figure1.png",
     "The section at $x = 1$, which the two orders with $x$ outermost read in two ways. Panel (a) "
     "cuts the section into vertical pieces for the order $dz\\,dy\\,dx$: the inner integral in $z$ "
     "runs from 0 to $(4-y)/2$. Panel (b) cuts it into horizontal pieces for the order "
     "$dy\\,dz\\,dx$: the inner integral in $y$ runs from $x^{2}$ to $4-2z$."),
    (5, "part5_figure4.png",
     "The section at $z = 0.5$, which the two orders with $z$ outermost read in two ways. Panel (a) "
     "cuts the section into vertical pieces for the order $dy\\,dx\\,dz$: the inner integral in $y$ "
     "runs from $x^{2}$ to $3$. Panel (b) cuts it into horizontal pieces for the order "
     "$dx\\,dy\\,dz$: the inner integral in $x$ runs from $-\\sqrt{y}$ to $\\sqrt{y}$."),
]
"""Figure number, file name, and caption of each figure, in reading order."""

FINAL_ANSWERS = [
    ("$dz\\,dy\\,dx$",
     "\\int_{-2}^{2}\\int_{x^{2}}^{4}\\int_{0}^{(4-y)/2} f(x,y,z)\\,dz\\,dy\\,dx"),
    ("$dy\\,dz\\,dx$",
     "\\int_{-2}^{2}\\int_{0}^{(4-x^{2})/2}\\int_{x^{2}}^{4-2z} f(x,y,z)\\,dy\\,dz\\,dx"),
    ("$dz\\,dx\\,dy$",
     "\\int_{0}^{4}\\int_{-\\sqrt{y}}^{\\sqrt{y}}\\int_{0}^{(4-y)/2} f(x,y,z)\\,dz\\,dx\\,dy"),
    ("$dx\\,dz\\,dy$",
     "\\int_{0}^{4}\\int_{0}^{(4-y)/2}\\int_{-\\sqrt{y}}^{\\sqrt{y}} f(x,y,z)\\,dx\\,dz\\,dy"),
    ("$dy\\,dx\\,dz$",
     "\\int_{0}^{2}\\int_{-\\sqrt{4-2z}}^{\\sqrt{4-2z}}\\int_{x^{2}}^{4-2z} f(x,y,z)\\,dy\\,dx\\,dz"),
    ("$dx\\,dy\\,dz$",
     "\\int_{0}^{2}\\int_{0}^{4-2z}\\int_{-\\sqrt{y}}^{\\sqrt{y}} f(x,y,z)\\,dx\\,dy\\,dz"),
]
"""The order and the three limit groups of each of the six answers."""

STYLE_BLOCK = """
    :root {
      --ink: #1f2933;
      --muted: #52606d;
      --rule: #cbd2d9;
      --accent: #2f5d8a;
      --panel: #f5f7fa;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0 auto;
      padding: 2.4rem 1.6rem 4rem;
      max-width: 52rem;
      color: var(--ink);
      background: #ffffff;
      font-family: Cambria, "Times New Roman", serif;
      font-size: 1.02rem;
      line-height: 1.68;
    }
    h1 { font-size: 1.72rem; line-height: 1.28; margin: 0 0 0.35rem; }
    .subtitle { color: var(--muted); font-size: 0.95rem; margin: 0 0 1.6rem; }
    h2 {
      font-size: 1.26rem;
      margin: 2.3rem 0 0.7rem;
      padding-bottom: 0.28rem;
      border-bottom: 1px solid var(--rule);
    }
    h3 { font-size: 1.06rem; margin: 1.5rem 0 0.45rem; color: var(--accent); }
    p { margin: 0.55rem 0; }
    .statement {
      background: var(--panel);
      border-left: 3px solid var(--accent);
      padding: 0.85rem 1.1rem;
      margin: 1rem 0 0.4rem;
    }
    .statement p { margin: 0.35rem 0; }
    code {
      font-family: "Cascadia Mono", Consolas, "DejaVu Sans Mono", monospace;
      font-size: 0.88em;
      background: #eef2f6;
      padding: 0.06em 0.3em;
      border-radius: 3px;
    }
    .math-display { margin: 0.9rem 0; overflow-x: auto; overflow-y: hidden; }
    .step { border-left: 2px solid var(--rule); padding-left: 1rem; margin: 1.2rem 0; }
    table { border-collapse: collapse; width: 100%; margin: 0.9rem 0; font-size: 0.93rem; }
    th, td { border: 1px solid var(--rule); padding: 0.34rem 0.5rem; text-align: left; }
    th { background: var(--panel); font-weight: 600; }
    td.number { text-align: right; font-variant-numeric: tabular-nums; }
    figure { margin: 1.5rem 0; text-align: center; }
    figure img { max-width: 100%; height: auto; border: 1px solid var(--rule); }
    figcaption { color: var(--muted); font-size: 0.9rem; margin-top: 0.5rem; text-align: left; }
    .answer { background: var(--panel); border: 1px solid var(--rule); padding: 0.9rem 1.1rem; }
    .answer p { margin: 0.5rem 0 0.15rem; }
    nav ol { margin: 0.4rem 0 0.2rem 1.2rem; padding: 0; }
    nav li { margin: 0.16rem 0; }
    nav a { color: var(--accent); text-decoration: none; }
    nav a:hover { text-decoration: underline; }
    .katex { font-family: "XITS", "XITS Math", "Cambria Math", serif; }
    footer { margin-top: 2.6rem; color: var(--muted); font-size: 0.86rem; border-top: 1px solid var(--rule); padding-top: 0.7rem; }
"""
"""Style sheet of the page."""

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Six iterated integrals for one solid</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>{style}</style>
</head>
<body>
"""
"""Head of the page, with the KaTeX style sheet and the KaTeX scripts."""

TAIL_TEMPLATE = """<footer>
<p>Every number of this page is printed by a script under <code>code/</code> and stored in
<code>code/results/</code>. The environment is recorded in <code>code/requirements.txt</code>.</p>
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
"""Tail of the page, with the call that renders every mathematical expression."""

INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
"""Pattern of an inline code element in a step file."""

BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")
"""Pattern of a bold phrase in a step file."""

STEP_HEADING_MARKER = chr(10) + "## "
"""Prefix of the first step heading of a step file, used to drop the part introduction from a step."""


def render_inline(raw_text: str) -> str:
    """Render one line of a step file as inline markup.

    Args:
        raw_text: The source text of the line.

    Returns:
        The text with the special characters escaped, with a bold phrase as a strong element, and
        with an inline code element as a code element.
    """
    escaped = raw_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    with_code = INLINE_CODE_PATTERN.sub(lambda match: "<code>" + match.group(1) + "</code>", escaped)
    return BOLD_PATTERN.sub(lambda match: "<strong>" + match.group(1) + "</strong>", with_code)


def render_table(block_lines: list[str]) -> str:
    """Render a pipe table of a step file as an HTML table.

    Args:
        block_lines: The lines of the table, including the separator line.

    Returns:
        The HTML table.
    """
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in block_lines]
    header, body = rows[0], rows[2:]
    pieces = ["<table>", "<thead><tr>"]
    pieces.extend(f"<th>{render_inline(cell)}</th>" for cell in header)
    pieces.append("</tr></thead><tbody>")
    for row in body:
        pieces.append("<tr>")
        pieces.extend(f"<td>{render_inline(cell)}</td>" for cell in row)
        pieces.append("</tr>")
    pieces.append("</tbody></table>")
    return "".join(pieces)


def render_blocks(markdown_text: str) -> str:
    """Render the body of a step file as HTML.

    Args:
        markdown_text: The source text of the step file.

    Returns:
        The HTML of the body, without the part heading and without the step headings.
    """
    pieces: list[str] = []
    blocks = [block for block in markdown_text.split("\n\n") if block.strip()]
    for block in blocks:
        lines = block.strip().splitlines()
        first = lines[0].strip()
        if first.startswith("# "):
            continue
        if first.startswith("## "):
            continue
        if first.startswith("$$"):
            joined = " ".join(line.strip() for line in lines)
            pieces.append(f'<div class="math-display">{joined}</div>')
            continue
        if first.startswith("|"):
            pieces.append(render_table(lines))
            continue
        pieces.append(f"<p>{render_inline(' '.join(line.strip() for line in lines))}</p>")
    return "".join(pieces)


def extract_heading(markdown_text: str) -> str:
    """Return the part heading of a step file.

    Args:
        markdown_text: The source text of the step file.

    Returns:
        The text of the first level one heading, with the markup rendered.
    """
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return render_inline(line[2:].strip())
    raise ValueError("the step file holds no part heading")


def extract_step_heading(markdown_text: str) -> str:
    """Return the step heading of a step file.

    Args:
        markdown_text: The source text of the step file.

    Returns:
        The text of the first level two heading, with the markup rendered.
    """
    for line in markdown_text.splitlines():
        if line.startswith("## "):
            return render_inline(line[3:].strip())
    raise ValueError("the step file holds no step heading")


def read_statement() -> str:
    """Return the statement of the problem as HTML.

    Returns:
        The statement text of ``problem/problem.md``, rendered as paragraphs and display blocks.
    """
    source = (WORKSPACE / "problem" / "problem.md").read_text(encoding="utf-8")
    start = source.index("## Statement")
    end = source.index("## Given Data")
    body = source[start + len("## Statement"):end]
    quoted = [line[1:].strip() if line.startswith(">") else line
              for line in body.splitlines()]
    cleaned = "\n".join(line for line in quoted if not line.startswith("- Source"))
    return render_blocks(cleaned)


def figure_markup(number: int, file_name: str, caption: str, heading: str) -> str:
    """Return the figure block of one figure.

    Args:
        number: The number of the figure in the page.
        file_name: The file name of the figure under ``code/figures/``.
        caption: The caption of the figure.
        heading: The heading that the figure carries as its visible title.

    Returns:
        The figure element with the image as a Base64 data uniform resource identifier.
    """
    payload = base64.b64encode((FIGURE_DIRECTORY / file_name).read_bytes()).decode("ascii")
    return (
        f'<figure id="figure{number}">'
        f'<img alt="{heading}" src="data:image/png;base64,{payload}">'
        f"<figcaption><strong>Figure {number}.</strong> {render_inline(caption)}</figcaption>"
        f"</figure>"
    )


def format_number(value: float) -> str:
    """Return one number with twelve significant digits.

    Args:
        value: The number to format.

    Returns:
        The formatted number, without a trailing zero of an integer value.
    """
    if value == 0.0:
        return "0"
    if abs(value) >= 1.0e-3 and value == int(value):
        return str(int(value))
    return f"{value:.12g}"


def results_table(part_number: int) -> str:
    """Return the table of verified results of one part.

    Args:
        part_number: The number of the part.

    Returns:
        The table element with one row for each verified result.
    """
    path = RESULT_DIRECTORY / f"part{part_number}_results.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    pieces = [
        "<table>",
        "<thead><tr><th>Claim that the script checks</th><th>Computed</th><th>Expected</th>"
        "<th>Difference</th></tr></thead><tbody>",
    ]
    for record in records:
        pieces.append(
            "<tr>"
            f"<td>{render_inline(record['label'])}</td>"
            f"<td class=\"number\">{format_number(record['computed'])}</td>"
            f"<td class=\"number\">{format_number(record['expected'])}</td>"
            f"<td class=\"number\">{record['difference']:.3e}</td>"
            "</tr>"
        )
    pieces.append("</tbody></table>")
    return "".join(pieces)


def final_answer_section() -> str:
    """Return the section that states the six answers.

    Returns:
        The section element with the six limit groups.
    """
    pieces = [
        '<h2 id="answer">Final answer</h2>',
        "<p>The six orders of integration, with the limits that each order needs. Each line is one "
        "answer to the problem, and the value of each line is the same number.</p>",
    ]
    for index, (order, limit_group) in enumerate(FINAL_ANSWERS, start=1):
        pieces.append(
            '<div class="answer">'
            f"<p>Answer {index}, order {order}</p>"
            f'<div class="math-display">$$\\iiint_{{E}} f(x,y,z)\\,dV = {limit_group}$$</div>'
            "</div>"
        )
    pieces.append(
        "<p>Six orders are the six permutations of three variables, so the count is $3! = 6$. "
        "Step 6.2 checks that all six orders return one value for four different integrands.</p>"
    )
    return "".join(pieces)


def build_page() -> str:
    """Build the whole page.

    Returns:
        The text of the composed page.
    """
    pieces = [HEAD_TEMPLATE.format(style=STYLE_BLOCK)]
    pieces.append("<h1>Six iterated integrals for one solid</h1>")
    pieces.append(
        '<p class="subtitle">Stewart, Calculus, Chapter 15.7, Exercise 31. The page derives every '
        "limit from the three defining inequalities, and every number comes from a script that the "
        "page names.</p>"
    )
    figure_counter = 0
    pieces.append("<nav><strong>Contents</strong><ol>")
    for part_number in sorted(PARTS):
        title = extract_heading((STEPS_DIRECTORY / PARTS[part_number][0]).read_text(encoding="utf-8"))
        pieces.append(f'<li><a href="#part{part_number}">{title}</a></li>')
    pieces.append('<li><a href="#answer">Final answer</a></li>')
    pieces.append("</ol></nav>")

    pieces.append('<h2 id="statement">Statement</h2>')
    pieces.append(f'<div class="statement">{read_statement()}</div>')

    for part_number in sorted(PARTS):
        files = PARTS[part_number]
        first_text = (STEPS_DIRECTORY / files[0]).read_text(encoding="utf-8")
        pieces.append(f'<h2 id="part{part_number}">{extract_heading(first_text)}</h2>')
        intro = render_blocks_before_first_step(first_text)
        if intro:
            pieces.append(intro)
        for index, file_name in enumerate(files):
            text = (STEPS_DIRECTORY / file_name).read_text(encoding="utf-8")
            if index == 0 and STEP_HEADING_MARKER in text:
                text = STEP_HEADING_MARKER + text.split(STEP_HEADING_MARKER, 1)[1]
            pieces.append('<div class="step">')
            pieces.append(f"<h3>{extract_step_heading(text)}</h3>")
            pieces.append(render_blocks(text))
            pieces.append("</div>")
        for figure_part, file_name, caption in FIGURES:
            if figure_part != part_number:
                continue
            figure_counter += 1
            pieces.append(figure_markup(figure_counter, file_name, caption, caption.split(".")[0]))
        pieces.append(f'<h3>Verified results of Part {part_number}</h3>')
        pieces.append(results_table(part_number))

    pieces.append(final_answer_section())
    pieces.append(TAIL_TEMPLATE.format())
    return "".join(pieces)


def render_blocks_before_first_step(markdown_text: str) -> str:
    """Render the paragraphs of a step file that come before its step heading.

    Args:
        markdown_text: The source text of the step file.

    Returns:
        The HTML of the introductory paragraphs, or an empty text when the file holds none.
    """
    body = markdown_text.split("\n## ")[0]
    lines = [line for line in body.splitlines() if not line.startswith("# ")]
    return render_blocks("\n".join(lines))


def check_page(page: str) -> None:
    """Check the three properties that the page must hold.

    Args:
        page: The text of the composed page.

    Raises:
        AssertionError: The page holds a control character, an empty code element, or a figure that
            is not embedded.
    """
    control_characters = [character for character in page
                          if ord(character) < 32 and character not in "\n"]
    assert not control_characters, f"the page holds {len(control_characters)} control characters"
    assert "<code></code>" not in page, "the page holds an empty inline code element"
    empty_code = page.count("<code>")
    filled_code = len(re.findall(r"<code>[^<]+</code>", page))
    assert empty_code == filled_code, f"{empty_code - filled_code} code elements are empty"
    for number, file_name, _ in FIGURES:
        payload = base64.b64encode((FIGURE_DIRECTORY / file_name).read_bytes()).decode("ascii")
        assert payload in page, f"figure {number} is not embedded"
    assert page.count("data:image/png;base64,") == len(FIGURES)


def main() -> None:
    """Compose the page, check it, and write the two files."""
    page = build_page()
    check_page(page)
    REPORT_PATH.write_text(page, encoding="utf-8")
    TUTORIAL_PATH.write_text(page, encoding="utf-8")
    print(f"wrote {REPORT_PATH} ({len(page)} characters)")
    print(f"wrote {TUTORIAL_PATH}")
    print(f"control characters: {sum(1 for c in page if ord(c) < 32 and c not in chr(10))}")
    print(f"code elements: {page.count('<code>')}, empty: {page.count('<code></code>')}")
    print(f"figures embedded: {page.count('data:image/png;base64,')}")
    print(f"display blocks: {page.count('math-display')}")


if __name__ == "__main__":
    main()
