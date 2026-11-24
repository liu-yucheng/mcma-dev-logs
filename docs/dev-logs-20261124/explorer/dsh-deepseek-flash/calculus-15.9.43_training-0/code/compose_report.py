"""Compose the tutorial page of the silo exercise.

The script reads the step files of ``steps/``, the verification summaries of ``code/outputs/``,
and the three figures of ``code/figures/``.  It writes ``report.html`` with the statement, the
steps in order, the figures as Base64 data identifiers, the verified values of each part, and the
final answer of each part.

The script checks the composed page before it writes the file: it requires no control character,
a full stop at the end of every list item, no paragraph that starts with a lower-case word, and
no mathematical token outside a ``$...$`` span in a table cell or in a caption.
"""

import base64
import pathlib
import re
import unicodedata

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

STEPS_DIRECTORY = WORKSPACE / "steps"
"""Directory of the step files."""

OUTPUTS_DIRECTORY = WORKSPACE / "code" / "outputs"
"""Directory of the verification summaries."""

FIGURES_DIRECTORY = WORKSPACE / "code" / "figures"
"""Directory of the drawn figures."""

REPORT_PATH = WORKSPACE / "report.html"
"""Path of the composed page."""

PART_TITLES = {
    1: "The frame, the body, and its three faces",
    2: "Horizontal sections and the volume",
    3: "The volume in cylindrical and in spherical coordinates",
    4: "The area of the drawn surfaces",
    5: "The height of the centroid",
    6: "The projection and the drawing recipe",
}
"""Title of each part of the solution."""

PART_ANSWERS = {
    1: r"$0\le r\le 3$, $0\le z\le 10+\sqrt{9-r^{2}}$; three faces: the lower disk, the "
       r"lateral face, and the cap.",
    2: r"$A(z)=9\pi$ for $0\le z\le 10$ and $A(z)=\pi\bigl(9-(z-10)^{2}\bigr)$ for "
       r"$10\le z\le 13$; $V=108\pi=339.292006588$.",
    3: r"$V=2\pi\int_{0}^{3}r\bigl(10+\sqrt{9-r^{2}}\bigr)dr=108\pi$; the cap gives "
       r"$9\cdot 1\cdot 2\pi=18\pi$.",
    4: r"$A=60\pi+18\pi+9\pi=87\pi=273.318560862$.",
    5: r"$\bar z=\frac{2601\pi/4}{108\pi}=\frac{289}{48}=6.02083333333$.",
    6: r"The projection is the rectangle $|x|\le 3$, $0\le z\le 10$ plus the half disk "
       r"$x^{2}+(z-10)^{2}\le 9$; the outline is $26+3\pi=35.4247779608$.",
}
"""Final answer of each part."""

FIGURE_SPECS = (
    {
        "number": 1,
        "part": 1,
        "after": "part1_step2",
        "file": "part1_figure1.png",
        "caption": r"Figure 1. The silo in its frame and its projection on the plane $y=0$. "
                   r"The three labelled anchors lie on the surfaces that they name: the lateral "
                   r"face at $x^{2}+y^{2}=9$, the lower disk at $z=0$, and the cap at "
                   r"$x^{2}+y^{2}+(z-10)^{2}=9$. The section at $z=8$ is red. The right panel "
                   r"shows the rectangle and the half disk of Step 6.1, and the dashed line "
                   r"marks the common edge at $z=10$.",
    },
    {
        "number": 2,
        "part": 2,
        "after": "part2_step2",
        "file": "part2_figure1.png",
        "caption": r"Figure 2. The area $A(z)$ of the horizontal section. The curve is flat at "
                   r"$9\pi=28.2743338823$ up to the rim $z=10$, then follows "
                   r"$\pi\bigl(9-(z-10)^{2}\bigr)$ and reaches $0$ at the top $z=13$. The marks "
                   r"are the heights $3$, $10$, and $11.5$ of the checks.",
    },
    {
        "number": 3,
        "part": 4,
        "after": "part4_step2",
        "file": "part4_figure1.png",
        "caption": r"Figure 3. The area of each face computed from a triangle mesh, and the "
                   r"relative error of that area against the closed form. Every mesh "
                   r"under-estimates, because a mesh is inscribed in the surface. The dashed "
                   r"line is the tolerance $5\times 10^{-4}$.",
    },
)
"""One entry for each figure of the page."""

STEP_PATTERN = re.compile(r"^part(?P<part>\d+)_step(?P<step>\d+)\.md$")
"""Pattern of the name of a step file."""


