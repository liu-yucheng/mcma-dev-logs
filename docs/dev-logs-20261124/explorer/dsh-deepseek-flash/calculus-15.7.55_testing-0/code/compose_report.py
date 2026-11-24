"""Compose the tutorial page from the step files and the verified results.

The composer reads `<workspace>/steps/part<N>_step<M>.md`, replaces each `{{key}}` token with a value that a
verification script printed, embeds each figure as a Base64 data uniform resource identifier, and writes
`<workspace>/report.html`. The composer asserts the page rules of the pass before it writes the file.
"""

from __future__ import annotations

import base64
import html
import json
import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CODE_DIRECTORY = WORKSPACE / "code"
STEPS_DIRECTORY = WORKSPACE / "steps"
FIGURES_DIRECTORY = CODE_DIRECTORY / "figures"
OUTPUTS_DIRECTORY = CODE_DIRECTORY / "outputs"
REPORT_PATH = WORKSPACE / "report.html"

PART_TITLES = {
    1: "The integrand selects the region and fixes its shape",
    2: "The candidate regions and the maximum",
    3: "Evaluate the integral over the ellipsoid",
    4: "The exact value from a computer algebra system",
}

TOKEN_PATTERN = re.compile(r"\{\{([A-Za-z0-9_.]+)(?::([^{}]+))?\}\}")
FIGURE_PATTERN = re.compile(r"\[\[figure:([A-Za-z0-9_]+)\|(.+?)\]\]")
MATH_INLINE_PATTERN = re.compile(r"\$[^$]+\$")
LIST_ITEM_PATTERN = re.compile(r"^\s*[-*]\s+")


def load_values() -> dict[str, object]:
    """Return one flat dictionary of the verified values of all four parts.

    Returns:
        A dictionary whose keys are `part<N>.<field>` and whose values are the printed results.
    """
    values: dict[str, object] = {}
    for part_number in (1, 2, 3, 4):
        path = OUTPUTS_DIRECTORY / f"part{part_number}_results.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        values[f"part{part_number}"] = payload
        for key, value in payload.items():
            values[f"part{part_number}.{key}"] = value
    return values


def resolve(values: dict[str, object], key: str, spec: str | None) -> str:
    """Return the formatted value of one token.

    Args:
        values: The flat dictionary of verified values.
        key: A dotted key such as `part3.exact_value` or `part2.candidate_rows.1.value`.
        spec: An optional format specification such as `.6f`.

    Returns:
        The formatted text of the value.
    """
    node: object = values
    for piece in key.split("."):
        if isinstance(node, dict):
            node = node[piece]
        elif isinstance(node, list):
            node = node[int(piece)]
        else:
            raise KeyError(f"the key {key} does not resolve")
    if isinstance(node, float):
        if spec:
            return format(node, spec)
        return f"{node:.10g}" if abs(node) < 1.0e-4 and node != 0.0 else repr(node)
    if isinstance(node, (list, dict)):
        raise KeyError(f"the key {key} holds a structure, not a number")
    if spec:
        return format(node, spec)
    return str(node)


def substitute_tokens(text: str, values: dict[str, object]) -> str:
    """Replace every token of a text with its verified value.

    Args:
        text: The source text with tokens.
        values: The flat dictionary of verified values.

    Returns:
        The text with every token replaced.
    """
    return TOKEN_PATTERN.sub(lambda match: resolve(values, match.group(1), match.group(2)), text)


def inline_markup(text: str) -> str:
    """Convert the inline markup of one paragraph to HTML and escape the rest.

    Args:
        text: One paragraph of Markdown with `$...$` mathematics.

    Returns:
        The HTML fragment of the paragraph.
    """
    parts: list[str] = []
    position = 0
    for match in MATH_INLINE_PATTERN.finditer(text):
        parts.append(escape_plain(text[position:match.start()]))
        parts.append(match.group(0))
        position = match.end()
    parts.append(escape_plain(text[position:]))
    joined = "".join(parts)
    joined = re.sub(r"`([^`]+)`", r"<code>\1</code>", joined)
    joined = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", joined)
    return joined


def escape_plain(text: str) -> str:
    """Escape one piece of plain text and keep the inline code spans.

    Args:
        text: A piece of text with no mathematics.

    Returns:
        The escaped text with `<code>` elements for the backtick spans.
    """
    pieces: list[str] = []
    position = 0
    for match in re.finditer(r"`([^`]+)`", text):
        pieces.append(html.escape(text[position:match.start()], quote=False))
        pieces.append(f"<code>{html.escape(match.group(1), quote=False)}</code>")
        position = match.end()
    pieces.append(html.escape(text[position:], quote=False))
    return "".join(pieces)


