"""Compose report.html from the statement, the steps, the figures, and the check tables.

The composer substitutes every value placeholder from a printed value of a
verification script, so no numeral of the page is typed by hand. It asserts the
page invariants after the composition. Run it with the environment interpreter:
code/.venv/Scripts/python.exe code/compose_report.py
"""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

CODE_DIRECTORY = Path(__file__).resolve().parent
WORKSPACE = CODE_DIRECTORY.parent
STEPS_DIRECTORY = WORKSPACE / "steps"
OUTPUT_DIRECTORY = CODE_DIRECTORY / "outputs"
FIGURE_DIRECTORY = CODE_DIRECTORY / "figures"
PROBLEM_PATH = WORKSPACE / "problem" / "problem.md"
REPORT_PATH = WORKSPACE / "report.html"
TUTORIAL_PATH = WORKSPACE / "tutorial.html"

PLACEHOLDER = re.compile(r"\{\{([a-z0-9_]+)\}\}")
FIGURE_MARKER = re.compile(r"\[\[figure:([a-z0-9_]+)\|(.+?)\]\]")
INLINE_CODE = re.compile(r"`([^`]+)`")
PART_NAMES = {
    "part1": "Part 1. The solid and the limits",
    "part2": "Part 2. Cross sections",
    "part3": "Part 3. The mass",
    "part4": "Part 4. The center of mass",
    "part5": "Part 5. The moment of inertia",
    "part6": "Part 6. The check layer",
}
STYLE = """
    body { font-family: Cambria, "Cambria Math", Georgia, serif; max-width: 60rem; margin: 0 auto;
           padding: 2rem 1.5rem 4rem; color: #1c2733; line-height: 1.55; }
    h1 { font-size: 1.7rem; margin-bottom: 0.2rem; }
    h2 { font-size: 1.35rem; margin-top: 2.4rem; padding-bottom: 0.3rem; border-bottom: 2px solid #9db8d6; }
    h3 { font-size: 1.12rem; margin-top: 1.8rem; color: #1f3b57; }
    h4 { font-size: 1rem; margin: 1rem 0 0.3rem; color: #33506c; letter-spacing: 0.02em; }
    p { margin: 0.45rem 0; }
    .meta { color: #5b6b7c; font-size: 0.92rem; }
    code { font-family: Consolas, "Courier New", monospace; font-size: 0.9rem;
           background: #eef2f7; padding: 0.05rem 0.25rem; border-radius: 3px; }
    figure { margin: 1.4rem 0; }
    figure img { width: 100%; height: auto; border: 1px solid #c7d3e0; border-radius: 4px; }
    figcaption { font-size: 0.92rem; color: #46586b; margin-top: 0.4rem; }
    table { border-collapse: collapse; width: 100%; font-size: 0.92rem; margin: 0.9rem 0 1.6rem; }
    th, td { border: 1px solid #c7d3e0; padding: 0.34rem 0.5rem; text-align: left; vertical-align: top; }
    th { background: #e8eef6; }
    .display-math { margin: 0.8rem 0; overflow-x: auto; }
    .statement { background: #f6f8fb; border-left: 4px solid #9db8d6; padding: 0.8rem 1.1rem; }
    .answer { background: #eef4fb; border: 1px solid #9db8d6; border-radius: 4px; padding: 0.9rem 1.2rem; }
    .katex { font-family: "XITS", "Cambria Math", "Latin Modern Math", serif; }
"""


