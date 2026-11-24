"""Compose the tutorial page of the session from the step files and the figures.

The script reads the step files of the workspace, resolves every check
placeholder to the line range of the check in its verification script, embeds
every figure as a Base64 data uniform resource identifier, and writes
``report.html``. It then asserts the properties of the composed page that the
session rules require, and it fails when one of them does not hold.
"""

from __future__ import annotations

import base64
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEPS_DIRECTORY = os.path.join(PROJECT_ROOT, "steps")
CODE_DIRECTORY = os.path.join(PROJECT_ROOT, "code")
FIGURE_DIRECTORY = os.path.join(CODE_DIRECTORY, "figures")
PROBLEM_PATH = os.path.join(PROJECT_ROOT, "problem", "problem.md")
REPORT_PATH = os.path.join(PROJECT_ROOT, "report.html")
TUTORIAL_PATH = os.path.join(PROJECT_ROOT, "tutorial.html")

STEP_FILE_PATTERN = re.compile(r"^part(\d+)_step(\d+)\.md$")
CHECK_BEGIN_PATTERN = re.compile(r"^\s*# BEGIN CHECK ([A-Za-z0-9_]+)$")
CHECK_END_PATTERN = re.compile(r"^\s*# END CHECK ([A-Za-z0-9_]+)$")
CHECK_REFERENCE_PATTERN = re.compile(r"\[\[check:part(\d+):([A-Za-z0-9_]+)\]\]")
FIGURE_PATTERN = re.compile(r"^FIGURE: ([A-Za-z0-9_]+\.png) \| (.+)$")
MATH_SPAN_PATTERN = re.compile(r"\$\$.+?\$\$|\$[^$]+\$", re.DOTALL)
CONTROL_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def escape_html(text_value: str) -> str:
    """Escape the two characters that break an HTML text node."""
    return text_value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def locate_checks() -> dict[tuple[int, str], tuple[int, int]]:
    """Return the first and last line of each named check in each part script."""
    locations: dict[tuple[int, str], tuple[int, int]] = {}
    for file_name in sorted(os.listdir(CODE_DIRECTORY)):
        match = re.match(r"^part(\d+)_verify\.py$", file_name)
        if not match:
            continue
        part_number = int(match.group(1))
        with open(os.path.join(CODE_DIRECTORY, file_name), encoding="utf-8") as source_file:
            source_lines = source_file.read().splitlines()
        for line_number, line in enumerate(source_lines, start=1):
            begin_match = CHECK_BEGIN_PATTERN.match(line)
            if not begin_match:
                continue
            check_name = begin_match.group(1)
            end_line = 0
            for later_number in range(line_number, len(source_lines) + 1):
                end_match = CHECK_END_PATTERN.match(source_lines[later_number - 1])
                if end_match and end_match.group(1) == check_name:
                    end_line = later_number
                    break
            if end_line == 0:
                raise ValueError(f"the check {check_name} of part {part_number} has no end marker")
            locations[(part_number, check_name)] = (line_number, end_line)
    return locations


def resolve_check_references(text_value: str, locations: dict[tuple[int, str], tuple[int, int]]) -> tuple[str, int]:
    """Replace each check placeholder with the file path and line range of the check."""
    resolved_count = 0

    def replace_reference(reference: re.Match[str]) -> str:
        nonlocal resolved_count
        part_number = int(reference.group(1))
        check_name = reference.group(2)
        key = (part_number, check_name)
        if key not in locations:
            raise ValueError(f"the check reference {check_name} of part {part_number} has no script")
        first_line, last_line = locations[key]
        resolved_count += 1
        return f"`{check_name}` in `code/part{part_number}_verify.py:{first_line}-{last_line}`"

    resolved_text = CHECK_REFERENCE_PATTERN.sub(replace_reference, text_value)
    return resolved_text, resolved_count


def render_inline(text_value: str) -> str:
    """Convert the inline markup of one line to HTML, keeping math spans intact."""
    parts = re.split(r"(\$\$.+?\$\$|\$[^$]+\$)", text_value)
    rendered_parts: list[str] = []
    for part in parts:
        if part.startswith("$"):
            rendered_parts.append(part.replace("<", "&lt;"))
            continue
        escaped = escape_html(part)
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
        rendered_parts.append(escaped)
    return "".join(rendered_parts)


