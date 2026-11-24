"""Compose the tutorial page from the step files, the check records and the figures.

The page holds the statement, the steps in order, the figures as Base64 data identifiers, the tables of checks and
the final answer. Every number of the page comes from the printed value store of a verification script, and the
script asserts the page before it writes the file.
"""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
"""The problem workspace."""

CODE_DIRECTORY = ROOT / "code"
STEP_DIRECTORY = ROOT / "steps"
OUTPUT_DIRECTORY = CODE_DIRECTORY / "outputs"
FIGURE_DIRECTORY = CODE_DIRECTORY / "figures"
REPORT_PATH = ROOT / "report.html"

PLACEHOLDER_PATTERN = re.compile(r"\{\{([a-z0-9_]+)\}\}")
"""The pattern of a value placeholder inside a step file."""

PART_TITLES = {
    1: "Part 1. Read the region from its four surfaces",
    2: "Part 2. The mass of the solid",
    3: "Part 3. The three moments and the center of mass",
    4: "Part 4. A second route through the shadow",
    5: "Part 5. The answer and its checks",
}
"""The heading of each part."""

STEP_ORDER = [
    "part1_step1.md",
    "part1_step2.md",
    "part1_step3.md",
    "part2_step1.md",
    "part2_step2.md",
    "part2_step3.md",
    "part3_step1.md",
    "part3_step2.md",
    "part3_step3.md",
    "part4_step1.md",
    "part4_step2.md",
    "part5_step1.md",
    "part5_step2.md",
]
"""The order of the step files in the page."""

FIGURE_AFTER_STEP = {
    "part1_step2.md": ("part1_figure1.png", "Figure 1. The solid with its four surfaces, and the section at "
                                             "$z = 0.5$ in red."),
    "part1_step3.md": ("part1_figure2.png", "Figure 2. The three sections of the solid at fixed $z = 0.5$, at fixed "
                                             "$y = 0.5$ and at fixed $x = 0.25$, with the area of each section."),
    "part4_step1.md": ("part4_figure1.png", "Figure 3. The shadow on the plane $z = 0$ and the projection on the "
                                             "plane $y = 0$. The red dot is the center of mass and the green square "
                                             "is the centroid of the projection triangle."),
}
"""The figure of a step, and its caption."""

STATEMENT_HTML = """
<p>The statement of the exercise is a photograph of the book page. The text of the exercise reads as follows.</p>
<p class="statement">Find the mass and the center of mass of the solid $E$ with the given density function
$\\rho$. $E$ is bounded by the parabolic cylinder $z = 1 - y^{2}$ and the planes $x + z = 1$, $x = 0$, and
$z = 0$; $\\rho(x, y, z) = 4$.</p>
"""
"""The statement of the problem as HTML."""


