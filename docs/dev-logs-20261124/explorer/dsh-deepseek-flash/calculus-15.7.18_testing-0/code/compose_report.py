"""Compose the tutorial page of the session from the step files and the records of the checks.

The page takes every number from a JSON record that a verification script writes, so no numeral of
the page is typed by hand.  The composed page holds the statement, the steps in order, the figures
as base64 data resources, the tables of the limits and of the checks, and the answer of each part.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path


PRODUCT_DIRECTORY = Path(__file__).resolve().parent.parent
"""Directory of the product page."""

CODE_DIRECTORY = Path(__file__).resolve().parent
"""Directory of the product code."""

STEP_DIRECTORY = PRODUCT_DIRECTORY / "steps"
"""Directory of the step files."""

OUTPUT_DIRECTORY = CODE_DIRECTORY / "outputs"
"""Directory of the JSON records of the four parts."""

FIGURE_DIRECTORY = CODE_DIRECTORY / "figures"
"""Directory of the rendered figures."""

REPORT_PATH = PRODUCT_DIRECTORY / "report.html"
"""Path of the composed page."""

REQUIREMENTS_PATH = CODE_DIRECTORY / "requirements.txt"
"""Path of the file that holds the version of each package."""

KATEX_BASE_URL = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
"""Address of the KaTeX style sheet and script."""

KATEX_VERSION = "0.16.11"
"""Version of KaTeX that renders the mathematics of the page."""

PART_TITLES = {
    1: "Part 1: the solid and its three projections",
    2: "Part 2: the limits of one integration order",
    3: "Part 3: the value of the integral",
    4: "Part 4: a check with a second order and two quadratures",
}
"""Title of each part of the page."""

STEP_FILES = {
    1: ["part1_step1.md", "part1_step2.md", "part1_step3.md"],
    2: ["part2_step1.md", "part2_step2.md", "part2_step3.md"],
    3: ["part3_step1.md", "part3_step2.md"],
    4: ["part4_step1.md", "part4_step2.md"],
}
"""Step file of each part, in the order of the page."""

FIGURES_AFTER_STEP = {
    "part1_step2.md": ["part1_figure1.png", "part1_figure2.png"],
    "part1_step3.md": ["part1_figure3.png"],
    "part2_step1.md": ["part2_figure1.png"],
    "part3_step2.md": ["part3_figure1.png"],
}
"""Figures that follow one step file."""

FIGURE_NUMBERS = {
    "part1_figure1.png": 1,
    "part1_figure2.png": 2,
    "part1_figure3.png": 3,
    "part2_figure1.png": 4,
    "part3_figure1.png": 5,
}
"""Number of each figure in the page."""

FIGURE_CAPTIONS = {
    "part1_figure1.png": (
        "The solid $E$: the wall of the cylinder $y^{2} + z^{2} = 9$, the quarter disk on the plane "
        "$x = 0$, the plane $y = 3x$ and the base on the plane $z = 0$."
    ),
    "part1_figure2.png": (
        "The three projections with their areas: $\\dfrac{9\\pi}{4}$ on the plane $x = 0$, "
        "$\\dfrac{3\\pi}{4}$ on the plane $y = 0$ and $\\dfrac{3}{2}$ on the plane $z = 0$."
    ),
    "part1_figure3.png": (
        "The section at $y = {{p2_demo_height}}$ is a {{p1_slice_y_kind}} with the area "
        "${{p1_slice_y_area}}$, and the section at $z = {{p2_demo_height}}$ is a "
        "{{p1_slice_z_kind}} with the area ${{p1_slice_z_area}}$."
    ),
    "part2_figure1.png": (
        "The limit of $z$ at $y = {{p2_demo_height}}$ is ${{p2_demo_z_high}}$, and the limit of $x$ "
        "at the same $y$ is ${{p2_demo_x_high}}$."
    ),
    "part3_figure1.png": (
        "The outer integrand with the area ${{p3_answer_latex}}$, and its antiderivative, whose "
        "change from zero to three is the same value."
    ),
}
"""Caption of each figure."""

CONTROL_CHARACTER_LIMIT = 0
"""Number of control characters that the composed page may hold."""

TABLE_OF_CHECKS_HEADER = """<table>
<thead>
<tr><th>Part</th><th>Script</th><th>Checks</th><th>Passed</th></tr>
</thead>
<tbody>
"""
"""Opening lines of the table of the checks."""


def read_json(name: str) -> dict[str, object]:
    """Return one JSON record of the output directory.

    Args:
        name: File name of the record.
    """
    return json.loads((OUTPUT_DIRECTORY / name).read_text(encoding="utf-8"))


def collect_facts() -> dict[str, str]:
    """Return every value that the page interpolates, taken from the records of the four parts."""
    facts: dict[str, str] = {}
    for number in (1, 2, 3, 4):
        values = read_json(f"part{number}_values.json")
        for key, value in values.items():
            if isinstance(value, str):
                facts[key] = value
    rows = read_json("part1_values.json")["p1_shape_rows"]
    if not isinstance(rows, list):
        raise TypeError("the shape rows of Part 1 are not a list")
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("one shape row of Part 1 is not an object")
        parameter = row["parameter"]
        value = row["value"]
        if parameter == "y" and value == "0.000":
            facts["p1_end_y0_kind"] = row["kind"]
        elif parameter == "y" and value == "1.500":
            facts["p1_slice_y_kind"] = row["kind"]
            facts["p1_slice_y_area"] = row["area"]
        elif parameter == "y" and value == "3.000":
            facts["p1_end_y3_kind"] = row["kind"]
        elif parameter == "z" and value == "1.500":
            facts["p1_slice_z_kind"] = row["kind"]
            facts["p1_slice_z_area"] = row["area"]
        elif parameter == "z" and value == "3.000":
            facts["p1_end_z3_kind"] = row["kind"]
    total = 0
    for number in (1, 2, 3, 4):
        record = read_json(f"part{number}_checks.json")
        total = total + int(record["check_count"])
    facts["check_total"] = str(total)
    return facts


def substitute(text: str, facts: dict[str, str]) -> str:
    """Replace every fact placeholder of one text block.

    Args:
        text: Text that may hold a placeholder of the form two braces around a key.
        facts: Value of each placeholder key.
    """
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in facts:
            raise KeyError(f"the page uses the unknown placeholder {key}")
        return facts[key]

    return re.sub(r"\{\{([a-z0-9_]+)\}\}", replace, text)


def escape_text(text: str) -> str:
    """Escape the two characters that would break the page markup.

    Args:
        text: One line of natural language or mathematics.
    """
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text: str) -> str:
    """Convert one line of text to inline markup and keep each mathematics span as it is.

    Args:
        text: One line without a block marker.
    """
    escaped = escape_text(text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def render_blocks(text: str) -> str:
    """Convert one step file to the body of a section.

    Args:
        text: Full text of one step file.
    """
    lines = text.split("\n")
    output: list[str] = []
    paragraph: list[str] = []
    items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    def flush_items() -> None:
        if items:
            output.append("<ul>")
            for item in items:
                output.append("<li>" + inline(item) + "</li>")
            output.append("</ul>")
            items.clear()

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_items()
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            flush_items()
            output.append("<h3>" + inline(stripped[2:]) + "</h3>")
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            flush_items()
            output.append("<h4>" + inline(stripped[3:]) + "</h4>")
            continue
        if stripped.startswith("$$"):
            flush_paragraph()
            flush_items()
            output.append('<div class="display">' + inline(stripped) + "</div>")
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            items.append(stripped[2:].strip())
            continue
        if raw.startswith("  ") and items:
            items[-1] = items[-1] + " " + stripped
            continue
        if items:
            flush_items()
        paragraph.append(stripped)
    flush_paragraph()
    flush_items()
    return "\n".join(output)


def image_element(file_name: str, facts: dict[str, str]) -> str:
    """Return the markup of one figure with its caption.

    Args:
        file_name: Name of the portable network graphic file of the figure.
        facts: Value of each placeholder key.
    """
    payload = base64.b64encode((FIGURE_DIRECTORY / file_name).read_bytes()).decode("ascii")
    number = FIGURE_NUMBERS[file_name]
    caption = escape_text(substitute(FIGURE_CAPTIONS[file_name], facts))
    return (
        f'<figure id="figure-{number}">'
        f'<img alt="figure {number}" src="data:image/png;base64,{payload}">'
        f"<figcaption><strong>Figure {number}.</strong> {caption}</figcaption>"
        "</figure>"
    )


def build_order_table(facts: dict[str, str]) -> str:
    """Return the table of the six integration orders.

    Args:
        facts: Value of each placeholder key.
    """
    rows = read_json("part2_values.json")["p2_order_rows"]
    if not isinstance(rows, list):
        raise TypeError("the order rows of Part 2 are not a list")
    lines = [
        "<table>",
        "<thead>",
        "<tr><th>Order</th><th>Outer limit</th><th>Middle limit</th><th>Inner limit</th>"
        "<th>Volume</th></tr>",
        "</thead>",
        "<tbody>",
    ]
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("one order row is not an object")
        lines.append(
            "<tr>"
            + f"<td>${escape_text(str(row['order']).replace(' ', chr(92) + ', '))}$</td>"
            + f"<td>${escape_text(str(row['outer']))}$</td>"
            + f"<td>${escape_text(str(row['middle']))}$</td>"
            + f"<td>${escape_text(str(row['inner']))}$</td>"
            + f"<td>${row['volume']}$</td>"
            + "</tr>"
        )
    lines.extend(["</tbody>", "</table>"])
    return "\n".join(lines)


def build_check_table() -> str:
    """Return the table of the checks of the four parts."""
    lines = [TABLE_OF_CHECKS_HEADER.rstrip("\n")]
    for number in (1, 2, 3, 4):
        record = read_json(f"part{number}_checks.json")
        lines.append(
            f"<tr><td>Part {number}</td><td><code>code/part{number}_verify.py</code></td>"
            f"<td>{record['check_count']}</td><td>{record['passed_count']}</td></tr>"
        )
    lines.extend(["</tbody>", "</table>"])
    return "\n".join(lines)


def page_head() -> str:
    """Return the head of the page with the style sheet of the page and of the mathematics."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Triple integral of z over a cylinder cut by two planes</title>
