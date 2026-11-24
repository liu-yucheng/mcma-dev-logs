"""Compose `report.html` and `tutorial.html` from the step files, the figures, and the results.

The composer reads one Markdown file for each step, one PNG file for each figure, and one JSON
record for each verified part. It writes one self-contained page: every figure enters the page as
a Base64 data uniform resource identifier, and KaTeX renders every LaTeX expression in the
browser. The composer then asserts five properties of its own output, so a broken page fails here
instead of reaching a reader.
"""

from __future__ import annotations

import base64
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
"""The problem workspace, which holds the steps, the code, and the product page."""

STEP_DIRECTORY = ROOT / "steps"
"""Directory of the Markdown files of the steps."""

RESULT_DIRECTORY = ROOT / "code" / "results"
"""Directory of the machine-readable record of each verified part."""

FIGURE_DIRECTORY = ROOT / "code" / "figures"
"""Directory of the PNG files of the figures."""

OUTPUT_PATHS = (ROOT / "report.html", ROOT / "tutorial.html")
"""The two names of the composed page, with the same content."""

KATEX_BASE = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/"
"""The base address of the KaTeX style sheet, script, and automatic-render script."""

FIGURES = {
    "part1_step2": (
        "part1_figure1.png",
        "Figure 1. The solid E and the section at x = 0.6. The left panel draws the four boundary "
        "surfaces and labels each one at a point that satisfies its own equation. The right panel "
        "draws the section, which is the triangle with 0 <= z <= y <= Y, with Y = 0.8 and area 0.3200.",
    ),
    "part4_step1": (
        "part4_figure1.png",
        "Figure 2. The eight monomial integrals of I_z. Each bar is one integral, and its label is "
        "the exact value of the same integral. The dashed line marks the sum of the eight values.",
    ),
}
"""The figure of each part: the file name, and the caption of the figure."""

CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
"""A character class that no composed page may contain."""

STATEMENT_HTML = r"""
<p>
Let $E$ be the solid in the first octant bounded by the cylinder $x^2+y^2=1$ and the planes
$y=z$, $x=0$, and $z=0$ with the density function $\rho(x,y,z)=1+x+y+z$. Use a computer algebra
system to find the exact values of the following quantities for $E$.
</p>
<ol class="statement">
<li>The mass $m$.</li>
<li>The center of mass $(\bar{x},\bar{y},\bar{z})$.</li>
<li>The moment of inertia $I_z$ about the $z$ axis.</li>
</ol>
"""
"""The statement of the problem, with the three quantities named by their symbols."""


def render_inline(text: str) -> str:
    """Render the inline markup of one line and return HTML.

    The only two inline constructs are a code span in backticks and a strong span in double
    asterisks. Every other character reaches the page unchanged, because a step file never holds
    a character that HTML reserves.
    """
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
    return rendered