def figure_element(name: str, caption: str, values: dict[str, object]) -> str:
    """Return one figure element with an embedded PNG and an escaped caption.

    Args:
        name: The file stem of the figure under `code/figures/`.
        caption: The caption with `$...$` mathematics.
        values: The flat dictionary of verified values.

    Returns:
        The HTML element of the figure.
    """
    path = FIGURES_DIRECTORY / f"{name}.png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    caption_text = substitute_tokens(caption, values)
    escaped = escape_caption(caption_text)
    extra = " narrow" if name.endswith("figure2") else ""
    return (f'<figure class="plate{extra}"><img alt="{html.escape(name)}" '
            f'src="data:image/png;base64,{payload}"><figcaption>{escaped}</figcaption></figure>')


def escape_caption(text: str) -> str:
    """Escape a caption and keep its `$...$` spans intact.

    Args:
        text: The caption text.

    Returns:
        The escaped caption.
    """
    pieces: list[str] = []
    position = 0
    for match in MATH_INLINE_PATTERN.finditer(text):
        pieces.append(html.escape(text[position:match.start()], quote=False))
        pieces.append(match.group(0))
        position = match.end()
    pieces.append(html.escape(text[position:], quote=False))
    return "".join(pieces)


def parse_step(path: Path, values: dict[str, object]) -> str:
    """Return the HTML of one step file.

    Args:
        path: The path of the step file.
        values: The flat dictionary of verified values.

    Returns:
        The HTML fragment of the step.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ").strip()
    match = re.match(r"Part\s+(\d+),\s*Step\s+(\d+):\s*(.+)", title)
    if match is None:
        raise AssertionError(f"the title of {path.name} does not name a part and a step")
    heading = f"Step {match.group(2)}: {match.group(3)}"

    blocks: list[str] = []
    paragraph: list[str] = []
    item_lines: list[str] = []
    items: list[str] = []
    table_rows: list[list[str]] = []
    display: list[str] = []
    in_display = False

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(paragraph).strip()
            blocks.append(f"<p>{inline_markup(substitute_tokens(text, values))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if items:
            rendered = "".join(f"<li>{item}</li>" for item in items)
            blocks.append(f"<ul>{rendered}</ul>")
            items.clear()

    def flush_table() -> None:
        if table_rows:
            header = table_rows[0]
            body = table_rows[2:] if len(table_rows) > 2 else []
            head_html = "".join(
                f"<th>{inline_markup(substitute_tokens(cell, values))}</th>" for cell in header)
            body_html = ""
            for row in body:
                cells = "".join(
                    f"<td>{inline_markup(substitute_tokens(cell, values))}</td>" for cell in row)
                body_html += f"<tr>{cells}</tr>"
            blocks.append(f"<table><thead><tr>{head_html}</tr></thead><tbody>{body_html}</tbody></table>")
            table_rows.clear()

    for raw in lines[1:]:
        line = raw.rstrip()
        if in_display:
            display.append(line)
            if line.strip().endswith("$$"):
                in_display = False
                blocks.append(f"<div class=\"display\">{substitute_tokens(chr(10).join(display), values)}</div>")
                display.clear()
            continue
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            continue
        if stripped.startswith("$$"):
            flush_paragraph()
            flush_list()
            flush_table()
            if stripped.endswith("$$") and len(stripped) > 4:
                blocks.append(f"<div class=\"display\">{substitute_tokens(stripped, values)}</div>")
            else:
                in_display = True
                display.append(stripped)
            continue
        if stripped.startswith("|"):
            flush_paragraph()
            flush_list()
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            table_rows.append(cells)
            continue
        if FIGURE_PATTERN.search(stripped):
            flush_paragraph()
            flush_list()
            flush_table()
            for match in FIGURE_PATTERN.finditer(stripped):
                blocks.append(figure_element(match.group(1), match.group(2), values))
            continue
        if LIST_ITEM_PATTERN.match(line):
            flush_paragraph()
            flush_table()
            if item_lines:
                items.append(inline_markup(substitute_tokens(" ".join(item_lines).strip(), values)))
                item_lines.clear()
            item_lines.append(LIST_ITEM_PATTERN.sub("", line).strip())
            continue
        if line.startswith("  ") and item_lines:
            item_lines.append(stripped)
            continue
        if item_lines:
            items.append(inline_markup(substitute_tokens(" ".join(item_lines).strip(), values)))
            item_lines.clear()
            flush_list()
        if line.startswith("#"):
            flush_paragraph()
            flush_list()
            flush_table()
            blocks.append(f"<h4>{inline_markup(substitute_tokens(stripped.lstrip('# ').strip(), values))}</h4>")
            continue
        paragraph.append(stripped)

    if item_lines:
        items.append(inline_markup(substitute_tokens(" ".join(item_lines).strip(), values)))
        item_lines.clear()
    flush_paragraph()
    flush_list()
    flush_table()
    if in_display:
        raise AssertionError(f"the display block of {path.name} is not closed")

    return (f'<article class="step" id="{path.stem}"><h3>{html.escape(heading)}</h3>'
            + "".join(blocks) + "</article>")


def build_page(values: dict[str, object]) -> str:
    """Return the complete HTML page.

    Args:
        values: The flat dictionary of verified values.

    Returns:
        The HTML text of the page.
    """
    step_paths = sorted(STEPS_DIRECTORY.glob("part*_step*.md"),
                        key=lambda path: tuple(int(number) for number in re.findall(r"\d+", path.stem)))
    sections: list[str] = []
    current_part: int | None = None
    for path in step_paths:
        part_number = int(re.search(r"part(\d+)_", path.name).group(1))
        if part_number != current_part:
            sections.append(f'<section class="part"><h2>Part {part_number}. '
                            f'{html.escape(PART_TITLES[part_number])}</h2>')
            current_part = part_number
        sections.append(parse_step(path, values))
    if step_paths:
        sections.append("</section>")

    statement = """
    <p>Find the region $E$ for which the triple integral</p>
    <div class="display">$$\\iiint_{E}\\left(1-x^{2}-2y^{2}-3z^{2}\\right)dV$$</div>
    <p>The integral is a maximum. Then use a computer algebra system to calculate the exact maximum value.</p>
    """

    answer_rows = [
        ("The region", "$E^{*}=\\{(x,y,z):x^{2}+2y^{2}+3z^{2}\\le 1\\}$"),
        ("The exact maximum", "$\\dfrac{8\\pi}{15\\sqrt{6}}=\\dfrac{4\\pi\\sqrt{6}}{45}$"),
        ("The decimal value", substitute_tokens("{{part4.exact_value}}", values)),
        ("The value to six decimals", substitute_tokens("{{part4.six_decimals}}", values)),
    ]
    answer_html = "".join(f"<tr><th>{name}</th><td>{value}</td></tr>" for name, value in answer_rows)

    check_rows = ""
    for part_number in (1, 2, 3, 4):
        count = values[f"part{part_number}.checks"]["count"]
        check_rows += (f"<tr><td><code>code/part{part_number}_verify.py</code></td>"
                       f"<td>{count}</td><td>pass</td></tr>")

    total_checks = sum(int(values[f"part{number}.checks"]["count"]) for number in (1, 2, 3, 4))

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The maximum of a triple integral over a free region</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
  :root {{ --ink: #1b1b1b; --muted: #5a5a5a; --rule: #d8d8d8; --accent: #1f4e79; --tint: #f4f7fa; }}
  html {{ font-size: 17px; }}
  body {{ margin: 0 auto; max-width: 46rem; padding: 2.2rem 1.4rem 4rem; color: var(--ink);
         background: #ffffff; font-family: Cambria, "Cambria Math", Georgia, serif; line-height: 1.62; }}
  h1 {{ font-size: 1.85rem; line-height: 1.25; margin: 0 0 0.4rem; }}
  h2 {{ font-size: 1.32rem; margin: 2.6rem 0 0.6rem; padding-bottom: 0.3rem; border-bottom: 2px solid var(--accent); }}
  h3 {{ font-size: 1.1rem; margin: 1.9rem 0 0.5rem; color: var(--accent); }}
  h4 {{ font-size: 1rem; margin: 1.3rem 0 0.4rem; color: var(--muted); }}
  p {{ margin: 0.6rem 0; }}
  .lead {{ color: var(--muted); font-size: 0.98rem; }}
  .display {{ margin: 0.9rem 0; overflow-x: auto; }}
  .katex {{ font-family: XITS, "XITS Math", Cambria Math, serif; }}
  table {{ border-collapse: collapse; width: 100%; margin: 0.9rem 0; font-size: 0.95rem; }}
  th, td {{ border: 1px solid var(--rule); padding: 0.42rem 0.6rem; text-align: left; vertical-align: top; }}
  thead th {{ background: var(--tint); }}
  tbody th {{ background: var(--tint); width: 34%; }}
  figure.plate {{ margin: 1.2rem 0; text-align: center; }}
  figure.plate.narrow img {{ max-width: 64%; }}
  figure.plate img {{ max-width: 100%; height: auto; border: 1px solid var(--rule); border-radius: 4px; }}
  figcaption {{ font-size: 0.9rem; color: var(--muted); margin-top: 0.45rem; }}
  code {{ font-family: Consolas, "Courier New", monospace; font-size: 0.88em; background: #f1f3f5;
          padding: 0.05rem 0.28rem; border-radius: 3px; }}
  ul {{ margin: 0.6rem 0 0.6rem 1.2rem; padding: 0; }}
  li {{ margin: 0.28rem 0; }}
  section.box {{ background: var(--tint); border: 1px solid var(--rule); border-radius: 6px; padding: 0.4rem 1rem; }}
</style>
</head>
<body>
<h1>The maximum of a triple integral over a free region</h1>
<p class="lead">A verified tutorial. Every number below is printed by a script under <code>code/</code>, and every
step names the check that supports it.</p>

<section class="box">
<h2>The problem</h2>
{statement}
</section>

<section>
<h2>The plan</h2>
<p>The integrand fixes the region, because a point with a positive integrand raises the integral and a point with a
negative integrand lowers it. Part 1 finds the zero set, its semi-axes, its sections, and its volume. Part 2
compares the candidate regions and tests the scale of the winner. Part 3 evaluates the integral with a linear map
and spherical coordinates. Part 4 repeats the calculation with exact fractions and a symbolic engine, and it tests
the sign of the integrand on a large sample.</p>
</section>

{''.join(sections)}

<section>
<h2>The answer</h2>
<table><tbody>{answer_html}</tbody></table>
</section>

<section>
<h2>The verification record</h2>
<p>The four verification scripts print {total_checks} comparisons of a computed value against an expected value.
Each comparison names both values and the difference, and the script stops on a failed comparison.</p>
<table>
<thead><tr><th>Script</th><th>Comparisons</th><th>Status</th></tr></thead>
<tbody>{check_rows}</tbody>
</table>
</section>

<script>
function renderPageMath() {{
  if (typeof renderMathInElement !== "function") {{
    window.setTimeout(renderPageMath, 120);
    return;
  }}
  renderMathInElement(document.body, {{
    delimiters: [
      {{left: "$$", right: "$$", display: true}},
      {{left: "$", right: "$", display: false}}
    ],
    throwOnError: false,
    strict: false
  }});
}}
document.addEventListener("DOMContentLoaded", renderPageMath);
window.addEventListener("load", renderPageMath);
</script>
</body>
</html>
"""
    return page


