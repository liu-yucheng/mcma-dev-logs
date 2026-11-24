"""Compose the tutorial page `report.html` from the step files and the figures.

The script reads the step files in the order of `PARTS`, converts the small
Markdown subset that the steps use into HTML, inlines every figure as a Base64
data uniform resource identifier, runs the four verification scripts, and writes
the whole page to `<workspace>/report.html`.

The script stops with an assertion when a figure file is absent, when a step
names a script that does not exist, or when a step file holds a tab character.
"""

import base64
import html
import io
import os
import re
import subprocess
import sys

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""The problem workspace, found from the location of this script."""

PYTHON = sys.executable
"""The interpreter that runs the verification scripts."""

STEPS = {
    "part1": ("Part 1", "Read the three limits", ("part1_step1.md", "part1_step2.md", "part1_step3.md")),
    "part2": ("Part 2", "The three families of cross sections",
              ("part2_step1.md", "part2_step2.md", "part2_step3.md")),
    "part3": ("Part 3", "The corner points and the faces", ("part3_step1.md", "part3_step2.md")),
    "part4": ("Part 4", "The sketch and its check", ("part4_step1.md", "part4_step2.md", "part4_step3.md")),
}
"""The four parts of the tutorial, with the title and the steps of each part."""

PART_INTRO = {
    "part1": "The three pairs of limits are the only data of the exercise. This part reads them in the order "
             "that the differentials give, and it turns the reading into six inequalities.",
    "part2": "A cross section shows the shape of the solid in one plane. This part cuts the solid in three "
             "directions, and it derives every section from the inequalities of Part 1.",
    "part3": "The corner points and the faces follow from the inequalities, not from a picture. This part "
             "produces both, so that the drawing of Part 4 rests on checked data.",
    "part4": "This part draws the solid and then checks the drawing against the integral in three "
             "independent ways.",
}
"""One introductory sentence for each part."""

FIGURES = (
    ("after:part2_step3.md", "code/figures/part2_figure1.png", "Figure 1",
     "One cross section from each family. Every polygon comes from the six limits, and every area in a title "
     "comes from the same script that checks it. The drawing comes from <code>code/part2_figure1.py</code>."),
    ("after:part4_step1.md", "code/figures/part4_figure2.png", "Figure 2",
     "The base triangle in the plane $y=0$, seen from above, with one level line $z=2/5$, the width $1-z$, "
     "and the point where Figure 3 carries the height bar. The drawing comes from "
     "<code>code/part4_figure2.py</code>."),
    ("after:part4_step2.md", "code/figures/part4_figure3.png", "Figure 3",
     "The sketch of the solid: the base triangle, the three walls $x=0$, $z=0$, and $x+z=1$, and the top "
     "face $y+2z=2$. Each dark dot marks a point of the face that the legend names. The z axis is drawn "
     "dashed where it runs inside the solid. The drawing comes from <code>code/part4_figure3.py</code>."),
)
"""For each figure: the place in the page, the file, the label, and the caption."""

VERIFY_SCRIPTS = ("code/part1_verify.py", "code/part2_verify.py", "code/part3_verify.py", "code/part4_verify.py")
"""The four verification scripts, in the order of the parts."""

SCRIPT_PATTERN = re.compile(r"code/(part\d_verify\.py)")
"""Pattern that finds the name of the script in the text of a step."""

TAB = "\t"
"""The character that must not appear in any step file."""


def read_step(name: str) -> str:
    """Return the text of one step file and check it for a tab character."""
    path = os.path.join(WORKSPACE, "steps", name)
    text = io.open(path, encoding="utf-8").read()
    assert TAB not in text, f"{name} holds a tab character"
    for script in SCRIPT_PATTERN.findall(text):
        assert os.path.exists(os.path.join(WORKSPACE, "code", script)), f"{name} names a missing {script}"
    return text


def inline(text: str) -> str:
    """Convert the inline Markdown of one line and keep every math segment unchanged."""
    pieces = re.split(r"(\$[^$]+\$)", text)
    result = []
    for piece in pieces:
        if piece.startswith("$") and piece.endswith("$") and len(piece) > 2:
            result.append(piece)
            continue
        escaped = html.escape(piece, quote=False)
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
        result.append(escaped)
    return "".join(result)


def convert(text: str) -> str:
    """Convert the Markdown subset of a step file into HTML."""
    lines = text.split("\n")
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("$$"):
            block: list[str] = []
            body = stripped[2:]
            if body.endswith("$$") and len(body) > 2:
                block.append(body[:-2])
                index += 1
            else:
                block.append(body)
                index += 1
                while index < len(lines) and not lines[index].strip().endswith("$$"):
                    block.append(lines[index])
                    index += 1
                if index < len(lines):
                    block.append(lines[index].strip()[:-2])
                    index += 1
            output.append('<div class="math-display">$$' + "\n".join(block).strip() + "$$</div>")
            continue
        if stripped.startswith("## "):
            output.append("<h3>" + inline(stripped[3:]) + "</h3>")
            index += 1
            continue
        if stripped.startswith("|"):
            rows: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(lines[index].strip())
                index += 1
            output.append(build_table(rows))
            continue
        if stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append("<li>" + inline(lines[index].strip()[2:]) + "</li>")
                index += 1
            output.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while index < len(lines) and re.match(r"^\d+\.\s", lines[index].strip()):
                items.append("<li>" + inline(re.sub(r"^\d+\.\s+", "", lines[index].strip())) + "</li>")
                index += 1
            output.append("<ol>" + "".join(items) + "</ol>")
            continue
        if stripped.startswith("> "):
            block = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                block.append(lines[index].strip().lstrip(">").strip())
                index += 1
            output.append('<blockquote class="answer">' + convert(" ".join(block)) + "</blockquote>")
            continue
        paragraph = [stripped]
        index += 1
        while index < len(lines) and lines[index].strip() and not lines[index].strip().startswith(
            ("## ", "$$", "- ", "> ", "|")
        ):
            paragraph.append(lines[index].strip())
            index += 1
        output.append("<p>" + inline(" ".join(paragraph)) + "</p>")
    return "\n".join(output)


def build_table(rows: list[str]) -> str:
    """Build an HTML table from the Markdown rows of a table."""
    cells = [[cell.strip() for cell in row.strip("|").split("|")] for row in rows]
    header = cells[0]
    body = [row for row in cells[2:]] if len(cells) > 1 and set("".join(cells[1])) <= set("-: ") else cells[1:]
    head_html = "".join("<th>" + inline(cell) + "</th>" for cell in header)
    body_html = "".join(
        "<tr>" + "".join("<td>" + inline(cell) + "</td>" for cell in row) + "</tr>" for row in body
    )
    return ('<table class="face-table"><thead><tr>' + head_html + "</tr></thead><tbody>"
            + body_html + "</tbody></table>")


def figure_html(path: str, label: str, caption: str) -> str:
    """Return one figure block with the image inlined as a data uniform resource identifier."""
    absolute = os.path.join(WORKSPACE, path)
    assert os.path.exists(absolute), f"the figure {path} is absent"
    with open(absolute, "rb") as handle:
        payload = base64.b64encode(handle.read()).decode("ascii")
    return (
        '<figure class="drawing">'
        f'<img alt="{label}" src="data:image/png;base64,{payload}">'
        f'<figcaption><strong>{label}.</strong> {caption}</figcaption>'
        "</figure>"
    )


def run_script(path: str) -> str:
    """Run one verification script and return its standard output."""
    result = subprocess.run(
        [PYTHON, os.path.basename(path)],
        cwd=os.path.join(WORKSPACE, "code"),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def build_page() -> str:
    """Build the whole page and return it as one string."""
    figures_after: dict[str, list[str]] = {}
    for marker, path, label, caption in FIGURES:
        place = marker.split(":", 1)[1]
        figures_after.setdefault(place, []).append(figure_html(path, label, caption))

    sections: list[str] = []
    for key in ("part1", "part2", "part3", "part4"):
        number, title, step_names = STEPS[key]
        body = [f'<section class="part" id="{key}">', f"<h2>{number} — {title}</h2>",
                f'<p class="intro">{inline(PART_INTRO[key])}</p>']
        for name in step_names:
            body.append(f'<article class="step" id="{name[:-3]}">')
            body.append(convert(read_step(name)))
            body.append("</article>")
            for block in figures_after.get(name, []):
                body.append(block)
        body.append(f'<p class="part-answer"><strong>Answer of {number}.</strong> '
                    + inline(PART_ANSWER[key]) + "</p>")
        body.append("</section>")
        sections.append("\n".join(body))

    checks = []
    for path in VERIFY_SCRIPTS:
        output = html.escape(run_script(path), quote=False)
        checks.append(f'<section class="check"><h3>{path}</h3><pre class="no-math">{output}</pre></section>')

    return PAGE.replace("{{SECTIONS}}", "\n".join(sections)).replace("{{CHECKS}}", "\n".join(checks))


PART_ANSWER = {
    "part1": "the solid is $R = \\{(x,y,z) : 0 \\le x \\le 1,\\ 0 \\le z \\le 1-x,\\ 0 \\le y \\le 2-2z\\}$, "
             "which is the part of the box $0 \\le x \\le 1$, $0 \\le y \\le 2$, $0 \\le z \\le 1$ that also holds "
             "$x+z \\le 1$ and $y+2z \\le 2$.",
    "part2": "$A(z) = 2(1-z)^2$ at constant $z$, $A(x) = 1-x^2$ at constant $x$, and "
             "$A(y) = 1/2-y^2/8$ at constant $y$. All three families fall as their variable grows.",
    "part3": "five corner points $P_0$ to $P_4$ and five faces: the base $D$, the top face $y+2z=2$, and the "
             "three walls $x=0$, $z=0$, and $x+z=1$.",
    "part4": "the sketch in Figure 3. The volume $2/3$ is a check of that sketch, and it is not the requested "
             "answer.",
}
"""The answer of each part, as LaTeX source for the composed page."""

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sketch the solid of an iterated integral — a verified tutorial</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
  :root {
    --ink: #17222b;
    --soft: #5b6b78;
    --rule: #d5dde3;
    --accent: #1f4e79;
    --warm: #9c2f1c;
    --paper: #fbfaf7;
  }
  html { background: #eceff2; }
  body {
    font-family: Cambria, "Cambria Math", "XITS Math", Georgia, serif;
    font-size: 17px;
    line-height: 1.62;
    color: var(--ink);
    background: var(--paper);
    max-width: 940px;
    margin: 0 auto;
    padding: 48px 40px 96px;
    box-shadow: 0 0 0 1px var(--rule);
  }
  h1 { font-size: 30px; line-height: 1.25; margin: 0 0 8px; letter-spacing: -0.01em; }
  h2 { font-size: 23px; margin: 48px 0 6px; padding-top: 18px; border-top: 2px solid var(--rule); }
  h3 { font-size: 19px; margin: 30px 0 6px; color: var(--accent); }
  p { margin: 10px 0; }
  .lede { font-size: 18px; color: var(--soft); margin-bottom: 26px; }
  .intro { color: var(--soft); font-style: italic; margin-bottom: 18px; }
  .statement {
    background: #fff;
    border-left: 4px solid var(--accent);
    padding: 16px 22px;
    margin: 22px 0 28px;
    box-shadow: 0 1px 2px rgba(23, 34, 43, 0.08);
  }
  .statement p { margin: 6px 0; }
  .step { margin: 18px 0 26px; }
  .step h3 { margin-top: 0; }
  .part-answer {
    background: #eef4f9;
    border-left: 4px solid var(--accent);
    padding: 12px 20px;
    font-weight: 600;
  }
  blockquote.answer {
    margin: 18px 0;
    padding: 14px 20px;
    background: #fff8f0;
    border-left: 4px solid var(--warm);
  }
  .math-display { margin: 14px 0; text-align: center; overflow-x: auto; }
  figure.drawing { margin: 26px 0 30px; text-align: center; }
  figure.drawing img { max-width: 100%; height: auto; border: 1px solid var(--rule); background: #fff; }
  figcaption { font-size: 14.5px; color: var(--soft); margin-top: 8px; text-align: left; }
  table.face-table { border-collapse: collapse; margin: 16px 0; width: 100%; font-size: 15.5px; }
  table.face-table th, table.face-table td { border: 1px solid var(--rule); padding: 7px 10px; text-align: left; }
  table.face-table th { background: #eef4f9; }
  ul, ol { margin: 10px 0 10px 22px; }
  li { margin: 5px 0; }
  code {
    font-family: Consolas, "DejaVu Sans Mono", monospace;
    font-size: 0.88em;
    background: #eef1f4;
    padding: 1px 4px;
  }
  pre.no-math {
    font-family: Consolas, "DejaVu Sans Mono", monospace;
    font-size: 12.5px;
    line-height: 1.5;
    background: #10181f;
    color: #e6edf3;
    padding: 14px 16px;
    overflow-x: auto;
    border-radius: 3px;
  }
  .check { margin: 18px 0 26px; }
  .checks h2 { border-top: 2px solid var(--accent); }
  .katex, .katex .mathdefault, .math-display { font-family: "XITS Math", "Cambria Math", Cambria, serif; }
</style>
</head>
<body>
<h1>Sketch the solid whose volume is given by an iterated integral</h1>
<p class="lede">Calculus, Early Transcendentals, Section 15.7, Exercise 27. A tutorial with one checked
computation for every numerical claim.</p>

<div class="statement">
<p><strong>Statement.</strong> Sketch the solid whose volume is given by the iterated integral.</p>
<div class="math-display">$$\int_{0}^{1}\int_{0}^{1-x}\int_{0}^{2-2z} dy\,dz\,dx$$</div>
<p><strong>What the exercise asks for.</strong> One sketch of one solid region. It asks for no number and for
no value of the integral.</p>
</div>

<p>The integrand is $1$, so the integral equals the volume of the region. That fact is a check of the drawing,
and it is not the answer of the exercise. The tutorial keeps the two apart.</p>

<p>How to read this page. Part 1 reads the three pairs of limits and turns them into inequalities.
Part 2 cuts the solid in three directions. Part 3 derives the corner points and the faces. Part 4 draws the
solid and checks the drawing. Every step names the script that checks its numbers, and the last section of the
page holds the printed output of all four scripts.</p>

{{SECTIONS}}

<section class="checks">
<h2>Verified results</h2>
<p>Each block below is the standard output of one script, captured when this page was composed. The command
uses the interpreter of the session environment, <code>code/.venv</code>.</p>
{{CHECKS}}
</section>

<script>
document.addEventListener("DOMContentLoaded", function () {
  renderMathInElement(document.body, {
    delimiters: [
      {left: "$$", right: "$$", display: true},
      {left: "$", right: "$", display: false}
    ],
    ignoredClasses: ["no-math"],
    throwOnError: false
  });
});
</script>
</body>
</html>
"""


def main() -> None:
    """Build the page and write it to `report.html`."""
    page = build_page()
    assert "\t" not in page, "the page holds a tab character"
    output = os.path.join(WORKSPACE, "report.html")
    io.open(output, "w", encoding="utf-8", newline="\n").write(page)
    print(f"wrote {output} with {len(page)} bytes")


if __name__ == "__main__":
    main()
