"""Compose the tutorial page from the statement, the step files, and the figures.

The script reads ``problem/problem.md`` and ``steps/part<K>_step<J>.md``, converts the
small Markdown subset that the step files use, embeds each figure as a Base64 data
uniform resource identifier, and writes ``report.html`` and ``tutorial.html``.

Run with ``code/.venv/Scripts/python.exe code/compose_report.py``.
"""

from __future__ import annotations

import base64
import html
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
STEPS_DIRECTORY = WORKSPACE / "steps"
PROBLEM_FILE = WORKSPACE / "problem" / "problem.md"
FIGURE_DIRECTORY = WORKSPACE / "code" / "figures"
REPORT_FILE = WORKSPACE / "report.html"
TUTORIAL_FILE = WORKSPACE / "tutorial.html"

CONTROL_CHARACTERS = [chr(code) for code in range(0, 32) if chr(code) not in "\n"]
INLINE_CODE_PATTERN = re.compile(r"`([^`]*)`")
BOLD_PATTERN = re.compile(r"\*\*([^*]+)\*\*")
FIGURE_PATTERN = re.compile(r"^!\[(?P<caption>[^\]]*)\]\((?P<path>[^)]+)\)$")
TABLE_LINE_PATTERN = re.compile(r"^\|.*\|$")


def escape_outside_math(text: str) -> str:
    """Escape the markup characters of a text and keep every math span unchanged.

    Args:
        text: Text that holds no displayed math.

    Returns:
        The escaped text.
    """
    parts = text.split("$")
    escaped: list[str] = []
    for index, part in enumerate(parts):
        escaped.append(part if index % 2 == 1 else html.escape(part, quote=False))
    return "$".join(escaped)


def apply_inline(text: str) -> str:
    """Convert inline code and bold runs of one text.

    Args:
        text: Escaped text.

    Returns:
        The text with inline elements.
    """
    with_code = INLINE_CODE_PATTERN.sub(lambda match: f"<code>{match.group(1)}</code>", text)
    if with_code.count("<code>") != with_code.count("</code>"):
        raise AssertionError("an inline code element is not closed")
    return BOLD_PATTERN.sub(lambda match: f"<strong>{match.group(1)}</strong>", with_code)


def join_continuation_lines(lines: list[str]) -> list[str]:
    """Join each indented continuation line to the line above it.

    Args:
        lines: Raw lines of one step file.

    Returns:
        The lines with no continuation line left.
    """
    joined: list[str] = []
    for line in lines:
        if line.startswith("  ") and joined and joined[-1].strip():
            joined[-1] = joined[-1].rstrip() + " " + line.strip()
        else:
            joined.append(line)
    return joined


def render_table(lines: list[str], start: int) -> tuple[str, int]:
    """Render one Markdown table.

    Args:
        lines: Lines of the block.
        start: Index of the first row of the table.

    Returns:
        The table markup and the index of the first line after the table.
    """
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and TABLE_LINE_PATTERN.match(lines[index].strip()):
        cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        if not all(set(cell) <= set("-: ") for cell in cells):
            rows.append(cells)
        index += 1
    head, body = rows[0], rows[1:]
    pieces = ["<table>", "<thead><tr>"]
    pieces.extend(f"<th>{apply_inline(escape_outside_math(cell))}</th>" for cell in head)
    pieces.append("</tr></thead><tbody>")
    for row in body:
        pieces.append("<tr>")
        pieces.extend(f"<td>{apply_inline(escape_outside_math(cell))}</td>" for cell in row)
        pieces.append("</tr>")
    pieces.append("</tbody></table>")
    return "".join(pieces), index


def figure_markup(caption: str, relative_path: str) -> str:
    """Build one figure with an embedded image.

    Args:
        caption: Caption of the figure.
        relative_path: Path of the image, relative to the code directory.

    Returns:
        The figure markup.
    """
    target = FIGURE_DIRECTORY / Path(relative_path).name
    if not target.is_file():
        raise AssertionError(f"the figure file {target} is absent")
    payload = base64.b64encode(target.read_bytes()).decode("ascii")
    safe_caption = apply_inline(escape_outside_math(caption))
    return (
        '<figure class="plate">'
        f'<img alt="{html.escape(caption, quote=True)}" src="data:image/png;base64,{payload}">'
        f"<figcaption>{safe_caption}</figcaption>"
        "</figure>"
    )