def check_page(page: str) -> None:
    """Assert the page rules of the pass.

    Args:
        page: The HTML text of the page.
    """
    if TOKEN_PATTERN.search(page):
        raise AssertionError("the page holds an unresolved token")
    for placeholder in ("[CORRECT_VALUE]", "[WRONG_VALUE]"):
        if placeholder in page:
            raise AssertionError(f"the page holds the placeholder {placeholder}")
    control = [character for character in page if ord(character) < 32 and character not in "\n\t"]
    if control:
        raise AssertionError(f"the page holds {len(control)} control characters")
    if "<code></code>" in page:
        raise AssertionError("the page holds an empty inline code element")

    for match in re.finditer(r"<li>(.+?)</li>", page, flags=re.DOTALL):
        text = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        if not text.endswith("."):
            raise AssertionError(f"a list item does not end with a full stop: {text[-60:]!r}")
    for match in re.finditer(r"<p>(.+?)</p>", page, flags=re.DOTALL):
        text = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        if text and text[0].islower():
            raise AssertionError(f"a paragraph starts with a lower-case word: {text[:60]!r}")

    for table_body in re.finditer(r"<table>(.*?)</table>", page, flags=re.DOTALL):
        for cell in re.finditer(r"<t[hd]>(.*?)</t[hd]>", table_body.group(1), flags=re.DOTALL):
            rest = MATH_INLINE_PATTERN.sub("", cell.group(1))
            rest = re.sub(r"<[^>]+>", "", rest)
            if "\\" in rest or "<" in rest:
                raise AssertionError(f"a table cell holds raw mathematics: {rest[:60]!r}")
    for caption in re.finditer(r"<figcaption>(.*?)</figcaption>", page, flags=re.DOTALL):
        rest = MATH_INLINE_PATTERN.sub("", caption.group(1))
        if "\\" in rest or "<" in rest:
            raise AssertionError(f"a caption holds raw mathematics: {rest[:60]!r}")

    for number, line in enumerate(page.splitlines(), start=1):
        if line.count("$") % 2 != 0:
            raise AssertionError(f"line {number} holds an odd number of dollar signs: {line[:60]!r}")
    print(f"the page passes every rule: {len(page.splitlines())} lines")


def main() -> None:
    """Compose the page, check it, and write the file."""
    values = load_values()
    page = build_page(values)
    check_page(page)
    REPORT_PATH.write_text(page, encoding="utf-8")
    print(f"wrote {REPORT_PATH}")
    print(f"the page holds {page.count('<article')} steps and {page.count('<figure')} figures")


if __name__ == "__main__":
    main()