def load_values() -> dict[str, str]:
    """Read the printed value store of every part.

    Returns:
        One dictionary that maps each value key to its printed text.
    """
    values: dict[str, str] = {}
    for path in sorted(OUTPUT_DIRECTORY.glob("part*_summary.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        for key, text in record["values"].items():
            if key in values:
                raise ValueError(f"the value key {key} appears in two parts")
            values[key] = str(text)
    return values


def load_records() -> dict[int, dict[str, object]]:
    """Read the check record of every part.

    Returns:
        One dictionary that maps the part number to its check record.
    """
    records: dict[int, dict[str, object]] = {}
    for path in sorted(OUTPUT_DIRECTORY.glob("part*_summary.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records[int(record["part_number"])] = record
    return records


def inline_markup(text: str) -> str:
    """Convert the inline markup of one text span to HTML.

    Args:
        text: One line of a step file.

    Returns:
        The line with the bold spans and the inline code spans converted.
    """
    parts = re.split(r"(\$[^$]+\$)", text)
    converted: list[str] = []
    for part in parts:
        if part.startswith("$") and part.endswith("$") and len(part) > 1:
            converted.append(part)
            continue
        escaped = html.escape(part, quote=False)
        escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        converted.append(escaped)
    return "".join(converted)


def render_step(markdown_text: str) -> str:
    """Convert the markdown text of one step file to HTML.

    Args:
        markdown_text: The text of the step file.

    Returns:
        The HTML of the step.
    """
    blocks = [block.strip("\n") for block in markdown_text.strip().split("\n\n")]
    pieces: list[str] = []
    for block in blocks:
        lines = [line.rstrip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        if lines[0].startswith("## "):
            pieces.append(f"<h3>{inline_markup(' '.join(lines))}</h3>".replace("## ", "", 1))
            continue
        if lines[0].startswith("$$"):
            joined = " ".join(line.strip() for line in lines)
            pieces.append(f'<div class="math-display">{joined}</div>')
            continue
        if all(line.startswith("- ") for line in lines):
            items: list[str] = []
            for line in lines:
                if line.startswith("- "):
                    items.append(line[2:].strip())
                else:
                    items[-1] = items[-1] + " " + line.strip()
            body = "".join(f"<li>{inline_markup(item)}</li>" for item in items)
            pieces.append(f"<ul>{body}</ul>")
            continue
        items = []
        for line in lines:
            if line.startswith("- "):
                items.append(("item", line[2:].strip()))
            elif items and items[-1][0] == "item":
                items.append(("item", items[-1][1] + " " + line.strip()))
                items.pop(-2)
            else:
                items.append(("text", line.strip()))
        merged: list[str] = []
        current: list[str] = []
        for kind, text in items:
            if kind == "item":
                if current:
                    merged.append(" ".join(current))
                    current = []
                merged.append("-item-" + text)
            else:
                current.append(text)
        if current:
            merged.append(" ".join(current))
        for entry in merged:
            if entry.startswith("-item-"):
                pieces.append(f"<ul><li>{inline_markup(entry[6:])}</li></ul>")
            else:
                pieces.append(f"<p>{inline_markup(entry)}</p>")
    return "\n".join(pieces)


def figure_html(file_name: str, caption: str) -> str:
    """Build the HTML of one figure with a Base64 image.

    Args:
        file_name: The name of the file under the figures directory.
        caption: The caption of the figure, with no math token outside a math span.

    Returns:
        The HTML of the figure element.
    """
    path = FIGURE_DIRECTORY / file_name
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    safe_caption = html.escape(caption, quote=False)
    return (
        f'<figure><img alt="{safe_caption}" src="data:image/png;base64,{payload}">'
        f"<figcaption>{safe_caption}</figcaption></figure>"
    )


def format_number(value: object) -> str:
    """Format one recorded check value for a table cell.

    Args:
        value: The recorded value, which is a number or a text.

    Returns:
        The text of the cell.
    """
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def check_table(record: dict[str, object]) -> str:
    """Build the table of checks of one part.

    Args:
        record: The check record of the part.

    Returns:
        The HTML of the table and of its heading.
    """
    checks = list(record["checks"])  # type: ignore[arg-type]
    rows: list[str] = []
    for check in checks:
        cells = [
            str(check["name"]),
            f"{format_number(check['computed'])} with {check['first_method']}",
            f"{format_number(check['expected'])} with {check['second_method']}",
            format_number(check["tolerance"]),
            "pass" if check["passed"] else "fail",
        ]
        cells = [html.escape(cell, quote=False) for cell in cells]
        rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
    header = (
        "<tr><th>Compared quantity</th><th>Value from the first method</th>"
        "<th>Value from the second method</th><th>Tolerance</th><th>Result</th></tr>"
    )
    heading = (
        f'<p class="table-heading">Checks of Part {record["part_number"]}: '
        f'{record["pass_count"]} of {len(checks)} checks pass.</p>'
    )
    return heading + f'<table class="checks">{header}{"".join(rows)}</table>'


def build_page() -> str:
    """Build the whole page.

    Returns:
        The HTML of the page.
    """
    values = load_values()
    records = load_records()

    body: list[str] = []
    body.append('<h1>Mass and center of mass of a solid between a parabolic cylinder and three planes</h1>')
    body.append('<p class="subtitle">Exercise 40 of Section 15.7, triple integrals in rectangular coordinates. '
                'Every number of this page comes from a printed value of a verification script.</p>')
    statement_image = base64.b64encode((ROOT / "problem" / "source" / "problem.png").read_bytes()).decode("ascii")
    body.append('<h2>The statement</h2>')
    body.append(STATEMENT_HTML)
    body.append(
        '<figure><img alt="photograph of the exercise" '
        f'src="data:image/png;base64,{statement_image}"><figcaption>The exercise as it appears in the book.'
        "</figcaption></figure>"
    )
    body.append('<h2>The plan</h2>')
    body.append(
        "<p>The solution has five parts. Part 1 reads the region from its four surfaces and derives the shape and "
        "the area of a section at a fixed value of each coordinate. Part 2 integrates the density and confirms the "
        "mass by four routes. Part 3 computes the three moments and divides them by the mass. Part 4 repeats the "
        "whole computation over the shadow of the solid on a coordinate plane. Part 5 collects the answer and tests "
        "it against three wrong values.</p>"
    )

    current_part = 0
    for name in STEP_ORDER:
        part_number = int(name[4])
        if part_number != current_part:
            current_part = part_number
            body.append(f"<h2>{html.escape(PART_TITLES[part_number], quote=False)}</h2>")
        text = (STEP_DIRECTORY / name).read_text(encoding="utf-8")
        text = PLACEHOLDER_PATTERN.sub(lambda match: values[match.group(1)], text)
        rendered = render_step(text)
        body.append(f'<section id="{name.replace(".md", "")}">{rendered}</section>')
        if name in FIGURE_AFTER_STEP:
            file_name, caption = FIGURE_AFTER_STEP[name]
            body.append(figure_html(file_name, caption))
        is_last_of_part = (
            name == STEP_ORDER[-1] or int(STEP_ORDER[STEP_ORDER.index(name) + 1][4]) != part_number
        )
        if is_last_of_part:
            body.append(check_table(records[part_number]))

    body.append("<h2>The answer</h2>")
    body.append(
        '<table class="answer"><tr><th>Quantity</th><th>Exact value</th><th>Decimal value</th></tr>'
        f'<tr><td>Mass of the solid</td><td>{values["p5_mass"]}</td><td>{values["p5_mass_decimal"]}</td></tr>'
        f'<tr><td>Volume of the solid</td><td>{values["p5_volume"]}</td><td>{values["p2_volume_decimal"]}</td></tr>'
        f'<tr><td>Center of mass</td><td>{values["p5_center"]}</td><td>{values["p5_center_decimal"]}</td></tr>'
        "</table>"
    )
    body.append(
        "<p>The center of mass lies in the plane $y = 0$, because the solid and the density are symmetric under the "
        "reflection $y \\to -y$.</p>"
    )
    body.append('<h2>How the checks work</h2>')
    body.append(
        "<p>Each part has one script under the code directory. Each script compares a value that one method "
        "computes with a value that a different method computes, and it prints both values beside the tolerance. "
        "A comparison of two values of the same method is a failure of the check layer, and the recorder of "
        "<code>code/check_report.py</code> raises an error in that case.</p>"
    )

    page = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Mass and center of mass of a solid bounded by a parabolic cylinder</title>\n"
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" '
        'onload="renderMathInElement(document.body, {delimiters: [{left: \'$$\', right: \'$$\', display: true}, '
        "{left: '$', right: '$', display: false}]});\"></script>\n"
        "<style>\n" + STYLE_TEXT + "</style>\n</head>\n<body>\n<main>\n" + "\n".join(body) +
        "\n</main>\n</body>\n</html>\n"
    )
    return page


STYLE_TEXT = """
:root { --ink: #1d2129; --muted: #5b6472; --line: #d7dbe2; --accent: #2f4b7c; }
body { margin: 0; background: #f6f7f9; color: var(--ink);
       font-family: Cambria, "Cambria Math", Georgia, serif; font-size: 17px; line-height: 1.62; }
main { max-width: 60rem; margin: 0 auto; padding: 2.4rem 2rem 4rem; background: #ffffff;
       box-shadow: 0 0 0 1px var(--line); }
h1 { font-size: 1.85rem; line-height: 1.25; margin: 0 0 0.4rem; color: var(--accent); }
h2 { font-size: 1.3rem; margin: 2.2rem 0 0.6rem; padding-bottom: 0.25rem; border-bottom: 1px solid var(--line);
     color: var(--accent); }
h3 { font-size: 1.06rem; margin: 1.5rem 0 0.4rem; color: #24303f; }
p { margin: 0.55rem 0; }
p.subtitle { color: var(--muted); font-size: 0.96rem; margin-bottom: 1.2rem; }
p.statement { background: #f2f5fa; border-left: 4px solid var(--accent); padding: 0.7rem 1rem; }
.math-display { margin: 0.9rem 0 0.9rem 1rem; overflow-x: auto; }
code { font-family: Consolas, "Courier New", monospace; font-size: 0.9em; background: #eef1f5;
       padding: 0.05rem 0.3rem; border-radius: 3px; }
figure { margin: 1.2rem 0; text-align: center; }
figure img { max-width: 100%; height: auto; border: 1px solid var(--line); border-radius: 4px; }
figcaption { color: var(--muted); font-size: 0.9rem; margin-top: 0.4rem; }
p.table-heading { font-weight: bold; margin-top: 1.4rem; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; margin: 0.5rem 0 1.2rem; }
th, td { border: 1px solid var(--line); padding: 0.32rem 0.5rem; text-align: left; vertical-align: top; }
th { background: #eaeef5; }
table.answer td, table.answer th { font-size: 0.95rem; }
.katex { font-family: XITS, "XITS Math", Cambria Math, serif; }
""".strip()
"""The style sheet of the page."""


def strip_math_spans(text: str) -> str:
    """Remove every math span from one text.

    Args:
        text: One text of the page.

    Returns:
        The text with every span between two dollar signs removed.
    """
    return re.sub(r"\$\$.*?\$\$", "", re.sub(r"\$[^$]*\$", "", text, flags=re.DOTALL))


def assert_page(page: str, values: dict[str, str]) -> list[str]:
    """Check the page before the write.

    Args:
        page: The HTML of the page.
        values: The printed value store.

    Returns:
        One line for each satisfied assertion.
    """
    lines: list[str] = []
    if "[CORRECT_VALUE]" in page or "[WRONG_VALUE]" in page:
        raise ValueError("a placeholder of a wrong value reached the page")
    lines.append("no wrong-value placeholder")
    leftover = PLACEHOLDER_PATTERN.findall(page)
    if leftover:
        raise ValueError(f"a value placeholder reached the page: {leftover}")
    lines.append("no value placeholder")
    control = [character for character in page if ord(character) < 32 and character != "\n"]
    if control:
        raise ValueError(f"the page holds {len(control)} control characters")
    lines.append("no control character")
    used = set(re.findall(r"\{\{([a-z0-9_]+)\}\}", "\n".join(
        (STEP_DIRECTORY / name).read_text(encoding="utf-8") for name in STEP_ORDER
    )))
    missing = sorted(key for key in used if key not in values)
    if missing:
        raise ValueError(f"a step file names a missing value: {missing}")
    lines.append(f"all {len(used)} value keys of the step files exist")
    odd_lines = [line for line in page.split("\n") if line.count("$") % 2 == 1]
    if odd_lines:
        raise ValueError(f"a line holds an odd count of dollar signs: {odd_lines[0][:120]}")
    lines.append("no line with an odd count of dollar signs")
    for cell in re.findall(r"<td>(.*?)</td>", page, flags=re.DOTALL):
        plain = strip_math_spans(cell)
        if "\\" in plain or "<" in plain:
            raise ValueError(f"a table cell holds a math token outside a math span: {cell[:120]}")
    for caption in re.findall(r"<figcaption>(.*?)</figcaption>", page, flags=re.DOTALL):
        plain = strip_math_spans(caption)
        if "\\" in plain or "<" in plain:
            raise ValueError(f"a caption holds a math token outside a math span: {caption[:120]}")
    lines.append("no math token outside a math span in a cell or a caption")
    for item in re.findall(r"<li>(.*?)</li>", page, flags=re.DOTALL):
        plain = re.sub(r"<[^>]+>", "", item).strip()
        if plain and not plain.endswith("."):
            raise ValueError(f"a list item does not end with a full stop: {plain[:120]}")
    lines.append("every list item ends with a full stop")
    for paragraph in re.findall(r"<p>(.*?)</p>", page, flags=re.DOTALL):
        plain = re.sub(r"<[^>]+>", "", paragraph).strip()
        if plain and plain[0].islower():
            raise ValueError(f"a paragraph begins with a lower-case word: {plain[:120]}")
    lines.append("no paragraph begins with a lower-case word")
    return lines


def main() -> None:
    """Compose the page, assert it and write it."""
    page = build_page()
    values = load_values()
    for line in assert_page(page, values):
        print(f"PAGE CHECK {line}")
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    print(f"REPORT written: {REPORT_PATH} ({len(page)} characters)")


if __name__ == "__main__":
    main()