def load_display() -> tuple[dict[str, str], list[dict]]:
    """Read every summary file of the verification scripts.

    Returns:
        The dictionary of the display values and the list of the summary records
        in the order of the part number.
    """
    display: dict[str, str] = {}
    records: list[dict] = []
    for path in sorted(OUTPUT_DIRECTORY.glob("part*_summary.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records.append(record)
        display.update(record["display"])
    if not records:
        raise AssertionError("no summary file of a verification script")
    return display, records


def substitute(text: str, display: dict[str, str]) -> str:
    """Replace each value placeholder of the text by a printed value.

    Args:
        text: Text with placeholders of the form double brace name double brace.
        display: Dictionary from a placeholder name to the printed value.

    Returns:
        The text with every placeholder replaced.
    """

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in display:
            raise AssertionError(f"placeholder {key} has no printed value")
        return display[key]

    return PLACEHOLDER.sub(replace, text)


def figure_html(name: str, caption: str) -> str:
    """Return the figure element with the image embedded as a data identifier.

    Args:
        name: Stem of the figure file below code/figures.
        caption: Text of the caption.

    Returns:
        The HTML of the figure element.
    """
    path = FIGURE_DIRECTORY / f"{name}.png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    safe_caption = html.escape(caption, quote=False)
    return (
        f'<figure><img alt="{safe_caption}" src="data:image/png;base64,{payload}">'
        f"<figcaption>{safe_caption}</figcaption></figure>"
    )


def inline(text: str) -> str:
    """Wrap each inline code span of a line in a code element.

    Args:
        text: One line of a step file.

    Returns:
        The line with code elements.
    """
    return INLINE_CODE.sub(lambda match: f"<code>{match.group(1)}</code>", text)


def table_html(record: dict) -> str:
    """Return the check table of one part.

    Args:
        record: Summary record of one verification script.

    Returns:
        The HTML table of the checks of that part.
    """
    rows = [
        "<table><thead><tr><th>Check</th><th>Computed</th><th>Expected or bound</th>"
        "<th>Tolerance</th><th>Reason of the comparison</th></tr></thead><tbody>"
    ]
    for check in record["checks"]:
        expected = check.get("expected", check.get("bound"))
        rows.append(
            "<tr><td><em>{}</em></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                check["name"],
                f"{check['computed']:.12g}",
                f"{float(expected):.12g}",
                f"{check['tolerance']:.3g}" if "tolerance" in check else "bound",
                check["reason"],
            )
        )
    rows.append("</tbody></table>")
    return "".join(rows)


def render_blocks(text: str) -> str:
    """Render the block subset of markdown that the step files use.

    Args:
        text: Body of one step file with the placeholders already replaced.

    Returns:
        The HTML of the blocks of that file.
    """
    lines = text.split("\n")
    output: list[str] = []
    paragraph: list[str] = []
    index = 0

    def flush() -> None:
        if paragraph:
            joined = " ".join(part.strip() for part in paragraph)
            output.append(f"<p>{inline(joined)}</p>")
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush()
            index += 1
            continue
        if stripped.startswith("[[figure:"):
            flush()
            match = FIGURE_MARKER.search(stripped)
            if match is None:
                raise AssertionError(f"bad figure marker: {stripped}")
            output.append(figure_html(match.group(1), match.group(2)))
            index += 1
            continue
        if stripped.startswith("# "):
            flush()
            output.append(f'<h2>{inline(stripped[2:])}</h2>')
            index += 1
            continue
        if stripped.startswith("## "):
            flush()
            output.append(f'<h3>{inline(stripped[3:])}</h3>')
            index += 1
            continue
        if stripped.startswith("### "):
            flush()
            output.append(f'<h4>{inline(stripped[4:])}</h4>')
            index += 1
            continue
        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            flush()
            output.append(f'<div class="display-math">{stripped}</div>')
            index += 1
            continue
        if stripped.startswith("- "):
            flush()
            items: list[str] = []
            while index < len(lines):
                current = lines[index]
                if current.strip().startswith("- "):
                    items.append(current.strip()[2:].strip())
                elif current.startswith("  ") and current.strip():
                    items[-1] = items[-1] + " " + current.strip()
                elif not current.strip():
                    if index + 1 < len(lines) and (
                        lines[index + 1].startswith("- ") or lines[index + 1].startswith("  ")
                    ):
                        index += 1
                        continue
                    break
                else:
                    break
                index += 1
            output.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>")
            continue
        paragraph.append(line)
        index += 1
    flush()
    return "\n".join(output)


def statement_html() -> str:
    """Return the statement section, read from the intake file.

    Returns:
        The HTML of the statement section.
    """
    text = PROBLEM_PATH.read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    statement = next(part for part in parts if part.startswith("Statement"))
    body = statement.split("\n", 1)[1]
    blocks = render_blocks(body.strip())
    return f'<section class="statement"><h2>Statement</h2>\n{blocks}</section>'


def assemble(display: dict[str, str], records: list[dict]) -> str:
    """Build the whole page.

    Args:
        display: Dictionary from a placeholder name to a printed value.
        records: Summary records of the verification scripts.

    Returns:
        The HTML text of the page.
    """
    body: list[str] = []
    body.append(
        '<h1>Exercise 47, Section 15.7: a solid between a cylinder and two planes</h1>'
        '<p class="meta">MCMA tutoring session 20261123_092307_tutoring_problem_24. '
        "Every value of this page is printed by one script below <code>code/</code>, and every "
        "mathematical expression is LaTeX source rendered by KaTeX.</p>"
    )
    body.append(statement_html())

    step_paths = sorted(STEPS_DIRECTORY.glob("part*_step*.md"))
    if not step_paths:
        raise AssertionError("no step file")
    for path in step_paths:
        text = substitute(path.read_text(encoding="utf-8"), display)
        body.append(f'<section class="part" id="{path.stem}">')
        body.append(render_blocks(text))
        body.append("</section>")

    total = sum(record["check_count"] for record in records)
    passed = sum(record["passed_count"] for record in records)
    body.append('<section class="part" id="checks"><h2>Check tables of all parts</h2>')
    body.append(
        f"<p>{total} comparisons run below <code>code/</code>, and {passed} of them pass. "
        "Each comparison puts a value that one method computes against a value that a different "
        "method computes.</p>"
    )
    for record in records:
        name = PART_NAMES.get(record["part"], record["part"])
        body.append(
            f"<h3>{name}</h3><p>{record['check_count']} comparisons, {record['passed_count']} pass. "
            f"The script is <code>code/{record['part']}_verify.py</code>.</p>"
        )
        body.append(table_html(record))
    body.append("</section>")

    body.append('<section class="part" id="answer"><h2>Answer</h2>')
    body.append('<div class="answer">')
    body.append(
        "<p>The limits of the solid are $-1 \\le x \\le 1$, $x^{2} \\le y \\le 1$, and "
        "$0 \\le z \\le 1 - y$, with the density $\\rho = \\sqrt{x^{2} + y^{2}}$.</p>"
    )
    body.append(
        "<p>(a) The mass is $m = " + display["p3_mass"] + "$."
        "</p>"
    )
    body.append(
        "<p>(b) The center of mass is $(\\bar{x}, \\bar{y}, \\bar{z}) = ("
        + display["p4_xbar"]
        + ", "
        + display["p4_ybar"]
        + ", "
        + display["p4_zbar"]
        + ")$.</p>"
    )
    body.append(
        "<p>(c) The moment of inertia about the $z$ axis is $I_{z} = " + display["p5_inertia"] + "$.</p>"
    )
    body.append("</div></section>")

    head = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Exercise 47, Section 15.7: a verified tutorial</title>\n"
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
    )
    tail = (
        "<script>\ndocument.addEventListener(\"DOMContentLoaded\", function () {\n"
        "  renderMathInElement(document.body, {delimiters: [{left: \"$$\", right: \"$$\", display: true},"
        " {left: \"$\", right: \"$\", display: false}], throwOnError: false});\n"
        "});\n</script>\n</body>\n</html>\n"
    )
    return head + "\n".join(body) + "\n" + tail