def render_markdown(text: str) -> str:
    """Render the small Markdown subset of a step file and return HTML.

    A heading starts with a single number sign. A displayed expression stands on its own line
    between two double dollar signs. A list item starts with a hyphen and a space, and an
    indented line continues the item above it. Any other non-empty block is one paragraph.
    """
    lines: list[str] = []
    for raw_line in text.split("\n"):
        if raw_line.startswith("  ") and lines and lines[-1].startswith(("- ", "  ")):
            lines[-1] = lines[-1] + " " + raw_line.strip()
        else:
            lines.append(raw_line.rstrip())

    blocks: list[str] = []
    paragraph: list[str] = []
    items: list[str] = []

    def flush_paragraph() -> None:
        """Write the collected paragraph as one paragraph element."""
        if paragraph:
            blocks.append("<p>" + render_inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    def flush_items() -> None:
        """Write the collected list items as one list element."""
        if items:
            blocks.append("<ul>" + "".join(f"<li>{render_inline(item)}</li>" for item in items) + "</ul>")
            items.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_items()
        elif stripped.startswith("# "):
            flush_paragraph()
            flush_items()
            blocks.append(f"<h3>{render_inline(stripped[2:])}</h3>")
        elif stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            flush_paragraph()
            flush_items()
            blocks.append(f'<div class="display">{stripped}</div>')
        elif stripped.startswith("- "):
            flush_paragraph()
            items.append(stripped[2:])
        else:
            paragraph.append(stripped)
    flush_paragraph()
    flush_items()
    return "\n".join(blocks)


def load_part(part_number: int) -> dict[str, object]:
    """Return the machine-readable record of one part."""
    path = RESULT_DIRECTORY / f"part{part_number}_results.json"
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def step_files(part_number: int) -> list[pathlib.Path]:
    """Return the step files of one part in their numeric order."""
    pattern = f"part{part_number}_step*.md"
    return sorted(STEP_DIRECTORY.glob(pattern), key=lambda path: int(path.stem.split("_step")[1]))


def format_value(value: object) -> str:
    """Return one number with twelve significant digits, or the text of a non-number."""
    if isinstance(value, (int, float)):
        return f"{float(value):.12g}"
    return str(value)


def render_checks(record: dict[str, object]) -> str:
    """Return the table of the checks of one part, with its bounds when it has any."""
    rows = []
    for check in record["checks"]:
        rows.append(
            "<tr>"
            f"<td>{render_inline(str(check['label']))}</td>"
            f"<td class=\"number\">{format_value(check['computed'])}</td>"
            f"<td class=\"number\">{format_value(check['expected'])}</td>"
            f"<td class=\"number\">{float(check['difference']):.3e}</td>"
            f"<td class=\"number\">{float(check['tolerance']):.3e}</td>"
            "</tr>"
        )
    html = [
        '<table class="checks">',
        "<caption>Checked values of this part. Each computed value comes from one method and "
        "each expected value comes from a different method.</caption>",
        "<thead><tr><th>check</th><th>computed</th><th>expected</th><th>difference</th>"
        "<th>tolerance</th></tr></thead>",
        "<tbody>" + "".join(rows) + "</tbody>",
        "</table>",
    ]
    bounds = record.get("bounds", [])
    if bounds:
        items = []
        for bound in bounds:
            items.append(
                "<li>"
                + render_inline(str(bound["label"]))
                + f": {format_value(bound['computed'])} and {format_value(bound['expected'])}"
                + f", gap {float(bound['difference']):.3e}."
                + "</li>"
            )
        html.append("<ul>" + "".join(items) + "</ul>")
    return "\n".join(html)


def render_tables(record: dict[str, object]) -> str:
    """Return every extra table of one part."""
    blocks = []
    for table in record.get("tables", []):
        head = "".join(f"<th>{render_inline(str(column))}</th>" for column in table["columns"])
        body = []
        for row in table["rows"]:
            cells = "".join(f"<td>{render_inline(str(cell))}</td>" for cell in row)
            body.append(f"<tr>{cells}</tr>")
        blocks.append(
            '<table class="values">'
            f"<caption>{render_inline(str(table['caption']))}</caption>"
            f"<thead><tr>{head}</tr></thead>"
            f"<tbody>{''.join(body)}</tbody>"
            "</table>"
        )
    return "\n".join(blocks)


def render_figure(step_name: str) -> str:
    """Return one figure as a Base64 data uniform resource identifier with its caption."""
    name, caption = FIGURES[step_name]
    data = base64.b64encode((FIGURE_DIRECTORY / name).read_bytes()).decode("ascii")
    return (
        '<figure><img alt="'
        + caption.replace('"', "'")
        + '" src="data:image/png;base64,'
        + data
        + '"><figcaption>'
        + caption
        + "</figcaption></figure>"
    )


def build_body() -> str:
    """Return the body of the page: the statement, every part, and the summary."""
    sections: list[str] = ["<h2>The statement</h2>", STATEMENT_HTML]
    for part_number in range(1, 5):
        record = load_part(part_number)
        sections.append(f'<section class="part"><h2>Part {part_number}. {record["title"]}</h2>')
        for path in step_files(part_number):
            sections.append(render_markdown(path.read_text(encoding="utf-8")))
            if path.stem in FIGURES:
                sections.append(render_figure(path.stem))
        sections.append('<h3 class="verified">Verified values of Part ' + str(part_number) + "</h3>")
        sections.append(render_tables(record))
        sections.append(render_checks(record))
        sections.append("</section>")

    answers = [
        ("(a) the mass", r"$m=\frac{44+9\pi}{96}\approx 0.752858$", "Part 2"),
        (
            "(b) the center of mass",
            r"$(\bar{x},\bar{y},\bar{z})=\left(\frac{28}{44+9\pi},\ \frac{30\pi+128}{5(44+9\pi)},"
            r"\ \frac{45\pi+208}{15(44+9\pi)}\right)\approx(0.387413,\ 0.615012,\ 0.322264)$",
            "Part 3",
        ),
        ("(c) the moment of inertia", r"$I_z=\frac{17}{60}+\frac{\pi}{16}\approx 0.479683$", "Part 4"),
    ]
    rows = "".join(
        f"<tr><td>{name}</td><td>{value}</td><td>{source}</td></tr>" for name, value, source in answers
    )
    sections.append(
        '<section class="part"><h2>The three answers</h2>'
        '<table class="answers"><caption>Exact values of the three quantities.</caption>'
        "<thead><tr><th>quantity</th><th>exact value</th><th>verified in</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "<p>Every value in this table comes from a script that the page names, and every script "
        "compares its exact value with an independent numerical value.</p></section>"
    )
    return "\n".join(sections)


def compose() -> str:
    """Return the full page."""
    styles = """
:root { --ink: #1c1c1c; --rule: #d8d8d8; --panel: #f6f7f9; }
html { font-size: 17px; }
body { margin: 0 auto; max-width: 60rem; padding: 2rem 1.5rem 4rem; color: var(--ink);
  font-family: Cambria, "Cambria Math", Georgia, serif; line-height: 1.55; }
h1 { font-size: 1.9rem; line-height: 1.25; margin: 0 0 0.4rem; }
h2 { font-size: 1.35rem; margin: 2.4rem 0 0.6rem; padding-bottom: 0.3rem;
  border-bottom: 2px solid var(--rule); }
h3 { font-size: 1.08rem; margin: 1.6rem 0 0.4rem; }
p { margin: 0.55rem 0; }
ul, ol { margin: 0.5rem 0 0.5rem 1.2rem; padding-left: 1rem; }
li { margin: 0.25rem 0; }
.display { margin: 0.8rem 0; padding: 0.5rem 0.8rem; background: var(--panel);
  border-left: 3px solid #4c78a8; overflow-x: auto; }
.katex, .display .katex { font-family: XITS, "XITS Math", Cambria Math, serif; }
code { font-family: Consolas, "Cascadia Mono", monospace; font-size: 0.9em;
  background: #eef0f3; padding: 0.05rem 0.25rem; border-radius: 3px; }
figure { margin: 1.2rem 0; }
figure img { width: 100%; height: auto; border: 1px solid var(--rule); }
figcaption { font-size: 0.88rem; color: #444; margin-top: 0.4rem; }
table { border-collapse: collapse; width: 100%; margin: 0.9rem 0; font-size: 0.9rem; }
caption { caption-side: top; text-align: left; font-size: 0.86rem; color: #444;
  padding-bottom: 0.3rem; }
th, td { border: 1px solid var(--rule); padding: 0.3rem 0.45rem; text-align: left;
  vertical-align: top; }
thead th { background: var(--panel); }
td.number { text-align: right; font-variant-numeric: tabular-nums; }
table.checks { font-size: 0.82rem; }
h3.verified { color: #2f5d8a; }
"""
    scripts = f"""
<link rel="stylesheet" href="{KATEX_BASE}katex.min.css">
<script defer src="{KATEX_BASE}katex.min.js"></script>
<script defer src="{KATEX_BASE}contrib/auto-render.min.js"></script>
<script>
// Render every LaTeX expression after the document is ready, and keep the raw source on failure.
document.addEventListener("DOMContentLoaded", function () {{
  renderMathInElement(document.body, {{
    delimiters: [
      {{left: "$$", right: "$$", display: true}},
      {{left: "$", right: "$", display: false}}
    ],
    throwOnError: false
  }});
}});
</script>
"""
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Mass, center of mass, and moment of inertia of a solid in the first octant</title>\n"
        f"{scripts}<style>{styles}</style>\n</head>\n<body>\n"
        "<h1>Mass, center of mass, and moment of inertia of a solid in the first octant</h1>\n"
        "<p class=\"lede\">A verified tutorial. Each step states its reason before its "
        "computation, and each part names the script that checks every number.</p>\n"
        f"{build_body()}\n</body>\n</html>\n"
    )