def render_step(text: str) -> str:
    """Render one step file.

    Args:
        text: Content of the step file.

    Returns:
        The markup of the step.
    """
    lines = join_continuation_lines(text.splitlines())
    blocks: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("## "):
            blocks.append(f"<h2>{apply_inline(escape_outside_math(stripped[3:]))}</h2>")
            index += 1
            continue
        figure_match = FIGURE_PATTERN.match(stripped)
        if figure_match:
            blocks.append(figure_markup(figure_match.group("caption"), figure_match.group("path")))
            index += 1
            continue
        if TABLE_LINE_PATTERN.match(stripped):
            markup, index = render_table(lines, index)
            blocks.append(markup)
            continue
        if stripped.startswith("$$"):
            collected = [stripped]
            index += 1
            while len(collected[-1]) < 4 or not collected[-1].endswith("$$"):
                collected.append(lines[index].strip())
                index += 1
            display = " ".join(collected)
            blocks.append(f'<div class="display">{display}</div>')
            continue
        if stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(lines[index].strip()[2:])
                index += 1
            joined = "".join(
                f"<li>{apply_inline(escape_outside_math(item))}</li>" for item in items
            )
            blocks.append(f"<ul>{joined}</ul>")
            continue
        paragraph: list[str] = []
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate or candidate.startswith("## ") or candidate.startswith("$$"):
                break
            if FIGURE_PATTERN.match(candidate) or TABLE_LINE_PATTERN.match(candidate):
                break
            if candidate.startswith("- ") and paragraph:
                break
            paragraph.append(candidate)
            index += 1
        blocks.append(f"<p>{apply_inline(escape_outside_math(' '.join(paragraph)))}</p>")
    return "\n".join(blocks)


def read_statement() -> str:
    """Return the statement of the problem as markup.

    Returns:
        The markup of the statement block.
    """
    lines = PROBLEM_FILE.read_text(encoding="utf-8").splitlines()
    start = next(index for index, line in enumerate(lines) if line.strip() == "## Statement")
    quoted: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith(">"):
            quoted.append(line.lstrip("> ").strip())
        elif quoted and not line.strip():
            continue
        elif quoted:
            break
    text = " ".join(item for item in quoted if item)
    return f'<blockquote class="statement">{apply_inline(escape_outside_math(text))}</blockquote>'


def collect_steps() -> list[tuple[int, int, Path]]:
    """Return the step files in the order of the tutorial.

    Returns:
        The list of the part number, the step number, and the path of each step file.
    """
    pattern = re.compile(r"part(?P<part>\d+)_step(?P<step>\d+)\.md$")
    collected: list[tuple[int, int, Path]] = []
    for path in sorted(STEPS_DIRECTORY.glob("part*_step*.md")):
        match = pattern.search(path.name)
        if match:
            collected.append((int(match.group("part")), int(match.group("step")), path))
    collected.sort()
    return collected