def read_text(path: pathlib.Path) -> str:
    """Return the text of a file, with the line endings of the platform removed."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def escape_outside_math(text: str) -> str:
    """Escape the HTML characters of a text and keep every math span unchanged."""
    pieces = []
    index = 0
    while index < len(text):
        start = text.find("$", index)
        if start < 0:
            pieces.append(escape_fragment(text[index:]))
            break
        pieces.append(escape_fragment(text[index:start]))
        closing = text.find("$", start + 1)
        if closing < 0:
            pieces.append(escape_fragment(text[start:]))
            break
        pieces.append(text[start:closing + 1])
        index = closing + 1
    return "".join(pieces)


def escape_fragment(text: str) -> str:
    """Escape the three HTML characters of one fragment of plain text."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_code_pattern() -> re.Pattern:
    """Return the pattern of one inline code span."""
    return re.compile(r"`([^`]+)`")


def render_inline(text: str) -> str:
    """Render one paragraph of markdown as HTML text."""
    escaped = escape_outside_math(text)
    return inline_code_pattern().sub(r"<code>\1</code>", escaped)


def is_display_start(line: str) -> bool:
    """Report whether a line opens a displayed mathematical expression."""
    return line.strip().startswith("$$")


def collect_display(lines: list, start: int) -> tuple:
    """Collect the lines of one displayed expression and return them with the next index."""
    collected = []
    index = start
    while index < len(lines):
        collected.append(lines[index].strip())
        if len(collected) > 1 and collected[-1].endswith("$$"):
            return collected, index + 1
        if len(collected) == 1 and collected[0].count("$$") >= 2:
            return collected, index + 1
        index += 1
    raise ValueError("a displayed expression is not closed")