def assert_page(page: str) -> None:
    """Assert the five properties that a composed page must hold."""
    control_count = len(CONTROL_CHARACTERS.findall(page))
    print(f"[page] control characters: {control_count}")
    if control_count:
        raise AssertionError(f"The composed page holds {control_count} control characters.")

    empty_code = page.count("<code></code>")
    print(f"[page] empty inline code elements: {empty_code}")
    if empty_code:
        raise AssertionError(f"The composed page holds {empty_code} empty inline code elements.")

    items = re.findall(r"<li>(.*?)</li>", page, flags=re.DOTALL)
    bad_items = [item for item in items if not item.strip().endswith(".")]
    print(f"[page] list items: {len(items)}, list items without a full stop: {len(bad_items)}")
    if bad_items:
        raise AssertionError(f"A list item does not end with a full stop: {bad_items[0]!r}")

    paragraphs = re.findall(r"<p([^>]*)>(.*?)</p>", page, flags=re.DOTALL)
    bad_paragraphs = [
        text for _, text in paragraphs if text.strip()[:1].islower()
    ]
    print(f"[page] paragraphs: {len(paragraphs)}, paragraphs that start in lower case: {len(bad_paragraphs)}")
    if bad_paragraphs:
        raise AssertionError(f"A paragraph starts in lower case: {bad_paragraphs[0][:80]!r}")

    figures = page.count("<figure>")
    print(f"[page] figures: {figures}, size: {len(page)} characters")


def main() -> None:
    """Compose the page, assert its properties, and write both output names."""
    for path in STEP_DIRECTORY.glob("part*_step*.md"):
        text = path.read_text(encoding="utf-8")
        if "<" in text or "&" in text:
            raise AssertionError(f"{path.name} holds a character that HTML reserves.")
    page = compose()
    assert_page(page)
    for output_path in OUTPUT_PATHS:
        output_path.write_text(page, encoding="utf-8", newline="\n")
        print(f"[page] wrote {output_path}")


if __name__ == "__main__":
    main()