def check_page(page: str) -> None:
    """Assert the invariants of the composed page.

    Args:
        page: HTML text of the page.
    """
    leftover = PLACEHOLDER.findall(page)
    if leftover:
        raise AssertionError(f"value placeholders left in the page: {leftover[:3]}")
    control = [character for character in page if ord(character) < 32 and character not in "\n\t"]
    if control:
        raise AssertionError(f"the page holds {len(control)} control characters")
    odd_lines = [line for line in page.split("\n") if line.count("$") % 2 == 1]
    if odd_lines:
        raise AssertionError(f"{len(odd_lines)} lines hold an odd count of dollar signs: {odd_lines[:2]}")
    codes = re.findall(r"<code>(.*?)</code>", page)
    if any(not item.strip() for item in codes):
        raise AssertionError("the page holds an empty code element")
    for item in codes:
        candidate = (WORKSPACE / item.strip()).resolve()
        if not candidate.exists():
            raise AssertionError(f"code element holds a path that does not exist: {item}")
    items = re.findall(r"<li>(.*?)</li>", page)
    for item in items:
        if not item.strip().endswith("."):
            raise AssertionError(f"list item does not end with a full stop: {item[:60]}")
    for paragraph in re.findall(r"<p>(.*?)</p>", page):
        text = re.sub(r"<[^>]+>", "", paragraph).strip()
        if text and text[0].islower():
            raise AssertionError(f"a paragraph starts with a lower case letter: {text[:60]}")
    for cell in re.findall(r"<td>(.*?)</td>", page):
        stripped = re.sub(r"\$[^$]*\$", "", re.sub(r"<[^>]+>", "", cell))
        if "\\" in stripped or "<" in stripped:
            raise AssertionError(f"a table cell holds raw LaTeX outside a math span: {cell[:60]}")
    print(f"page checks pass: {len(codes)} code elements, {len(items)} list items, {len(page)} characters")


def main() -> None:
    """Compose the page, assert its invariants, and write both product files."""
    display, records = load_display()
    page = assemble(display, records)
    check_page(page)
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    TUTORIAL_PATH.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {REPORT_PATH}")
    print(f"wrote {TUTORIAL_PATH}")


if __name__ == "__main__":
    main()