def split_table_row(line: str) -> list[str]:
    """Split one pipe table row into its cells."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_separator_row(cells: list[str]) -> bool:
    """Return True when every cell of the row is a dash rule."""
    return all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def render_table(table_lines: list[str]) -> str:
    """Render a pipe table with a header row and an optional separator row."""
    rows = [split_table_row(line) for line in table_lines]
    if len(rows) >= 2 and is_separator_row(rows[1]):
        header_cells = rows[0]
        body_rows = rows[2:]
    else:
        header_cells = rows[0]
        body_rows = rows[1:]
    html_parts = ['<table>', "<thead><tr>"]
    for cell in header_cells:
        html_parts.append(f"<th>{render_inline(cell)}</th>")
    html_parts.append("</tr></thead><tbody>")
    for row_cells in body_rows:
        html_parts.append("<tr>")
        for cell in row_cells:
            html_parts.append(f"<td>{render_inline(cell)}</td>")
        html_parts.append("</tr>")
    html_parts.append("</tbody></table>")
    return "".join(html_parts)


def embed_figure(file_name: str, caption: str, figure_number: int) -> str:
    """Return one figure element whose image is a Base64 data identifier."""
    figure_path = os.path.join(FIGURE_DIRECTORY, file_name)
    if not os.path.exists(figure_path):
        raise FileNotFoundError(f"the figure {file_name} is absent")
    with open(figure_path, "rb") as figure_file:
        encoded = base64.b64encode(figure_file.read()).decode("ascii")
    caption_html = render_inline(caption)
    return (
        f'<figure class="numbered-figure" id="figure-{figure_number}">'
        f'<img alt="Figure {figure_number}" src="data:image/png;base64,{encoded}">'
        f"<figcaption>Figure {figure_number}. {caption_html}</figcaption>"
        "</figure>"
    )


def render_step_block(block_lines: list[str]) -> str:
    """Render one step block, which is a heading plus text, lists, tables, and figures."""
    html_parts: list[str] = []
    paragraph_lines: list[str] = []
    table_lines: list[str] = []
    list_items: list[str] = []
    display_math: list[str] = []
    in_display_math = False

    def flush_paragraph() -> None:
        if paragraph_lines:
            html_parts.append(f"<p>{render_inline(' '.join(paragraph_lines))}</p>")
            paragraph_lines.clear()

    def flush_table() -> None:
        if table_lines:
            html_parts.append(render_table(table_lines))
            table_lines.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            html_parts.append(f"<ul>{items}</ul>")
            list_items.clear()

    for line in block_lines:
        stripped = line.strip()
        if in_display_math:
            if stripped.endswith("$$") and len(stripped) > 2:
                display_math.append(stripped[:-2])
                joined_math = " ".join(display_math).replace("<", "&lt;")
                html_parts.append('<div class="display-math">$$' + joined_math + "$$</div>")
                display_math.clear()
                in_display_math = False
            else:
                display_math.append(stripped)
            continue
        if stripped.startswith("$$") and not (stripped.endswith("$$") and len(stripped) > 2):
            flush_paragraph()
            flush_table()
            flush_list()
            in_display_math = True
            display_math.append(stripped[2:])
            continue
        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            flush_paragraph()
            flush_table()
            flush_list()
            html_parts.append(f"<div class=\"display-math\">{stripped}</div>")
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            flush_table()
            flush_list()
            html_parts.append(f"<h2>{render_inline(stripped[3:])}</h2>")
            continue
        if stripped.startswith("| "):
            flush_paragraph()
            flush_list()
            table_lines.append(line)
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            flush_table()
            list_items.append(stripped[2:])
            continue
        if not stripped:
            flush_paragraph()
            flush_table()
            flush_list()
            continue
        if list_items and not stripped.startswith("## "):
            list_items[-1] = list_items[-1] + " " + stripped
            continue
        flush_table()
        paragraph_lines.append(stripped)

    flush_paragraph()
    flush_table()
    flush_list()
    if in_display_math:
        raise ValueError("a display math block is not closed")
    return "\n".join(html_parts)


def collect_step_files() -> list[tuple[int, int, str]]:
    """Return the step files in part order and then in step order."""
    entries: list[tuple[int, int, str]] = []
    for file_name in os.listdir(STEPS_DIRECTORY):
        match = STEP_FILE_PATTERN.match(file_name)
        if match:
            entries.append((int(match.group(1)), int(match.group(2)), file_name))
    entries.sort()
    return entries


def read_statement() -> str:
    """Return the quoted statement of the problem as one block quote.

    A display formula inside the quotation becomes an inline formula in display
    style, because a quotation keeps the flow of the sentence that holds it.
    """
    with open(PROBLEM_PATH, encoding="utf-8") as problem_file:
        problem_lines = problem_file.read().splitlines()
    start_index = problem_lines.index("## Problem statement")
    quoted_lines: list[str] = []
    for line in problem_lines[start_index + 1 :]:
        if line.startswith("## "):
            break
        if line.startswith(">"):
            quoted_lines.append(line.lstrip(">").strip())

    paragraphs: list[str] = []
    current: list[str] = []
    pending_break = False
    for line in quoted_lines:
        if not line:
            pending_break = True
            continue
        if pending_break and current and line[:1].isupper():
            paragraphs.append(" ".join(current))
            current = []
        current.append(line)
        pending_break = False
    if current:
        paragraphs.append(" ".join(current))

    rendered_parts: list[str] = []
    for paragraph in paragraphs:
        inline_display = re.sub(
            "[$][$](.+?)[$][$]",
            lambda match: "$" + chr(92) + "displaystyle " + match.group(1) + "$",
            paragraph,
        )
        rendered_parts.append(f"<p>{render_inline(inline_display)}</p>")
    return "<blockquote>" + "".join(rendered_parts) + "</blockquote>"


def build_page() -> tuple[str, list[tuple[int, str, int, int]]]:
    """Build the full page text and return it with the list of resolved checks."""
    locations = locate_checks()
    resolved_checks: list[tuple[int, str, int, int]] = []
    figure_count = 0
    body_parts: list[str] = []

    for part_number, step_number, file_name in collect_step_files():
        with open(os.path.join(STEPS_DIRECTORY, file_name), encoding="utf-8") as step_file:
            step_lines = step_file.read().splitlines()
        block_lines: list[str] = []
        for line in step_lines:
            figure_match = FIGURE_PATTERN.match(line.strip())
            if figure_match:
                block_lines.append("@@FIGURE@@ " + figure_match.group(1) + " || " + figure_match.group(2))
            else:
                block_lines.append(line)
        resolved_block: list[str] = []
        for line in block_lines:
            resolved_line, line_check_count = resolve_check_references(line, locations)
            for reference in CHECK_REFERENCE_PATTERN.finditer(line):
                if line_check_count:
                    key = (int(reference.group(1)), reference.group(2))
                    first_line, last_line = locations[key]
                    resolved_checks.append((key[0], key[1], first_line, last_line))
            resolved_block.append(resolved_line)
        rendered_parts: list[str] = []
        pending_text: list[str] = []
        for line in resolved_block:
            if line.startswith("@@FIGURE@@ "):
                payload = line[len("@@FIGURE@@ ") :]
                figure_file_name, caption = payload.split(" || ", 1)
                if pending_text:
                    rendered_parts.append(render_step_block(pending_text))
                    pending_text = []
                figure_count += 1
                rendered_parts.append(embed_figure(figure_file_name, caption, figure_count))
            else:
                pending_text.append(line)
        if pending_text:
            rendered_parts.append(render_step_block(pending_text))
        step_identifier = f"part{part_number}-step{step_number}"
        body_parts.append(
            f'<section class="step" id="{step_identifier}">' + "\n".join(rendered_parts) + "</section>"
        )

    check_rows = []
    seen_checks: set[tuple[int, str]] = set()
    for part_number, check_name, first_line, last_line in resolved_checks:
        if (part_number, check_name) in seen_checks:
            continue
        seen_checks.add((part_number, check_name))
        check_rows.append(
            "<tr>"
            f"<td>Part {part_number}</td>"
            f"<td><code>{check_name}</code></td>"
            f"<td><code>code/part{part_number}_verify.py:{first_line}-{last_line}</code></td>"
            "</tr>"
        )
    check_table = (
        '<table class="check-table"><thead><tr><th>Part</th><th>Check</th><th>Script and lines</th>'
        "</tr></thead><tbody>" + "".join(check_rows) + "</tbody></table>"
    )

    statement_html = read_statement()
    head_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Drawing the solid enclosed by two paraboloids</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
:root {
  --ink: #16202b;
  --muted: #55636f;
  --accent: #1f5f8b;
  --warm: #a0522d;
  --rule: #d8dee5;
  --paper: #fbfcfd;
}
html { font-size: 17px; }
body {
  margin: 0 auto; max-width: 52rem; padding: 2.4rem 1.6rem 4rem;
  background: var(--paper); color: var(--ink);
  font-family: Cambria, "Cambria Math", Georgia, serif; line-height: 1.62;
}
h1 { font-size: 1.85rem; line-height: 1.25; margin: 0 0 0.4rem; letter-spacing: 0.01em; }
h2 { font-size: 1.24rem; margin: 2.1rem 0 0.7rem; color: var(--accent); border-bottom: 1px solid var(--rule); padding-bottom: 0.3rem; }
p { margin: 0.7rem 0; }
.lede { color: var(--muted); font-size: 1.02rem; margin-bottom: 1.4rem; }
.answer-box { border-left: 4px solid var(--accent); background: #eef4f9; padding: 0.85rem 1.1rem; margin: 1.4rem 0 1.8rem; }
.answer-box p { margin: 0.25rem 0; }
blockquote { margin: 1.1rem 0; padding: 0.7rem 1.1rem; border-left: 3px solid var(--rule); background: #f4f6f8; color: #24313d; }
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }
section.step { margin-bottom: 0.6rem; }
.display-math { margin: 1rem 0; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; margin: 1.1rem 0; font-size: 0.95rem; }
th, td { border: 1px solid var(--rule); padding: 0.42rem 0.6rem; text-align: left; vertical-align: top; }
th { background: #eef2f6; font-weight: 600; }
code { font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 0.86em; background: #eef1f4; padding: 0.08em 0.3em; border-radius: 3px; color: #14324a; }
figure.numbered-figure { margin: 1.6rem 0; text-align: center; }
figure.numbered-figure img { max-width: 100%; height: auto; border: 1px solid var(--rule); border-radius: 4px; background: #fff; }
figcaption { margin-top: 0.55rem; color: var(--muted); font-size: 0.9rem; text-align: left; }
strong { font-weight: 600; }
.katex { font-family: "XITS Math", "Cambria Math", Cambria, serif; font-size: 1.02em; }
ul { margin: 0.6rem 0 0.6rem 1.2rem; }
li { margin: 0.25rem 0; }
.check-table { font-size: 0.88rem; }
footer { margin-top: 3rem; border-top: 1px solid var(--rule); padding-top: 0.9rem; color: var(--muted); font-size: 0.88rem; }
</style>
</head>
<body>
"""

    answer_html = r"""
<header>
<h1>The solid enclosed by the paraboloids $z = x^{2} + y^{2}$ and $z = 5 - x^{2} - y^{2}$</h1>
<p class="lede">A verified tutorial for exercise 14 of section 15.8. The answer is a drawing, so the page carries the inequality description, the drawn closed body with the meeting circle, and one scale on each axis. Every numerical claim cites the file and the line range of its check.</p>
<div class="answer-box">
<p><strong>Answer.</strong> $\displaystyle E = \left\{(x, y, z) : x^{2} + y^{2} \le z \le 5 - x^{2} - y^{2}\right\}$</p>
<p>The body is closed. Its footprint is the disk $x^{2} + y^{2} \le \dfrac{5}{2}$, its rim is the circle $x^{2} + y^{2} = \dfrac{5}{2}$ at $z = \dfrac{5}{2}$, and its heights run from $0$ to $5$.</p>
<p>Figure 3 draws that body with the horizontal marks $1$ and $2$ and the vertical marks $1$, $3$ and $5$.</p>
</div>
</header>

<section id="statement">
<h2>The statement</h2>
"""
    closing_html = (
        "\n</section>\n"
        '<section id="checks">\n<h2>Every check of the tutorial</h2>\n'
        "<p>Each row names the check of one step and the line range of the check in its script. "
        "The script prints the computed value and the expected value, and it stops with an error when "
        "the two values disagree beyond the tolerance of the problem.</p>\n"
        + check_table
        + "\n</section>\n"
        "<footer>Product of the MCMA tutoring stage for session "
        "20261123_040701_tutoring_problem_16. The three figure scripts write the three figures of the page; "
        "the verification scripts write the printed checks.</footer>\n"
        "<script>\n"
        "document.addEventListener('DOMContentLoaded', function () {\n"
        "  if (typeof renderMathInElement === 'function') {\n"
        "    renderMathInElement(document.body, {\n"
        "      delimiters: [\n"
        "        {left: '$$', right: '$$', display: true},\n"
        "        {left: '$', right: '$', display: false}\n"
        "      ],\n"
        "      throwOnError: false\n"
        "    });\n"
        "  }\n"
        "});\n"
        "</script>\n"
        "</body>\n</html>\n"
    )

    page_text = (
        head_html
        + answer_html
        + statement_html
        + "\n</section>\n"
        + "\n".join(body_parts)
        + closing_html
    )
    return page_text, resolved_checks


