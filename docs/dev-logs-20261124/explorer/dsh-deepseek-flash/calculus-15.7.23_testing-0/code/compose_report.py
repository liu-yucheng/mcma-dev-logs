"""Compose the tutorial page of the session from the step files, the values, and the figures.

The script reads the step files in order, joins each indented continuation line to the list item
that it continues, replaces each figure marker with a Base64 data uniform resource identifier,
interpolates every numeral from the JSON records of the verification scripts, and asserts the
properties of the composed page before it writes the file.
"""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

CODE_DIRECTORY = Path(__file__).resolve().parent
"""Directory of the product code."""

WORKSPACE = CODE_DIRECTORY.parent
"""Workspace of the session."""

STEP_DIRECTORY = WORKSPACE / "steps"
"""Directory of the step files."""

OUTPUT_DIRECTORY = CODE_DIRECTORY / "outputs"
"""Directory of the JSON records of the parts."""

FIGURE_DIRECTORY = CODE_DIRECTORY / "figures"
"""Directory of the rendered figures."""

REPORT_PATH = WORKSPACE / "report.html"
"""Path of the composed page."""

FIGURE_PATTERN = re.compile(r"!\[figure\]\(FIGURE:([^|]+)\|(.+)\)")
"""Pattern of a figure marker: file name and caption."""

CODE_PATTERN = re.compile(r"`([^`]+)`")
"""Pattern of an inline code span."""


def load_values() -> dict[str, str]:
    """Read every published value of the four parts into one dictionary."""
    values: dict[str, str] = {}
    for path in sorted(OUTPUT_DIRECTORY.glob("part*_values.json")):
        values.update(json.loads(path.read_text(encoding="utf-8")))
    return values


def interpolate(text: str, values: dict[str, str]) -> str:
    """Replace each token with its published value, and refuse an unknown token."""
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise KeyError(f"the page uses an unpublished value: {key}")
        return values[key]

    return re.sub(r"\{\{(\w+)\}\}", replace, text)


def escape_text(text: str) -> str:
    """Escape the two characters that HTML reads, and keep the dollar signs."""
    return html.escape(text, quote=False)


def inline(text: str) -> str:
    """Convert one paragraph with inline code spans and inline mathematics."""
    escaped = escape_text(text)
    escaped = CODE_PATTERN.sub(lambda match: "<code>" + match.group(1) + "</code>", escaped)
    return escaped


def figure_markup(match: re.Match[str]) -> str:
    """Return the markup of one figure with a Base64 data uniform resource identifier."""
    name = match.group(1).strip()
    caption = match.group(2).strip()
    path = FIGURE_DIRECTORY / name
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    escaped_caption = inline(caption)
    return (f'<figure>\n<img alt="{escaped_caption}" '
            f'src="data:image/png;base64,{payload}">\n'
            f"<figcaption>{escaped_caption}</figcaption>\n</figure>")


def blocks_of(markdown: str) -> list[str]:
    """Split one step file into HTML blocks: headings, paragraphs, and display mathematics."""
    lines = markdown.splitlines()
    joined: list[str] = []
    for line in lines:
        if line.startswith(("    ", "\t")) and joined and joined[-1].strip():
            joined[-1] = joined[-1].rstrip() + " " + line.strip()
            continue
        joined.append(line)

    blocks: list[str] = []
    paragraph: list[str] = []
    index = 0
    while index < len(joined):
        line = joined[index]
        stripped = line.strip()
        if stripped.startswith("$$"):
            if paragraph:
                blocks.append(" ".join(paragraph))
                paragraph = []
            body: list[str] = []
            if stripped.endswith("$$") and len(stripped) > 2:
                body.append(stripped)
                index += 1
            else:
                index += 1
                while index < len(joined) and not joined[index].strip().endswith("$$"):
                    body.append(joined[index].strip())
                    index += 1
                if index < len(joined):
                    body.append(joined[index].strip())
                    index += 1
            blocks.append("DISPLAY:" + " ".join(body))
            continue
        if stripped.startswith("#"):
            if paragraph:
                blocks.append(" ".join(paragraph))
                paragraph = []
            level = len(stripped) - len(stripped.lstrip("#"))
            blocks.append(f"HEADING:{level}:{stripped[level:].strip()}")
            index += 1
            continue
        if not stripped:
            if paragraph:
                blocks.append(" ".join(paragraph))
                paragraph = []
            index += 1
            continue
        paragraph.append(stripped)
        index += 1
    if paragraph:
        blocks.append(" ".join(paragraph))
    return blocks


def render_step(markdown: str) -> str:
    """Return the HTML of one step file."""
    pieces: list[str] = []
    for block in blocks_of(markdown):
        if block.startswith("HEADING:"):
            _, level, text = block.split(":", 2)
            pieces.append(f"<h{level}>{inline(text)}</h{level}>")
        elif block.startswith("DISPLAY:"):
            pieces.append(f"<div class=\"display\">{escape_text(block[8:])}</div>")
        elif FIGURE_PATTERN.search(block) and len(FIGURE_PATTERN.sub("", block).strip()) < 3:
            match = FIGURE_PATTERN.search(block)
            pieces.append(f"<p>@@{match.group(0)}@@</p>")
        else:
            pieces.append(f"<p>{inline(block)}</p>")
    return "\n".join(pieces)


