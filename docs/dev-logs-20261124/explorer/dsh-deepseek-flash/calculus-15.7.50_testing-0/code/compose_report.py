"""Compose the tutorial page from the step files, the result files, and the figure files.

The composer reads one Markdown file for each step, replaces each placeholder with a value that a
verification script printed, embeds each figure as a Base64 data identifier, and asserts the page
rules before it writes the page: no control character, no unused placeholder, no wrong math
delimiter, and no text that prints raw LaTeX outside a math span.
"""

from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

CODE_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIRECTORY))

import verification_support as support

WORKSPACE_DIRECTORY = CODE_DIRECTORY.parent
STEPS_DIRECTORY = WORKSPACE_DIRECTORY / "steps"
OUTPUTS_DIRECTORY = CODE_DIRECTORY / "outputs"
FIGURES_DIRECTORY = CODE_DIRECTORY / "figures"
REPORT_PATH = WORKSPACE_DIRECTORY / "report.html"
TUTORIAL_PATH = WORKSPACE_DIRECTORY / "tutorial.html"
PLACEHOLDER_PATTERN = re.compile(r"\{\{([a-zA-Z0-9_]+)(?:\|(\d+))?\}\}")
CONTROL_CHARACTER_PATTERN = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f]")
MATH_SPAN_PATTERN = re.compile(r"\$[^$]*\$")
CODE_PATTERN = re.compile(r"`([^`]+)`")
BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")
STEP_FILE_PATTERN = re.compile(r"^part(\d+)_step(\d+)\.md$")
RELATIVE_DIFFERENCE_LIMIT = support.RELATIVE_DIFFERENCE_LIMIT
SAMPLE_SIGMA_LIMIT = support.MONTE_CARLO_STANDARD_ERROR_FACTOR
FIGURE_NUMBERS = {"part1_figure1": 1, "part1_figure2": 2, "part3_figure1": 3}
QUANTITY_LABELS = {
    "mass": r"$M$",
    "x rho": r"$\int_{E} x\rho\,dV$",
    "y rho": r"$\int_{E} y\rho\,dV$",
    "z rho": r"$\int_{E} z\rho\,dV$",
    "inertia": r"$I_{z}$",
}

KATEX_STYLE = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
KATEX_SCRIPT = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"
KATEX_AUTORENDER = ("https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/"
                    "auto-render.min.js")

PAGE_STYLE = """
  :root { color-scheme: light; }
  body { font-family: Cambria, "Cambria Math", Georgia, serif; font-size: 17px; line-height: 1.62;
         color: #14181d; background: #fbfaf7; margin: 0 auto; max-width: 60rem;
         padding: 2.2rem 1.6rem 5rem 1.6rem; }
  h1 { font-size: 1.95rem; line-height: 1.25; margin: 0 0 0.4rem 0; }
  h2 { font-size: 1.42rem; margin: 2.6rem 0 0.7rem 0; border-bottom: 1px solid #d9d4c8;
       padding-bottom: 0.25rem; }
  h3 { font-size: 1.12rem; margin: 1.9rem 0 0.5rem 0; color: #22303c; }
  p { margin: 0.7rem 0; }
  .subtitle { color: #4a5563; font-size: 0.95rem; margin-bottom: 1.6rem; }
  blockquote { margin: 1.1rem 0; padding: 0.8rem 1.1rem; background: #f2eee4;
               border-left: 4px solid #b9a97f; }
  table { border-collapse: collapse; margin: 1.1rem 0; font-size: 0.94rem; width: 100%; }
  caption { caption-side: top; text-align: left; font-size: 0.9rem; color: #4a5563;
            padding-bottom: 0.35rem; }
  th, td { border: 1px solid #d5cfc1; padding: 0.32rem 0.55rem; text-align: right; }
  th { background: #efe9dc; text-align: center; }
  th:first-child, td:first-child { text-align: left; }
  figure { margin: 1.5rem 0; text-align: center; }
  figure img { max-width: 100%; height: auto; border: 1px solid #ded8cb; background: #ffffff; }
  figcaption { font-size: 0.9rem; color: #4a5563; margin-top: 0.5rem; text-align: left; }
  ul { margin: 0.6rem 0 0.6rem 1.2rem; padding: 0; }
  li { margin: 0.3rem 0; }
  code { font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 0.88em;
         background: #efece4; padding: 0.05rem 0.3rem; border-radius: 3px; }
  .katex { font-family: "XITS Math", "Cambria Math", Cambria, serif; }
  .katex-display { margin: 1rem 0; }
"""