def assert_page_properties(page_text: str, figure_count: int, check_count: int) -> None:
    """Assert the composed page properties that the session rules require."""
    control_characters = CONTROL_PATTERN.findall(page_text)
    if control_characters:
        raise AssertionError(f"the page holds {len(control_characters)} control characters")
    if "[[" in page_text or "]]" in page_text:
        raise AssertionError("the page holds an unresolved placeholder")
    data_identifier_count = page_text.count("data:image/png;base64,")
    if data_identifier_count != figure_count:
        raise AssertionError(
            f"the page holds {data_identifier_count} embedded figures but {figure_count} figures were written"
        )
    if page_text.count("$$") % 2 != 0:
        raise AssertionError("the page holds an unpaired display math delimiter")
    mentioned_figures = {int(number) for number in re.findall(r"Figure (\d+)", page_text)}
    if mentioned_figures - set(range(1, figure_count + 1)):
        raise AssertionError("the page cites a figure number that no figure carries")
    for list_item in re.findall(r"<li>(.*?)</li>", page_text, flags=re.DOTALL):
        plain_text = re.sub(r"<[^>]+>", "", list_item).strip()
        if plain_text and not plain_text.endswith("."):
            raise AssertionError(f"the list item {plain_text[:40]!r} does not end with a full stop")
    for paragraph in re.findall(r"<p>(.*?)</p>", page_text, flags=re.DOTALL):
        plain_text = re.sub(r"<[^>]+>", "", paragraph).strip()
        if plain_text and plain_text[0].islower():
            raise AssertionError(f"the paragraph {plain_text[:40]!r} begins with a lower-case word")
    cell_pattern = re.compile(r"<t[dh]>(.*?)</t[dh]>", re.DOTALL)
    for cell in cell_pattern.findall(page_text):
        outside_math = MATH_SPAN_PATTERN.sub("", cell)
        if "\\" in outside_math:
            raise AssertionError(f"the cell {outside_math[:40]!r} holds a backslash outside math")
        if "&lt;" in outside_math:
            raise AssertionError(f"the cell {outside_math[:40]!r} holds a literal less-than sign")
    for caption in re.findall(r"<figcaption>(.*?)</figcaption>", page_text, flags=re.DOTALL):
        outside_math = MATH_SPAN_PATTERN.sub("", caption)
        if "\\" in outside_math:
            raise AssertionError("a caption holds a backslash outside math")
        if "&lt;" in outside_math:
            raise AssertionError("a caption holds a literal less-than sign")
    if check_count == 0:
        raise AssertionError("the page cites no check")
    empty_code_count = page_text.count("<code></code>")
    if empty_code_count:
        raise AssertionError(f"the page holds {empty_code_count} empty inline code elements")
    code_contents = re.findall(r"<code>(.*?)</code>", page_text, flags=re.DOTALL)
    if any(not content.strip() for content in code_contents):
        raise AssertionError("an inline code element holds no name")
    print(f"page assertions passed: {figure_count} figures, {check_count} check citations")


def main() -> None:
    """Compose the page, write it, and assert its properties."""
    page_text, resolved_checks = build_page()
    for page_path in (REPORT_PATH, TUTORIAL_PATH):
        with open(page_path, "w", encoding="utf-8", newline="\n") as report_file:
            report_file.write(page_text)
    distinct_checks = {(part_number, check_name) for part_number, check_name, _, _ in resolved_checks}
    assert_page_properties(page_text, page_text.count("data:image/png;base64,"), len(resolved_checks))
    print(f"wrote {REPORT_PATH} and {TUTORIAL_PATH}")
    print(f"distinct checks cited: {len(distinct_checks)}")
    print(f"check citations: {len(resolved_checks)}")
    print(f"page size in bytes: {len(page_text)}")


if __name__ == "__main__":
    main()