<link rel="stylesheet" href="{KATEX_BASE_URL}/katex.min.css">
<script defer src="{KATEX_BASE_URL}/katex.min.js"></script>
<script defer src="{KATEX_BASE_URL}/contrib/auto-render.min.js"></script>
<style>
  body {{ font-family: Cambria, "Cambria Math", Georgia, serif; line-height: 1.55;
         max-width: 52rem; margin: 0 auto; padding: 2rem 1.2rem 4rem; color: #1c1c1c; }}
  h1 {{ font-size: 1.7rem; line-height: 1.3; margin-bottom: 0.4rem; }}
  h2 {{ font-size: 1.3rem; margin-top: 2.4rem; border-bottom: 1px solid #d8d8d8;
        padding-bottom: 0.3rem; }}
  h3 {{ font-size: 1.08rem; margin-top: 1.6rem; }}
  h4 {{ font-size: 0.98rem; margin: 1.1rem 0 0.2rem; color: #444; text-transform: none; }}
  p, li {{ font-size: 1rem; }}
  code {{ font-family: Consolas, "Courier New", monospace; font-size: 0.92rem;
          background: #f3f3f3; padding: 0.05rem 0.25rem; border-radius: 3px; }}
  .display {{ margin: 0.9rem 0; overflow-x: auto; }}
  figure {{ margin: 1.4rem 0; }}
  figure img {{ width: 100%; height: auto; border: 1px solid #e2e2e2; }}
  figcaption {{ font-size: 0.9rem; color: #444; margin-top: 0.4rem; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.92rem; }}
  th, td {{ border: 1px solid #d8d8d8; padding: 0.32rem 0.5rem; text-align: left; }}
  th {{ background: #f5f5f5; }}
  .answer {{ border-left: 4px solid #2f6b2a; background: #f4f8f2; padding: 0.8rem 1rem;
             margin: 1.2rem 0; }}
  .katex {{ font-family: "XITS Math", "XITS", "Cambria Math", Cambria, serif; }}
</style>
</head>
<body>
"""


def page_foot() -> str:
    """Return the tail of the page, which renders every mathematics span after the load."""
    return """<script>
document.addEventListener("DOMContentLoaded", function () {
  renderMathInElement(document.body, {
    delimiters: [
      {left: "$$", right: "$$", display: true},
      {left: "$", right: "$", display: false}
    ],
    throwOnError: false
  });
});
</script>
</body>
</html>
"""


def compose_sections(facts: dict[str, str]) -> str:
    """Return the markup of the four parts with their steps and figures.

    Args:
        facts: Value of each placeholder key.
    """
    blocks: list[str] = []
    for number, file_names in STEP_FILES.items():
        blocks.append(f"<h2>{PART_TITLES[number]}</h2>")
        for file_name in file_names:
            text = (STEP_DIRECTORY / file_name).read_text(encoding="utf-8")
            blocks.append(render_blocks(substitute(text, facts)))
            for figure in FIGURES_AFTER_STEP.get(file_name, []):
                blocks.append(image_element(figure, facts))
    return "\n".join(blocks)


def check_page(page: str, facts: dict[str, str]) -> list[str]:
    """Assert every property that the page must hold and return the report lines.

    Args:
        page: Full text of the composed page.
        facts: Value of each placeholder key.
    """
    report: list[str] = []
    controls = [character for character in page if ord(character) < 32 and character != "\n"]
    if len(controls) != CONTROL_CHARACTER_LIMIT:
        raise AssertionError(f"the page holds {len(controls)} control characters")
    report.append(f"control characters: {len(controls)}")

    for token in ("[WRONG" + "_VALUE]", "[CORRECT" + "_VALUE]"):
        if token in page:
            raise AssertionError(f"the page holds the placeholder {token}")
    template = re.findall(r"\{\{[a-z0-9_]+\}\}", page)
    if template:
        raise AssertionError(f"{len(template)} placeholder templates stayed in the page")
    report.append("placeholders: 0")

    odd = 0
    for line in page.split("\n"):
        if line.count("$") % 2 != 0:
            odd = odd + 1
    if odd != 0:
        raise AssertionError(f"{odd} lines hold an odd number of dollar signs")
    report.append(f"lines with an odd number of math delimiters: {odd}")

    if "<code></code>" in page:
        raise AssertionError("the page holds an empty inline code element")
    code_names = re.findall(r"<code>([^<]*)</code>", page)
    report.append(f"inline code elements: {len(code_names)}, empty: 0")

    bare_item = [item for item in re.findall(r"<li>(.*?)</li>", page) if not item.rstrip().endswith(".")]
    if bare_item:
        raise AssertionError(f"{len(bare_item)} list items do not end with a full stop")
    report.append("list items that end with a full stop: all")

    lower_paragraph = re.findall(r"<p>([a-z])", page)
    if lower_paragraph:
        raise AssertionError(f"{len(lower_paragraph)} paragraphs start with a lower case letter")
    report.append("paragraphs that start with a lower case letter: 0")

    cells = re.findall(r"<t[dh]>(.*?)</t[dh]>", page)
    bad_cells = 0
    for cell in cells:
        plain = re.sub(r"\$[^$]*\$", "", cell)
        plain = re.sub(r"<code>[^<]*</code>", "", plain)
        if "\\" in plain or "<" in plain:
            bad_cells = bad_cells + 1
    if bad_cells != 0:
        raise AssertionError(f"{bad_cells} table cells hold mathematics outside a math span")
    report.append(f"table cells: {len(cells)}, cells with loose mathematics: {bad_cells}")

    captions = re.findall(r"<figcaption>(.*?)</figcaption>", page)
    bad_captions = 0
    for caption in captions:
        plain = re.sub(r"\$[^$]*\$", "", caption)
        if "\\" in plain or "<p>" in plain:
            bad_captions = bad_captions + 1
    if bad_captions != 0:
        raise AssertionError(f"{bad_captions} captions hold mathematics outside a math span")
    report.append(f"captions: {len(captions)}, captions with loose mathematics: {bad_captions}")

    unused = [key for key in facts if "{{" + key + "}}" in page]
    if unused:
        raise AssertionError(f"{len(unused)} placeholders stayed in the page")
    report.append(f"facts interpolated: {len(facts)}")
    return report


def main() -> None:
    """Compose the page, assert its properties and write it."""
    facts = collect_facts()
    statement = (
        "<p>Evaluate $\\iiint_{E} z\\,dV$, where $E$ is the solid bounded by the cylinder "
        "$y^{2} + z^{2} = 9$ and the planes $x = 0$, $y = 3x$ and $z = 0$ in the first octant.</p>"
    )
    answer_box = (
        '<div class="answer">'
        f"<p><strong>Answer.</strong> $\\iiint_{{E}} z\\,dV = {facts['p3_answer_latex']} = "
        f"{facts['p3_answer_decimal']}$.</p>"
        f"<p>The solid has the volume ${facts['p1_volume_latex']}$, and the mean height of a point of "
        f"the solid is ${facts['p3_mean_height_latex']} = {facts['p3_mean_height_decimal']}$.</p>"
        f"<p>The three projections have the areas ${facts['p1_yz_area_latex']}$ on the plane $x = 0$, "
        f"${facts['p1_xz_area_latex']}$ on the plane $y = 0$ and ${facts['p1_xy_area_latex']}$ on the "
        "plane $z = 0$.</p>"
        "</div>"
    )
    body = [
        "<h1>The triple integral of the height over a cylinder cut by two planes</h1>",
        statement,
        answer_box,
        compose_sections(facts),
        "<h2>The six integration orders and their volume</h2>",
        "<p>Every order of Step 2.2 is admissible, and each one gives the volume of the solid. The "
        "table takes every entry from <code>code/part2_verify.py</code>.</p>",
        build_order_table(facts),
        "<h2>What the checks cover</h2>",
        f"<p>The four scripts of the session run {facts['check_total']} checks in total, and every "
        "check passes. One check compares a value that one method computes with a value that a "
        "different method computes.</p>",
        build_check_table(),
        "<p>The environment holds the packages that "
        "<code>code/requirements.txt</code> lists, and every script prints the value that it checks "
        "beside the value that it expects.</p>",
    ]
    page = page_head() + "\n".join(body) + "\n" + page_foot()
    report = check_page(page, facts)
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    for line in report:
        print(line)
    print(f"wrote {REPORT_PATH} with {len(page)} characters")


if __name__ == "__main__":
    main()