PAGE_SCRIPT = """
  document.addEventListener("DOMContentLoaded", function () {
    renderMathInElement(document.body, {
      delimiters: [
        {left: "$$", right: "$$", display: true},
        {left: "$", right: "$", display: false}
      ],
      throwOnError: false
    });
  });
"""


def load_results() -> dict[str, object]:
    """Return every value that the verification scripts printed, merged in file-name order."""
    merged: dict[str, object] = {}
    for path in sorted(OUTPUTS_DIRECTORY.glob("*.json")):
        content = json.loads(path.read_text(encoding="utf-8"))
        for key, value in content.items():
            if key == "checks":
                continue
            if key in merged:
                known = merged[key]
                if isinstance(known, str) and isinstance(value, str) and known == value:
                    print(f"the key {key} of {path.name} repeats the same printed value")
                    continue
                if isinstance(known, list) and isinstance(value, list):
                    continue
                raise ValueError(f"the key {key} of {path.name} holds a different value")
            merged[key] = value
    merged["part1_checks"] = load_checks(1)
    merged["part2_checks"] = load_checks(2)
    merged["part3_checks"] = load_checks(3)
    merged["part4_checks"] = load_checks(4)
    merged["part5_checks"] = load_checks(5)
    if not merged:
        raise ValueError("no result file exists in code/outputs")
    return merged


def load_results_of(part: int) -> dict[str, object]:
    """Return the whole result file of one part."""
    return json.loads((OUTPUTS_DIRECTORY / f"part{part}_results.json").read_text(encoding="utf-8"))


def load_checks(part: int) -> dict[str, object]:
    """Return the check summary of one part."""
    return dict(load_results_of(part)["checks"])


def format_value(name: str, value: object, digits: str | None) -> str:
    """Return the printed form of one value, with the requested count of decimals for a float."""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        width = int(digits) if digits is not None else 6
        return f"{float(value):.{width}f}"
    if isinstance(value, str):
        return value
    raise ValueError(f"the value of {name} is not a scalar: {type(value).__name__}")


def substitute(text: str, results: dict[str, object]) -> str:
    """Replace every placeholder of one step text with the value that a script printed."""

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in results:
            raise KeyError(f"the placeholder {name} has no result")
        return format_value(name, results[name], match.group(2))

    return PLACEHOLDER_PATTERN.sub(replace, text)