def page_head() -> str:
    """Return the head of the page with the fonts and the mathematics style sheet."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wedge cut from a cylinder: a worked tutorial</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
  :root { --ink: #1d232b; --soft: #5a6672; --line: #d6dde5; --panel: #f6f8fa; }
  body { font-family: Cambria, "Georgia", serif; color: var(--ink); margin: 0 auto;
         max-width: 62rem; padding: 2.2rem 1.6rem 4rem; line-height: 1.55; }
  h1 { font-size: 1.85rem; line-height: 1.2; margin: 0 0 0.4rem; }
  h2 { font-size: 1.35rem; margin: 2.2rem 0 0.6rem; border-bottom: 1px solid var(--line);
       padding-bottom: 0.3rem; }
  h3 { font-size: 1.1rem; margin: 1.5rem 0 0.4rem; color: #24303c; }
  p { margin: 0.65rem 0; }
  .display { margin: 1rem 0; text-align: center; overflow-x: auto; }
  code { font-family: "Consolas", monospace; font-size: 0.9em; background: var(--panel);
         padding: 0.08em 0.3em; border-radius: 3px; }
  figure { margin: 1.4rem 0; text-align: center; }
  figure img { max-width: 100%; border: 1px solid var(--line); border-radius: 4px; }
  figcaption { font-size: 0.9rem; color: var(--soft); margin-top: 0.5rem; }
  .statement { background: var(--panel); border-left: 4px solid #7fa8c9; padding: 0.9rem 1.1rem;
               margin: 1rem 0; }
  .katex { font-family: XITS, "Cambria Math", serif; font-size: 1.03em; }
</style>
</head>
<body>
"""


def page_tail() -> str:
    """Return the script that renders the mathematics and closes the page."""
    return """<script>
  document.addEventListener("DOMContentLoaded", function () {
    renderMathInElement(document.body, {
      delimiters: [{left: "$$", right: "$$", display: true},
                   {left: "$", right: "$", display: false}],
      throwOnError: false
    });
  });
</script>
</body>
</html>
"""


def main() -> None:
    """Compose the page and assert its properties."""
    values = load_values()
    statement = (WORKSPACE / "problem" / "problem.md").read_text(encoding="utf-8")
    quoted: list[str] = []
    for line in statement.splitlines():
        if line.startswith(">"):
            piece = line.lstrip("> ").strip()
            if piece.startswith("(a)") or piece.startswith("(b)") or not quoted:
                quoted.append(piece)
            else:
                quoted[-1] = quoted[-1] + " " + piece
    statement_html = "\n".join(f"<p>{inline(line)}</p>" for line in quoted if line)

    body: list[str] = ["<h1>Wedge cut from a cylinder by two planes</h1>",
                       '<div class="statement">',
                       "<h2>Problem</h2>",
                       statement_html,
                       "</div>"]

    step_paths = sorted(STEP_DIRECTORY.glob("part*_step*.md"))
    if len(step_paths) != 4:
        raise AssertionError(f"expected four step files, found {len(step_paths)}")
    for path in step_paths:
        markdown = interpolate(path.read_text(encoding="utf-8"), values)
        body.append(render_step(markdown))

    body.append("""<h2>Answers</h2>
<p>Part (a). The volume is the iterated integral $V=\\int_{0}^{1}\\int_{0}^{\\sqrt{1-z^{2}}}\\int_{0}^{y}1\\,dx\\,dy\\,dz$.</p>
<p>Part (b). The exact value is $V=""" + values["p3_exact_fraction"] + """$, that is """ +
                values["p3_exact_decimal"] + """ as a decimal.</p>
<p>The second method of Part 4 gives """ + values["p4_polar"] + """ by the polar rule and """ +
                values["p4_midpoint"] + """ by the grid rule.</p>""")

    page = page_head() + "\n".join(body) + "\n" + page_tail()
    page = re.sub(r"<p>@@!\[figure\]\(FIGURE:([^|]+)\|(.*)\)@@</p>", figure_markup, page)

    control = [character for character in page if ord(character) < 32 and character not in "\n\t"]
    if control:
        raise AssertionError(f"the page holds {len(control)} control characters")
    for marker in ("[WRONG_VALUE]", "[CORRECT_VALUE]", "{{"):
        if marker in page:
            raise AssertionError(f"the page keeps the marker {marker}")
    if "<code></code>" in page:
        raise AssertionError("the page holds an empty inline code element")
    for line in page.splitlines():
        if line.count("$") % 2 != 0:
            raise AssertionError(f"a line holds an odd number of dollar signs: {line[:80]}")
    for paragraph in re.findall(r"<p>(.*?)</p>", page, flags=re.S):
        text = re.sub(r"<[^>]+>", "", paragraph).strip()
        if text and text[0].islower():
            raise AssertionError(f"a paragraph starts with a lower-case word: {text[:60]}")
    figure_count = page.count("<figure>")
    if figure_count != 2:
        raise AssertionError(f"expected two figures, found {figure_count}")

    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {REPORT_PATH} with {len(page)} characters, {figure_count} figures, "
          f"{len(step_paths)} steps")


if __name__ == "__main__":
    main()