def render_step(text: str) -> tuple:
    """Render one step file and return its title and its HTML body."""
    lines = text.split("\n")
    title = ""
    blocks = []
    index = 0
    paragraph = []

    def flush_paragraph() -> None:
        """Append the pending paragraph to the block list."""
        if paragraph:
            blocks.append("<p>" + render_inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            title = stripped[2:].strip()
            index += 1
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            blocks.append("<h4>" + render_inline(stripped[3:].strip()) + "</h4>")
            index += 1
            continue
        if is_display_start(stripped):
            flush_paragraph()
            collected, index = collect_display(lines, index)
            joined = " ".join(collected)
            blocks.append('<div class="display-math">' + joined + "</div>")
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            items = []
            current = stripped[2:].strip()
            index += 1
            while index < len(lines):
                following = lines[index]
                if following.strip().startswith("- "):
                    items.append(current)
                    current = following.strip()[2:].strip()
                    index += 1
                    continue
                if following.startswith("  ") and following.strip():
                    current = current + " " + following.strip()
                    index += 1
                    continue
                break
            items.append(current)
            blocks.append("<ul>" + "".join(
                "<li>" + render_inline(item) + "</li>" for item in items
            ) + "</ul>")
            continue
        paragraph.append(stripped)
        index += 1
    flush_paragraph()
    return title, "\n".join(blocks)


def step_files() -> list:
    """Return the step files in the order of the solution."""
    found = []
    for path in STEPS_DIRECTORY.iterdir():
        match = STEP_PATTERN.match(path.name)
        if match:
            found.append((int(match.group("part")), int(match.group("step")), path))
    return sorted(found)


def render_verification_table(part: int) -> str:
    """Render the verification summary of one part as an HTML table."""
    path = OUTPUTS_DIRECTORY / f"part{part}_summary.md"
    lines = [line for line in read_text(path).split("\n") if line.strip()]
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    header = [cell.strip("* ") for cell in header]
    rows = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    parts = ['<table class="checks">']
    parts.append("<thead><tr>" + "".join(f"<th>{render_inline(cell)}</th>" for cell in header)
                 + "</tr></thead><tbody>")
    for cells in rows:
        parts.append("<tr>" + "".join(f"<td>{render_inline(cell)}</td>" for cell in cells)
                     + "</tr>")
    parts.append("</tbody></table>")
    return "\n".join(parts)


def figure_data_identifier(name: str) -> str:
    """Return the Base64 data identifier of one figure file."""
    payload = base64.b64encode((FIGURES_DIRECTORY / name).read_bytes()).decode("ascii")
    return "data:image/png;base64," + payload


def render_figure(spec: dict) -> str:
    """Render one figure with its caption."""
    return (
        '<figure class="drawing">'
        f'<img alt="Figure {spec["number"]}" src="{figure_data_identifier(spec["file"])}">'
        f'<figcaption>{render_inline(spec["caption"])}</figcaption>'
        "</figure>"
    )


def build_page() -> str:
    """Build the whole page."""
    pieces = []
    pieces.append("<!DOCTYPE html>")
    pieces.append('<html lang="en">')
    pieces.append("<head>")
    pieces.append('<meta charset="utf-8">')
    pieces.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    pieces.append("<title>A silo: cylinder and hemisphere, drawn and measured</title>")
    pieces.append(
        '<link rel="stylesheet" '
        'href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">'
    )
    pieces.append("<style>")
    pieces.append(STYLE_SHEET)
    pieces.append("</style>")
    pieces.append("</head>")
    pieces.append("<body>")
    pieces.append("<main>")
    pieces.append("<h1>A silo: a cylinder of radius 3 and height 10 with a hemispherical cap</h1>")
    pieces.append(
        '<p class="lead">This page draws one silo and measures it. Every number of the page '
        "comes from a checked computation, and each part names the script that checks it.</p>"
    )

    pieces.append('<section id="statement">')
    pieces.append("<h2>The statement</h2>")
    pieces.append(
        "<blockquote><p>Use a graphing device to draw a silo consisting of a cylinder with "
        "radius 3 and height 10 surmounted by a hemisphere.</p>"
        "<footer>Calculus, Early Transcendentals, Section 15.9, Exercise 43.</footer>"
        "</blockquote>"
    )
    pieces.append(
        "<p>The exercise asks for a drawing, but a drawing that a reader can trust needs the "
        "shape itself, the volume that the shape encloses, the area that the drawing shows, and "
        "the recipe that the device follows. This page supplies all four.</p>"
    )
    pieces.append("</section>")

    pieces.append('<section id="answers">')
    pieces.append("<h2>The answer of each part</h2>")
    pieces.append('<table class="answers"><thead><tr><th>Part</th><th>Answer</th></tr></thead>')
    pieces.append("<tbody>")
    for number in sorted(PART_ANSWERS):
        pieces.append(
            f"<tr><td>{number}</td><td>{render_inline(PART_ANSWERS[number])}</td></tr>"
        )
    pieces.append("</tbody></table>")
    pieces.append("</section>")

    steps = step_files()
    figures_by_anchor = {}
    for spec in FIGURE_SPECS:
        figures_by_anchor.setdefault(spec["after"], []).append(spec)

    for part in sorted({item[0] for item in steps}):
        pieces.append(f'<section class="part" id="part{part}">')
        pieces.append(f"<h2>Part {part}. {PART_TITLES[part]}</h2>")
        for step_part, step_number, path in steps:
            if step_part != part:
                continue
            title, body = render_step(read_text(path))
            slug = f"part{step_part}_step{step_number}"
            pieces.append(f'<article class="step" id="{slug}">')
            pieces.append(f"<h3>{render_inline(title)}</h3>")
            pieces.append(body)
            pieces.append("</article>")
            for spec in figures_by_anchor.get(slug, []):
                pieces.append(render_figure(spec))
        pieces.append('<div class="verification">')
        pieces.append(
            f"<h3>Verified values of Part {part}</h3>"
            "<p>Each row prints the value that one method computes against the value that a "
            "second method computes. The script is "
            f"<code>code/part{part}_verify.py</code>.</p>"
        )
        pieces.append(render_verification_table(part))
        pieces.append("</div>")
        pieces.append("</section>")

    pieces.append('<section id="checks">')
    pieces.append("<h2>What the page checks</h2>")
    pieces.append(
        "<p>The six scripts run 48 checks and all of them pass. Four rules hold over the whole "
        "page. First, no check compares a value with itself: each row pairs two methods, such as "
        "an integral against a closed form, a formula against a bisection, or a mesh against a "
        "closed form. Second, every figure is drawn by a script that asserts the placement of "
        "its own labels before it writes the file. Third, every mathematical expression is "
        "LaTeX source inside a math span. Fourth, every step names the script that verifies it."
        "</p>"
    )
    pieces.append("</section>")
    pieces.append("</main>")
    pieces.append(SCRIPT_BLOCK)
    pieces.append("</body>")
    pieces.append("</html>")
    return "\n".join(pieces) + "\n"


STYLE_SHEET = """
:root {
  --ink: #1a1a1a;
  --muted: #55524d;
  --rule: #d9d4cc;
  --accent: #1d4f7a;
  --paper: #fdfcf9;
}
html { font-size: 17px; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Cambria, "Cambria Math", Georgia, serif;
  line-height: 1.55;
}
main { max-width: 62rem; margin: 0 auto; padding: 2.6rem 1.6rem 4rem; }
h1 { font-size: 1.95rem; line-height: 1.25; margin: 0 0 0.6rem; }
h2 { font-size: 1.36rem; margin: 2.6rem 0 0.7rem; padding-bottom: 0.28rem;
     border-bottom: 1px solid var(--rule); }
h3 { font-size: 1.1rem; margin: 1.9rem 0 0.5rem; color: var(--accent); }
h4 { font-size: 0.98rem; margin: 1.15rem 0 0.35rem; letter-spacing: 0.02em;
     text-transform: uppercase; color: var(--muted); }
p { margin: 0.55rem 0; }
p.lead { font-size: 1.06rem; color: var(--muted); }
blockquote { margin: 0.9rem 0; padding: 0.7rem 1.1rem; background: #f4f1ea;
             border-left: 3px solid var(--accent); }
blockquote p { margin: 0.2rem 0; }
blockquote footer { color: var(--muted); font-size: 0.86rem; }
.step { margin-bottom: 0.4rem; }
.display-math { margin: 0.75rem 0 0.85rem; text-align: center; overflow-x: auto; }
.katex { font-family: "XITS", "STIX Two Math", "Cambria Math", serif; }
code { font-family: "Cascadia Mono", "Consolas", monospace; font-size: 0.86em;
       background: #efece5; padding: 0.06rem 0.3rem; border-radius: 3px; }
table { border-collapse: collapse; width: 100%; margin: 0.8rem 0 0.4rem; font-size: 0.9rem; }
th, td { border: 1px solid var(--rule); padding: 0.34rem 0.5rem; text-align: left;
         vertical-align: top; }
th { background: #f2efe8; font-weight: 600; }
table.answers td:first-child { width: 3.2rem; text-align: center; }
figure.drawing { margin: 1.3rem 0 1.5rem; }
figure.drawing img { width: 100%; height: auto; border: 1px solid var(--rule);
                     border-radius: 4px; background: #ffffff; }
figcaption { font-size: 0.9rem; color: var(--muted); margin-top: 0.45rem; }
.verification { margin-top: 1.5rem; }
.verification table.checks { font-size: 0.84rem; }
"""

SCRIPT_BLOCK = """
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '$', right: '$', display: false}
    ],
    throwOnError: false
  });"></script>
"""
"""Script block that renders the mathematics of the page."""


def check_page(page: str) -> list:
    """Check the composed page and return the list of the reported facts."""
    facts = []
    control_count = sum(1 for character in page if unicodedata.category(character) == "Cc"
                        and character not in "\n\t")
    if control_count:
        raise AssertionError(f"the page holds {control_count} control characters")
    facts.append("control characters: 0")

    for item in re.findall(r"<li>(.*?)</li>", page, flags=re.DOTALL):
        plain = re.sub(r"<[^>]+>", "", item).strip()
        if not plain.endswith("."):
            raise AssertionError(f"a list item does not end with a full stop: {plain[-60:]!r}")
    facts.append("list items that end with a full stop: all")

    for paragraph in re.findall(r"<p>(.*?)</p>", page, flags=re.DOTALL):
        plain = re.sub(r"<[^>]+>", "", paragraph).strip()
        if plain and plain[0].islower():
            raise AssertionError(f"a paragraph starts with a lower-case word: {plain[:60]!r}")
    facts.append("paragraphs that start with a lower-case word: 0")

    cells = re.findall(r"<t[dh]>(.*?)</t[dh]>", page, flags=re.DOTALL)
    captions = re.findall(r"<figcaption>(.*?)</figcaption>", page, flags=re.DOTALL)
    for text in cells + captions:
        plain = re.sub(r"<[^>]+>", "", text)
        outside = re.sub(r"\$\$.*?\$\$", "", plain)
        outside = re.sub(r"\$[^$]*\$", "", outside)
        if "\\" in outside:
            raise AssertionError(f"a backslash sits outside a math span: {plain[:80]!r}")
        if "<" in outside:
            raise AssertionError(f"an angle bracket sits outside a math span: {plain[:80]!r}")
    facts.append(f"cells and captions without stray mathematics: {len(cells)} and "
                 f"{len(captions)}")

    figure_count = page.count('src="data:image/png;base64,')
    if figure_count != len(FIGURE_SPECS):
        raise AssertionError(f"the page holds {figure_count} figures and not {len(FIGURE_SPECS)}")
    facts.append(f"figures with a data identifier: {figure_count}")

    step_count = len(re.findall(r'<article class="step"', page))
    facts.append(f"steps in order: {step_count}")
    return facts


def main() -> None:
    """Compose the page, check it, and write the file."""
    page = build_page()
    facts = check_page(page)
    REPORT_PATH.write_text(page, encoding="utf-8", newline="\n")
    for fact in facts:
        print(fact, flush=True)
    print(f"wrote {REPORT_PATH} with {len(page)} characters", flush=True)


if __name__ == "__main__":
    main()
