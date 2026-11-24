"""Write one Markdown file for each step, and compose the product page.

The script writes `<workspace>/steps/part<number>_step<number>.md` for each step of
steps_content.py, then composes `<workspace>/report.html` and its copy `<workspace>/
tutorial.html`. Every figure goes into the page as a Base64 data uniform resource identifier, so
the page needs no other file. Every mathematical expression is LaTeX source, and the page
renders it with KaTeX.
"""

from __future__ import annotations

import base64
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from six_forms import SIX_FORMS, VERIFIED_CHECKS
from steps_content import FIGURE_NOTE, FINAL_ANSWERS, PARTS, STATEMENT

# Root of the workspace of this session.
WORKSPACE = Path(__file__).resolve().parent.parent

# Directory of the step files.
STEPS_DIRECTORY = WORKSPACE / "steps"

# Directory of the figures.
FIGURES_DIRECTORY = WORKSPACE / "code" / "figures"

# Path of the product page.
REPORT_PATH = WORKSPACE / "report.html"

# Path of the copy of the product page.
TUTORIAL_PATH = WORKSPACE / "tutorial.html"

# Version of the KaTeX distribution.
KATEX_VERSION = "0.16.11"

# Base address of the KaTeX distribution.
KATEX_BASE = f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/"

# The style sheet of the page.
STYLE = """
:root {
  --ink: #1f2933;
  --muted: #52606d;
  --line: #d9e2ec;
  --accent: #1f3b57;
  --wash: #f5f8fb;
}
body {
  margin: 0 auto;
  max-width: 60rem;
  padding: 2.2rem 1.6rem 4rem;
  background: #ffffff;
  color: var(--ink);
  font-family: Cambria, "Cambria Math", Georgia, serif;
  font-size: 1.02rem;
  line-height: 1.62;
}
h1 { font-size: 1.85rem; line-height: 1.25; margin: 0 0 0.6rem; }
h2 { font-size: 1.35rem; margin: 2.6rem 0 0.5rem; color: var(--accent); }
h3 { font-size: 1.12rem; margin: 1.9rem 0 0.4rem; }
p { margin: 0.55rem 0; }
.katex, .katex-display { font-family: "XITS Math", "XITS", "Cambria Math", KaTeX_Main, serif; }
.lede { color: var(--muted); font-size: 0.98rem; }
.statement {
  border-left: 4px solid var(--accent);
  background: var(--wash);
  padding: 0.9rem 1.1rem;
  margin: 1.1rem 0 1.4rem;
}
.note {
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  color: var(--muted);
  font-size: 0.95rem;
  background: #fcfdfe;
}
.step {
  border-top: 1px solid var(--line);
  padding-top: 0.9rem;
  margin-top: 1.6rem;
}
.step h3 { margin-top: 0; }
.label {
  font-variant: small-caps;
  letter-spacing: 0.04em;
  color: var(--accent);
  font-size: 0.92rem;
  margin-right: 0.35rem;
}
.result {
  background: #eef6f0;
  border-left: 3px solid #3f7d58;
  padding: 0.6rem 0.9rem;
  margin: 0.8rem 0 0.5rem;
}
.check {
  color: var(--muted);
  font-size: 0.94rem;
  border-left: 3px solid var(--line);
  padding-left: 0.9rem;
  margin-top: 0.6rem;
}
figure { margin: 1.3rem 0; }
figure img { width: 100%; height: auto; border: 1px solid var(--line); border-radius: 6px; }
figcaption { color: var(--muted); font-size: 0.92rem; margin-top: 0.45rem; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.96rem; }
th, td { border: 1px solid var(--line); padding: 0.45rem 0.6rem; text-align: left; vertical-align: top; }
th { background: var(--wash); }
code, pre { font-family: Consolas, "Courier New", monospace; font-size: 0.9rem; }
pre { background: var(--wash); border: 1px solid var(--line); border-radius: 6px; padding: 0.8rem;
      overflow-x: auto; }
.display { overflow-x: auto; overflow-y: hidden; }
"""