def build_page() -> str:
    """Build the whole page.

    Returns:
        The markup of the page.
    """
    steps = collect_steps()
    if not steps:
        raise AssertionError("no step file is present")
    sections: list[str] = []
    contents: list[str] = []
    current_part: int | None = None
    for part, step, path in steps:
        text = path.read_text(encoding="utf-8")
        title_match = re.search(r"^## (.+)$", text, flags=re.MULTILINE)
        title = title_match.group(1) if title_match else f"Step {part}.{step}"
        anchor = f"step-{part}-{step}"
        if part != current_part:
            sections.append(f'<section class="part" id="part-{part}"><h1>Part {part}</h1>')
            contents.append(f'<p class="part"><a href="#part-{part}">Part {part}</a></p>')
            current_part = part
        contents.append(f'<p class="step"><a href="#{anchor}">{title}</a></p>')
        sections.append(f'<article class="step" id="{anchor}">{render_step(text)}</article>')
    sections.append("</section>")
    contents_markup = '<nav class="contents">' + "".join(contents) + "</nav>"
    answers_markup = "\n".join(
        [
            "<h2>Answers</h2>",
            "<p>Part (a): the volume is $V = \\dfrac{2}{3}\\pi a^{3} - \\dfrac{8}{9}a^{3}"
            " = \\dfrac{a^{3}\\left(6\\pi - 8\\right)}{9}$.</p>",
            "<p>Part (b): Figure 3 draws the sphere and the cylinder on one screen, with the curve"
            " where the two surfaces meet.</p>",
        ]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Problem 17: the volume that a cylinder cuts out of a sphere</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
:root {{ --ink: #23303a; --muted: #5b6a76; --rule: #d5dde3; --plate: #f6f8fa; }}
html {{ background: #ffffff; }}
body {{ margin: 0 auto; max-width: 54rem; padding: 2.4rem 1.6rem 4rem;
  font-family: Cambria, "Cambria Math", Georgia, serif; color: var(--ink);
  font-size: 1.02rem; line-height: 1.62; }}
h1 {{ font-size: 1.45rem; margin: 2.6rem 0 0.8rem; letter-spacing: 0.01em; }}
h2 {{ font-size: 1.12rem; margin: 1.9rem 0 0.5rem; }}
p {{ margin: 0.55rem 0; }}
strong {{ font-weight: 700; }}
code {{ font-family: "Cascadia Mono", Consolas, monospace; font-size: 0.88em;
  background: var(--plate); border: 1px solid var(--rule); border-radius: 3px;
  padding: 0.05em 0.32em; }}
.display {{ margin: 0.9rem 0; text-align: center; overflow-x: auto; }}
blockquote.statement {{ margin: 1rem 0 1.6rem; padding: 0.9rem 1.2rem;
  background: var(--plate); border-left: 3px solid #8fb3c9; }}
figure.plate {{ margin: 1.4rem 0; padding: 0.6rem; background: var(--plate);
  border: 1px solid var(--rule); border-radius: 4px; }}
figure.plate img {{ display: block; width: 100%; height: auto; }}
figcaption {{ margin-top: 0.5rem; color: var(--muted); font-size: 0.92rem; text-align: center; }}
.contents {{ font-size: 0.95rem; border-left: 1px solid var(--rule); padding-left: 0.9rem; }}
.contents p {{ margin: 0.18rem 0; }}
.contents p.step {{ padding-left: 1.1rem; }}
a {{ color: #1d5c80; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.katex {{ font-family: "XITS Math", "STIX Two Math", "Cambria Math", serif; }}
.lead {{ color: var(--muted); }}
</style>
</head>
<body>
<h1>Problem 17: the volume that a cylinder cuts out of a sphere</h1>
<p class="lead">Stewart Calculus, section 15.8, exercise 26. The answer stays symbolic in the radius
$a$, because the statement gives no numeric value for it.</p>
<h2>Statement</h2>
{read_statement()}
<h2>Plan of the tutorial</h2>
<p>The tutorial has six parts and thirteen steps. Part 1 reads the two surfaces. Part 2 writes the
solid as limits in cylindrical coordinates. Parts 3 and 4 carry out the three integrations. Part 5
checks the volume by three methods that do not use the closed form. Part 6 draws the two surfaces for
part (b) of the statement.</p>
{contents_markup}
{''.join(sections)}
{answers_markup}
<script>
document.addEventListener("DOMContentLoaded", function () {{
  renderMathInElement(document.body, {{
    delimiters: [
      {{ left: "$$", right: "$$", display: true }},
      {{ left: "$", right: "$", display: false }}
    ],
    throwOnError: false
  }});
}});
</script>
</body>
</html>
"""


def strip_math(text: str) -> str:
    """Remove each displayed math block and each inline math span of a markup text.

    Args:
        text: Markup text.

    Returns:
        The text with no math span left.
    """
    without_display = re.sub(r"\$\$.+?\$\$", "", text, flags=re.DOTALL)
    return re.sub(r"\$[^$]+?\$", "", without_display)


def assert_page(page: str) -> None:
    """Assert the properties that the composed page must have.

    Args:
        page: The composed page.

    Raises:
        AssertionError: The page breaks one of the rules.
    """
    for character in CONTROL_CHARACTERS:
        assert character not in page, f"the page holds the control character {ord(character)}"
    outside_math = strip_math(page)
    assert "\\" not in outside_math, "a backslash sits outside a math span"

    for paragraph in re.findall(r"<p>(.*?)</p>", page, flags=re.DOTALL):
        plain = re.sub(r"<[^>]+>", "", paragraph).strip()
        if plain:
            assert plain[0].isupper(), f"a paragraph begins with a lower-case letter: {plain[:40]}"
    for item in re.findall(r"<li>(.*?)</li>", page, flags=re.DOTALL):
        plain = re.sub(r"<[^>]+>", "", item).strip()
        assert plain.endswith("."), f"a list item does not end with a full stop: {plain[:40]}"
    for content in INLINE_CODE_PATTERN.findall(page):
        assert content.strip(), "an inline code element is empty"
    for cell in re.findall(r"<t[dh]>(.*?)</t[dh]>", page, flags=re.DOTALL):
        plain = strip_math(cell)
        assert "\\" not in plain, f"a table cell holds a math token outside a math span: {plain[:40]}"
        assert "<" not in re.sub(r"<[^>]+>", "", plain), "a table cell holds an unescaped bracket"
    for caption in re.findall(r"<figcaption>(.*?)</figcaption>", page, flags=re.DOTALL):
        plain = strip_math(caption)
        assert "\\" not in plain, "a caption holds a math token outside a math span"
        assert " = " not in plain, f"a caption holds a relation outside a math span: {plain[:40]}"
    assert page.count("<figure") == 3, f"the page holds {page.count('<figure')} figures"
    assert page.count("data:image/png;base64,") == 3, "a figure is not embedded"
    assert page.count("<article") == 13, f"the page holds {page.count('<article')} steps"
    print(
        f"CHECK page_properties PASS figures={page.count('<figure')} "
        f"steps={page.count('<article')} tables={page.count('<table>')} "
        f"code_spans={page.count('<code>')}"
    )


def main() -> None:
    """Compose the two pages and report their size."""
    page = build_page()
    assert_page(page)
    REPORT_FILE.write_text(page, encoding="utf-8")
    TUTORIAL_FILE.write_text(page, encoding="utf-8")
    print(f"WROTE {REPORT_FILE} bytes={REPORT_FILE.stat().st_size}")
    print(f"WROTE {TUTORIAL_FILE} bytes={TUTORIAL_FILE.stat().st_size}")


if __name__ == "__main__":
    main()