def escape_outside_math(text: str) -> str:
    """Escape the characters that HTML reserves, and keep each math span untouched."""
    pieces = text.split("$")
    escaped = []
    for index, piece in enumerate(pieces):
        if index % 2 == 1:
            escaped.append(piece)
        else:
            escaped.append(piece.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return "$".join(escaped)


def render_inline(text: str) -> str:
    """Render one line of step text as inline HTML: escape, then code spans, then bold spans."""
    pieces = text.split("$")
    for index, piece in enumerate(pieces):
        if index % 2 == 1:
            continue
        escaped = piece.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        escaped = CODE_PATTERN.sub(lambda match: f"<code>{match.group(1)}</code>", escaped)
        escaped = BOLD_PATTERN.sub(lambda match: f"<strong>{match.group(1)}</strong>", escaped)
        pieces[index] = escaped
    return "$".join(pieces)


def quantity_label(name: str) -> str:
    """Return the math label of one quantity that the result files name in plain words."""
    if name not in QUANTITY_LABELS:
        raise KeyError(f"the quantity {name} has no label")
    return QUANTITY_LABELS[name]


def render_table(caption: str, header: list[str], rows: list[list[str]]) -> str:
    """Render one HTML table from a caption, a header row, and body rows."""
    parts = ["<table>", f"<caption>{render_inline(caption)}</caption>", "<thead><tr>"]
    parts.extend(f"<th>{render_inline(cell)}</th>" for cell in header)
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        parts.extend(f"<td>{render_inline(cell)}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def scientific_latex(text: str) -> str:
    """Return a printed number in scientific notation as a LaTeX expression."""
    mantissa, exponent = text.split("e")
    if float(mantissa) == 0.0:
        return "0"
    return (mantissa + " \\times 10^{" + str(int(exponent)) + "}")


def inner_table(caption: str, rows: list[dict[str, str]]) -> str:
    """Render the table of an inner integral that three routes compute."""
    body = [[f"${row['y']}$", f"${row['formula']}$", f"${row['direct']}$", f"${row['gauss']}$",
             f"${scientific_latex(row['difference'])}$"] for row in rows]
    return render_table(caption, ["$y$", "closed form", "antiderivative", "Gauss rule",
                                  "difference"], body)


def shapes_table(rows: list[dict[str, str]]) -> str:
    """Render the table of the section shape at three values of y."""
    body = [[f"${row['y']}$", f"${row['distinct_corners']}$", f"${row['width']}$",
             f"${row['height']}$", f"${row['area']}$", row["shape"]] for row in rows]
    return render_table("The section at three values of $y$: the corners, the size, and the shape.",
                        ["$y$", "distinct corners", "width", "height", "area", "shape"], body)


def numerators_table(rows: list[dict[str, str]]) -> str:
    """Render the table of the three numerators of the center of mass."""
    body = [[quantity_label(row["name"]), f"${row['primary']}$", f"${row['alternate']}$",
             f"${row['monte_carlo']}$", f"${row['error']}$", f"${row['sigma']}$"] for row in rows]
    return render_table("Each numerator from its closed form, from the order $dz\\,dy\\,dx$, and "
                        "from a uniform sample.",
                        ["numerator", "closed form", "second order", "sample", "sample error",
                         "deviation"], body)


def final_table(rows: list[dict[str, str]]) -> str:
    """Render the table that cross-checks the printed values of the five parts."""
    body = [[quantity_label(row["name"]), f"${row['printed']}$", f"${row['alternate']}$",
             f"${row['relative_difference_latex']}$", f"${row['monte_carlo']}$",
             f"${row['error']}$",
             f"${row['sigma']}$"] for row in rows]
    return render_table("Each printed value against the order $dz\\,dy\\,dx$ and against a fresh "
                        "sample.",
                        ["quantity", "printed value", "second order", "relative difference",
                         "sample", "sample error", "deviation"], body)


def checks_table() -> str:
    """Render the table of the check count of each part."""
    rows = [[f"Part {part}", f"`code/part{part}_verify.py`", f"${load_checks(part)['count']}$"]
            for part in (1, 2, 3, 4, 5)]
    return render_table("The number of checks that each verification script prints.",
                        ["part", "script", "checks"], rows)


def figure_element(name: str, caption: str) -> str:
    """Return a figure element with the image embedded as a Base64 data identifier."""
    path = FIGURES_DIRECTORY / f"{name}.png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    if name not in FIGURE_NUMBERS:
        raise ValueError(f"the figure {name} has no number")
    label = f"Figure {FIGURE_NUMBERS[name]}. "
    return (f'<figure><img alt="{name}" src="data:image/png;base64,{encoded}">'
            f"<figcaption>{label}{render_inline(caption)}</figcaption></figure>")


def render_named_table(name: str) -> str:
    """Return the HTML table that the given name selects."""
    if name == "inner_x":
        return inner_table("The inner integral of the mass at three values of $y$.",
                           load_results_of(2)["inner_rows"])
    if name == "inner_iz":
        return inner_table("The inner integral of the moment of inertia at three values of $y$.",
                           load_results_of(4)["inner_rows"])
    if name == "shapes":
        return shapes_table(load_results_of(1)["shape_rows"])
    if name == "numerators":
        return numerators_table(load_results_of(3)["numerator_rows"])
    if name == "final":
        return final_table(load_results_of(5)["rows"])
    if name == "checks":
        return checks_table()
    raise ValueError(f"the table {name} has no builder")


def block_kind(line: str) -> str:
    """Return the kind of one line of a step file."""
    if not line.strip():
        return "blank"
    if line.startswith("## "):
        return "heading"
    if line.startswith("$$"):
        return "display"
    if line.startswith("- "):
        return "list"
    if line.startswith("  ") and line.strip():
        return "continuation"
    if line.startswith("{{figure:"):
        return "figure"
    if line.startswith("{{table:"):
        return "table"
    return "text"


def join_continuations(lines: list[str]) -> list[str]:
    """Join each indented continuation line to the list item or the paragraph above it."""
    joined: list[str] = []
    for line in lines:
        if block_kind(line) == "continuation" and joined:
            joined[-1] = joined[-1].rstrip() + " " + line.strip()
        else:
            joined.append(line.rstrip())
    return joined


def render_step_file(path: Path, results: dict[str, object]) -> str:
    """Render one step file as HTML."""
    text = substitute(path.read_text(encoding="utf-8"), results)
    lines = join_continuations(text.splitlines())
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{render_inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            output.append("<ul>" + "".join(f"<li>{render_inline(item)}</li>"
                                          for item in list_items) + "</ul>")
            list_items.clear()

    for line in lines:
        kind = block_kind(line)
        if kind != "text":
            flush_paragraph()
        if kind != "list":
            flush_list()
        if kind == "blank":
            continue
        if kind == "heading":
            output.append(f"<h3>{render_inline(line[3:].strip())}</h3>")
        elif kind == "display":
            body = line.strip()
            if not (body.startswith("$$") and body.endswith("$$") and len(body) > 4):
                raise ValueError(f"a display line of {path.name} is not on one line: {body}")
            output.append(f'<div class="katex-display">{body}</div>')
        elif kind == "list":
            list_items.append(line[2:].strip())
        elif kind == "figure":
            match = re.fullmatch(r"\{\{figure:([a-zA-Z0-9_]+)\|(.*)\}\}", line.strip())
            if match is None:
                raise ValueError(f"a figure line of {path.name} is malformed: {line}")
            output.append(figure_element(match.group(1), match.group(2)))
        elif kind == "table":
            match = re.fullmatch(r"\{\{table:([a-zA-Z0-9_]+)\}\}", line.strip())
            if match is None:
                raise ValueError(f"a table line of {path.name} is malformed: {line}")
            output.append(render_named_table(match.group(1)))
        else:
            paragraph.append(line.strip())
    flush_paragraph()
    flush_list()
    return "\n".join(output)


def statement_block() -> str:
    """Return the statement of the problem as a quotation block."""
    return (
        "<h2>Statement</h2>\n"
        "<blockquote><p>If $E$ is the solid bounded by the cylinder $y^{2} + z^{2} = 9$ and the "
        "planes $x = 0$, $y = 3x$, and $z = 0$ in the first octant, with the density function "
        "$\\rho(x, y, z) = x^{2} + y^{2}$, find the following quantities, correct to three "
        "decimal places.</p>"
        "<p>(a) The mass. (b) The center of mass. (c) The moment of inertia about the $z$ axis."
        "</p></blockquote>\n"
        "<p>The density has units of mass per unit volume. The three quantities are the "
        "integral of $\\rho$ over $E$, the point $\\left(\\bar{x}, \\bar{y}, \\bar{z}\\right)$ with "
        "$\\bar{x} = \\frac{1}{M}\\int_{E} x\\rho\\,dV$ and similarly for the other two "
        "coordinates, and the integral of $\\left(x^{2} + y^{2}\\right)\\rho$ over $E$.</p>"
    )


def check_page(page: str) -> None:
    """Assert every rule of the composed page, and print the measurement of each rule."""
    control_count = len(CONTROL_CHARACTER_PATTERN.findall(page))
    print(f"control characters = {control_count}")
    assert control_count == 0, "the page holds a control character"

    for placeholder in ("[CORRECT_VALUE]", "[WRONG_VALUE]", "{{"):
        count = page.count(placeholder)
        print(f"occurrences of {placeholder} = {count}")
        assert count == 0, f"the page holds {placeholder}"

    odd_lines = [index + 1 for index, line in enumerate(page.splitlines())
                 if line.count("$") % 2 == 1]
    print(f"lines with an odd number of dollar signs = {len(odd_lines)}")
    assert not odd_lines, f"lines with an odd number of dollar signs: {odd_lines[:5]}"

    math_spans = MATH_SPAN_PATTERN.findall(page)
    print(f"inline math spans = {len(math_spans)}")
    assert math_spans, "the page holds no inline math span"

    empty_code = page.count("<code></code>")
    print(f"empty inline code elements = {empty_code}")
    assert empty_code == 0, "the page holds an empty inline code element"

    for element in ("td", "figcaption"):
        cells = re.findall(rf"<{element}[^>]*>(.*?)</{element}>", page, flags=re.DOTALL)
        for cell in cells:
            plain = re.sub(r"<[^>]+>", "", MATH_SPAN_PATTERN.sub("", cell))
            assert chr(92) not in plain, f"a {element} prints raw LaTeX outside a math span"
            assert "<" not in plain, f"a {element} prints an angle bracket outside a math span"
            assert "`" not in plain, f"a {element} prints a backtick"
            assert "**" not in plain, f"a {element} prints an unrendered bold marker"
        print(f"cells of {element} that keep their text inside math spans = {len(cells)}")

    stripped = re.sub(r"<[^>]+>", "", MATH_SPAN_PATTERN.sub("", page))
    print(f"backticks in the page = {stripped.count('`')}")
    assert stripped.count("`") == 0, "the page prints a backtick"
    print(f"unrendered bold markers in the page = {stripped.count('**')}")
    assert stripped.count("**") == 0, "the page prints an unrendered bold marker"
    bold_elements = page.count("<strong>")
    print(f"bold labels in the page = {bold_elements}")
    assert bold_elements >= 20, "the page holds fewer bold labels than the steps hold"
    code_elements = page.count("<code>")
    print(f"inline code elements in the page = {code_elements}")
    assert code_elements >= 5, "the page holds fewer script names than the steps cite"

    list_items = re.findall(r"<li>(.*?)</li>", page, flags=re.DOTALL)
    bad_items = [item[:60] for item in list_items if not item.rstrip().endswith(".")]
    print(f"list items = {len(list_items)}, items without a full stop = {len(bad_items)}")
    assert not bad_items, f"list items without a full stop: {bad_items[:3]}"

    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", page, flags=re.DOTALL)
    lower_starts = []
    for paragraph in paragraphs:
        plain = re.sub(r"<[^>]+>", "", paragraph).strip()
        plain = plain.lstrip("$").strip()
        if plain and plain[0].islower():
            lower_starts.append(plain[:40])
    print(f"paragraphs = {len(paragraphs)}, paragraphs that start with a lower-case word ="
          f" {len(lower_starts)}")
    assert not lower_starts, f"paragraphs that start with a lower-case word: {lower_starts[:3]}"

    data_identifiers = page.count("data:image/png;base64,")
    print(f"embedded figures = {data_identifiers}")
    assert data_identifiers == 3, "the page does not embed three figures"
    print(f"tables = {page.count('<table>')}")
    assert page.count("<table>") >= 5, "the page holds fewer tables than the tutorial needs"
    assert KATEX_AUTORENDER in page and "renderMathInElement" in page, "the math renderer is absent"

    final = load_results_of(5)
    worst_relative = max(float(row["relative_difference"]) for row in final["rows"])
    worst_sigma = float(final["worst_sigma"])
    print(f"largest relative difference of the cross-check = {worst_relative:.3e} against the"
          f" limit {RELATIVE_DIFFERENCE_LIMIT:.1e}")
    print(f"largest sample deviation of the cross-check = {worst_sigma:.3f} against the limit"
          f" {SAMPLE_SIGMA_LIMIT:.1f}")
    assert worst_relative < RELATIVE_DIFFERENCE_LIMIT, "a cross-check exceeds the limit"
    assert worst_sigma < SAMPLE_SIGMA_LIMIT, "a sample route exceeds the sigma limit"

    tracked_relative = float(final["worst_relative_difference"])
    print(f"the largest relative difference that the script tracked = {tracked_relative:.3e}")
    assert abs(tracked_relative - worst_relative) <= max(1.0e-18, 1.0e-6 * worst_relative), (
        "the tracked worst relative difference disagrees with the worst row of the table")
    tracked_limit = float(final["relative_difference_limit"])
    print(f"the limit that the script printed = {tracked_limit:.1e} against the limit of the"
          f" composer {RELATIVE_DIFFERENCE_LIMIT:.1e}")
    assert tracked_limit == RELATIVE_DIFFERENCE_LIMIT, "the two limits disagree"


def compose() -> str:
    """Build the whole page and check every rule of the page."""
    results = load_results()
    step_paths = sorted(STEPS_DIRECTORY.glob("part*_step*.md"),
                        key=lambda item: tuple(int(value) for value in
                                               STEP_FILE_PATTERN.match(item.name).groups()))
    if not step_paths:
        raise ValueError("no step file exists")
    body: list[str] = [statement_block()]
    for path in step_paths:
        number = STEP_FILE_PATTERN.match(path.name)
        body.append(render_step_file(path, results))
        print(f"rendered {path.name} for part {number.group(1)} step {number.group(2)}")
    page = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Problem 25: mass, center of mass, and moment of inertia</title>\n"
        f'<link rel="stylesheet" href="{KATEX_STYLE}">\n'
        f"<style>{PAGE_STYLE}</style>\n</head>\n<body>\n"
        "<h1>Problem 25: the mass, the center of mass, and the moment of inertia of a solid</h1>\n"
        '<p class="subtitle">A verified tutorial. Each numerical claim holds the name of the script '
        "that checks the claim.</p>\n"
        + "\n".join(body)
        + "\n</body>\n"
        f'<script src="{KATEX_SCRIPT}"></script>\n'
        f'<script src="{KATEX_AUTORENDER}"></script>\n'
        f"<script>{PAGE_SCRIPT}</script>\n</html>\n"
    )
    check_page(page)
    return page


def main() -> None:
    """Compose the page, write both copies, and report the size of each file."""
    page = compose()
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    TUTORIAL_PATH.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {REPORT_PATH} with {len(page)} characters")
    print(f"wrote {TUTORIAL_PATH} with {len(page)} characters")


if __name__ == "__main__":
    main()