# The final block of the page, which starts the KaTeX renderer.
SCRIPT = """
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


def mark_inline_code(text: str) -> str:
    """Escape a text and turn each pair of backticks into an inline code element.

    Args:
        text: The Markdown text.

    Returns:
        The escaped HTML with inline code elements.
    """
    escaped = html.escape(text)
    return re.sub(r"`([^`]+)`", r"<code></code>", escaped)


def paragraphs(text: str) -> str:
    """Convert a small block of Markdown into HTML paragraphs and display math.

    A block that starts with two dollar signs becomes a display block. A block that starts with
    a dash becomes a list. Every other block becomes a paragraph. The dollar signs stay in the
    text, because KaTeX reads them after the document is ready.

    Args:
        text: The Markdown text of one field of a step.

    Returns:
        The HTML of that field.
    """
    pieces = []
    for block in text.split("\n\n"):
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("$$"):
            pieces.append(f'<div class="display">{html.escape(stripped)}</div>')
        elif stripped.startswith("- "):
            items = "".join(
                f"<li>{mark_inline_code(line[2:].strip())}</li>"
                for line in stripped.split("\n")
                if line.strip().startswith("- ")
            )
            pieces.append(f"<ul>{items}</ul>")
        else:
            pieces.append(f"<p>{mark_inline_code(stripped)}</p>")
    return "\n".join(pieces)


def figure_block(file_name: str, caption: str) -> str:
    """Return the HTML of one figure with a Base64 data uniform resource identifier.

    Args:
        file_name: Name of the figure file below the figures directory.
        caption: Caption of the figure.

    Returns:
        The HTML of the figure.
    """
    path = FIGURES_DIRECTORY / file_name
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        "<figure>"
        f'<img alt="{html.escape(caption)}" src="data:image/png;base64,{payload}">'
        f"<figcaption>{html.escape(caption)}</figcaption>"
        "</figure>"
    )


def write_step_files() -> list[Path]:
    """Write one Markdown file for each step.

    Returns:
        The paths of the written files.
    """
    STEPS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    written = []
    for part in PARTS:
        for step in part["steps"]:
            stem = f"part{part['number']}_step{step['number'].split('.')[1]}"
            path = STEPS_DIRECTORY / f"{stem}.md"
            parts_text = [
                f"# Part {part['number']}, Step {step['number']}: {step['title']}",
                "",
                f"Part goal: {part['goal']}",
                "",
                "## Reason",
                "",
                step["reason"],
                "",
                "## Computation",
                "",
                step["computation"],
                "",
                "## Result",
                "",
                step["result"],
                "",
                "## Verification",
                "",
                step["verify"],
                "",
            ]
            path.write_text("\n".join(parts_text), encoding="utf-8", newline="\n")
            written.append(path)
    return written


def build_table() -> str:
    """Return the HTML of the table of the six orders.

    Returns:
        The HTML of the table.
    """
    body = "".join(
        f"<tr><td>{order}</td><td>{integral}</td></tr>" for order, integral in SIX_FORMS
    )
    header = "<tr><th>Order, innermost first</th><th>Integral</th></tr>"
    return f"<table><thead>{header}</thead><tbody>{body}</tbody></table>"


def build_verified_table() -> str:
    """Return the HTML of the table of the verified values.

    Returns:
        The HTML of the table.
    """
    body = "".join(
        f"<tr><td>{check}</td><td>{quantity}</td><td>{value}</td><td>{margin}</td></tr>"
        for check, quantity, value, margin in VERIFIED_CHECKS
    )
    header = "<tr><th>Check</th><th>Quantity</th><th>Value</th><th>Margin</th></tr>"
    return f"<table><thead>{header}</thead><tbody>{body}</tbody></table>"


def build_page() -> str:
    """Return the HTML of the product page.

    Returns:
        The HTML of the page.
    """
    sections = []
    sections.append(
        f"<h1>Six iterated integrals over one solid</h1>"
        f'<p class="lede">A verified tutorial for Section 15.7, Exercise 29. '
        f"The page shows the reason of each step before its computation, and it names the script "
        f"that checks every number.</p>"
        f'<div class="statement"><p><span class="label">Problem</span></p>'
        f"<p>{html.escape(STATEMENT)}</p></div>"
        f'<p class="note">{html.escape(FIGURE_NOTE)}</p>'
    )
    answers = "".join(f"<tr><td>{part}</td><td>{text}</td></tr>" for part, text in FINAL_ANSWERS)
    sections.append(
        "<h2>Answers at a glance</h2>"
        f"<table><thead><tr><th>Part</th><th>Answer</th></tr></thead><tbody>{answers}</tbody></table>"
    )
    for part in PARTS:
        sections.append(f"<h2>Part {part['number']}. {part['title']}</h2>")
        sections.append(f"<p><span class=\"label\">Goal</span>{html.escape(part['goal'])}</p>")
        for file_name, caption in part["figures"]:
            sections.append(figure_block(file_name, caption))
        for step in part["steps"]:
            block = [
                f'<div class="step"><h3>Step {step["number"]}. {step["title"]}</h3>',
                f'<p><span class="label">Reason</span></p>',
                paragraphs(step["reason"]),
                f'<p><span class="label">Computation</span></p>',
                paragraphs(step["computation"]),
                f'<div class="result"><span class="label">Result</span>'
                f'{paragraphs(step["result"])}</div>',
                f'<div class="check"><span class="label">Verification</span>'
                f"{paragraphs(step['verify'])}</div></div>",
            ]
            sections.append("\n".join(block))
        sections.append(
            f'<p class="check"><span class="label">Part check</span>'
            f"The script <code>{html.escape(part['verify_script'])}</code> verifies this part. "
            f"It runs with <code>code/.venv/Scripts/python.exe {html.escape(part['verify_script'])}"
            f"</code>.</p>"
        )
    sections.append("<h2>The six forms in one table</h2>")
    sections.append(build_table())
    sections.append("<h2>Verified results</h2>")
    sections.append(build_verified_table())
    sections.append(
        "<h2>How to reproduce</h2>"
        "<p>Each script prints the computed value and the expected value, and stops when the "
        "two disagree. The environment holds <code>numpy</code>, <code>scipy</code>, and "
        "<code>matplotlib</code> at the versions of <code>code/requirements.txt</code>.</p>"
        "<pre>code/.venv/Scripts/python.exe code/part1_verify.py\n"
        "code/.venv/Scripts/python.exe code/part2_verify.py\n"
        "code/.venv/Scripts/python.exe code/part3_verify.py\n"
        "code/.venv/Scripts/python.exe code/part4_verify.py\n"
        "code/.venv/Scripts/python.exe code/part5_verify.py\n"
        "code/.venv/Scripts/python.exe code/part6_verify.py\n"
        "code/.venv/Scripts/python.exe code/part1_figure1.py</pre>"
        "<p>The random seed of every sampled check is printed in the script that uses it.</p>"
    )
    head = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Six iterated integrals over one solid</title>\n"
        f'<link rel="stylesheet" href="{KATEX_BASE}katex.min.css">\n'
        f"<style>{STYLE}</style>\n</head>\n<body>\n"
    )
    tail = (
        f'\n<script src="{KATEX_BASE}katex.min.js"></script>\n'
        f'<script src="{KATEX_BASE}contrib/auto-render.min.js"></script>\n'
        f"<script>{SCRIPT}</script>\n</body>\n</html>\n"
    )
    return head + "\n".join(sections) + tail


def main() -> None:
    """Write the step files, the product page, and its copy."""
    written = write_step_files()
    page = build_page()
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    TUTORIAL_PATH.write_text(page, encoding="utf-8", newline="\n")
    print(f"step files written = {len(written)}")
    print(f"report page bytes = {len(page.encode('utf-8'))}")
    print(f"figures embedded = {sum(len(part['figures']) for part in PARTS)}")
    print(f"count of tab characters in the page = {page.count(chr(9))}")
    print(f"wrote {REPORT_PATH}")
    print(f"wrote {TUTORIAL_PATH}")


if __name__ == "__main__":
    main()
