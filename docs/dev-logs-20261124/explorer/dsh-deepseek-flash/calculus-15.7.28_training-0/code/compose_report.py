"""Compose the tutorial page from the step files, the figures, and the records of the checks.

The page needs no other file: each figure enters the page as a Base64 data uniform resource
identifier.  The script also checks the page before it writes the page: every LaTeX control word
must stay whole, every math delimiter must have a partner, and every step file and every figure
must reach the page.
"""

import base64
import html
import json
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

STEPS_DIRECTORY = WORKSPACE / "steps"
"""Directory of the step files."""

FIGURE_DIRECTORY = WORKSPACE / "code" / "figures"
"""Directory of the drawn figures."""

RESULT_DIRECTORY = WORKSPACE / "code" / "results"
"""Directory of the records of the checks."""

OUTPUT_FILES = (WORKSPACE / "report.html", WORKSPACE / "tutorial.html")
"""The two names of the composed page.  The two files hold the same bytes."""

KATEX_HEAD = (
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">\n'
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>\n'
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/'
    'auto-render.min.js"></script>\n'
)
"""The style sheet and the scripts of KaTeX, at the version of the pass."""

KATEX_START = """
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
"""The call that renders every math expression after the document is ready."""

STYLE = """
:root {
  --ink: #1d2530;
  --muted: #5b6675;
  --rule: #d3dae2;
  --paper: #fbfcfd;
  --accent: #1f4e79;
  --accent-soft: #eaf1f7;
  --check: #f4f7fa;
}
body {
  margin: 0 auto;
  max-width: 60rem;
  padding: 3rem 1.6rem 6rem;
  background: var(--paper);
  color: var(--ink);
  font-family: Cambria, "Cambria Math", Georgia, serif;
  font-size: 17px;
  line-height: 1.62;
}
h1, h2, h3, h4 {
  font-family: Cambria, Georgia, serif;
  color: var(--accent);
  line-height: 1.25;
}
h1 { font-size: 2.0rem; margin: 0 0 0.4rem; }
h2 { font-size: 1.5rem; margin: 3.0rem 0 0.8rem; border-bottom: 2px solid var(--rule);
     padding-bottom: 0.35rem; }
h3 { font-size: 1.24rem; margin: 2.2rem 0 0.5rem; }
h4 { font-size: 1.06rem; margin: 1.6rem 0 0.4rem; }
p { margin: 0.75rem 0; }
.subtitle { color: var(--muted); font-size: 1.02rem; margin-bottom: 2.2rem; }
.quote {
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  padding: 0.9rem 1.2rem;
  margin: 1.2rem 0;
}
.statement { background: #fff; border: 1px solid var(--rule); padding: 1.2rem 1.4rem;
             border-radius: 6px; }
table { border-collapse: collapse; width: 100%; margin: 1.1rem 0; font-size: 0.95rem; }
th, td { border: 1px solid var(--rule); padding: 0.45rem 0.65rem; text-align: left;
         vertical-align: top; }
th { background: var(--accent-soft); color: var(--accent); font-weight: 600; }
tbody tr:nth-child(even) { background: #fff; }
tbody tr:nth-child(odd) { background: var(--check); }
code, pre { font-family: "Cascadia Mono", Consolas, monospace; font-size: 0.9rem; }
code { background: #eef2f6; padding: 0.08rem 0.32rem; border-radius: 3px; }
figure { margin: 1.8rem 0; text-align: center; }
figure img { max-width: 100%; border: 1px solid var(--rule); border-radius: 6px;
             background: #fff; }
figcaption { color: var(--muted); font-size: 0.92rem; margin-top: 0.5rem; text-align: left; }
.answer {
  border: 2px solid var(--accent);
  border-radius: 6px;
  background: #fff;
  padding: 0.9rem 1.2rem;
  margin: 1.4rem 0 2.2rem;
}
.answer .label { color: var(--accent); font-weight: 600; letter-spacing: 0.02em;
                 font-size: 0.92rem; text-transform: uppercase; }
.math-block { overflow-x: auto; margin: 1.1rem 0; }
.katex, .math-block, .math-inline { font-family: "XITS Math", "XITS", serif; }
.scope-note { color: var(--muted); font-size: 0.92rem; }
ol, ul { margin: 0.7rem 0 0.7rem 1.4rem; }
li { margin: 0.35rem 0; }
"""


def escape_html(text):
    """Escape the characters of HTML in a text and keep every other character.

    Args:
        text: The text to escape.

    Returns:
        The escaped text.
    """
    return html.escape(text, quote=False)


def render_inline(text):
    """Render the inline parts of one line of Markdown.

    The function handles an inline code span and a bold span.  A math expression passes through
    without a change, because the renderer of the page reads it later.

    Args:
        text: One line of Markdown, already escaped.

    Returns:
        The line as HTML.
    """
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
    return rendered


def render_table(lines):
    """Render a Markdown table.

    Args:
        lines: The lines of the table, with the header row and the separator row first.

    Returns:
        The table as HTML.
    """
    rows = []
    for index, line in enumerate(lines):
        if index == 1:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    head = "".join(f"<th>{render_inline(cell)}</th>" for cell in rows[0])
    body = "".join(
        "<tr>" + "".join(f"<td>{render_inline(cell)}</td>" for cell in row) + "</tr>"
        for row in rows[1:]
    )
    return f"<table>\n<thead><tr>{head}</tr></thead>\n<tbody>{body}</tbody>\n</table>\n"


def render_markdown(source):
    """Render the subset of Markdown that the step files use.

    The function handles a heading, a display math block, a table, a list, and a paragraph.

    Args:
        source: The text of one step file.

    Returns:
        The text as HTML.
    """
    lines = escape_html(source).split("\n")
    output = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped == "$$":
            collected = []
            index += 1
            while index < len(lines) and lines[index].strip() != "$$":
                collected.append(lines[index])
                index += 1
            index += 1
            output.append('<div class="math-block">$$' + "\n".join(collected) + "$$</div>")
            continue
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            level = min(len(heading.group(1)) + 2, 6)
            output.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            index += 1
            continue
        if stripped.startswith("|"):
            collected = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                collected.append(lines[index])
                index += 1
            output.append(render_table(collected))
            continue
        if re.match(r"^(-|\d+\.)\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            items = []
            while index < len(lines) and re.match(r"^(-|\d+\.)\s+", lines[index].strip()):
                item = re.sub(r"^(-|\d+\.)\s+", "", lines[index].strip())
                items.append(f"<li>{render_inline(item)}</li>")
                index += 1
            output.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        collected = []
        while index < len(lines) and lines[index].strip() and not lines[index].strip().startswith(
            ("#", "|", "$$")
        ) and not re.match(r"^(-|\d+\.)\s+", lines[index].strip()):
            collected.append(render_inline(lines[index].strip()))
            index += 1
        output.append("<p>" + " ".join(collected) + "</p>")
    return "\n".join(output)


def figure_data_uri(name):
    """Return the Base64 data uniform resource identifier of one figure.

    Args:
        name: The file name of the figure without a suffix.

    Returns:
        The data uniform resource identifier as a text.
    """
    path = FIGURE_DIRECTORY / f"{name}.png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def figure_block(name, caption):
    """Build the element of one figure with its caption.

    Args:
        name: The file name of the figure without a suffix.
        caption: The text of the caption.

    Returns:
        The element as HTML.
    """
    return (
        f'<figure><img alt="{name}" src="{figure_data_uri(name)}">'
        f"<figcaption>{caption}</figcaption></figure>\n"
    )


def load_record(name):
    """Read one record of the checks.

    Args:
        name: The name of the part, as part1.

    Returns:
        The record as a dictionary.
    """
    return json.loads((RESULT_DIRECTORY / f"{name}_results.json").read_text(encoding="utf-8"))


def part1_tables(record):
    """Build the table of the checked values of part 1.

    Args:
        record: The record of part 1.

    Returns:
        The table as HTML.
    """
    extent = record["extent"]
    volume = record["volume"]
    rows = [
        ("largest value of $x$", f"{extent['analytic']['x']:.6g}", f"{extent['grid']['x']:.6g}"),
        ("largest value of $y$", f"{extent['analytic']['y']:.6g}", f"{extent['grid']['y']:.6g}"),
        ("largest value of $z$", f"{extent['analytic']['z']:.6g}", f"{extent['grid']['z']:.6g}"),
        (
            "disagreements of the nested form and the flat form",
            f"{record['nested_against_flat']}",
            "0",
        ),
        (
            "disagreements of the nested form and the solved form",
            f"{record['nested_against_solved']}",
            "0",
        ),
        (
            "disagreements of the nested form and the misreading",
            f"{record['nested_against_misread']}",
            "more than 0",
        ),
        (
            "volume in the order $x$, $z$, $y$",
            f"{volume['given_order']:.12f}",
            f"{volume['exact_text']} = {volume['exact_value']:.12f}",
        ),
        (
            "volume in the order $z$, $x$, $y$",
            f"{volume['swapped_inner_order']:.12f}",
            f"{volume['given_order']:.12f}",
        ),
        (
            "volume in the order $x$, $y$, $z$",
            f"{volume['order_x_y_z']:.12f}",
            f"{volume['given_order']:.12f}",
        ),
        ("largest gap of the three volumes", f"{volume['largest_gap']:.3e}", "0"),
    ]
    head = "<tr><th>Quantity</th><th>Computed value</th><th>Expected value</th></tr>"
    body = "".join(
        f"<tr><td>{first}</td><td>{second}</td><td>{third}</td></tr>"
        for first, second, third in rows
    )
    return f"<table><thead>{head}</thead><tbody>{body}</tbody></table>\n"


def part2_tables(record):
    """Build the table of the checked values of part 2.

    Args:
        record: The record of part 2.

    Returns:
        The table as HTML.
    """
    head = (
        "<tr><th>Height $y$</th><th>Shape</th><th>Sides</th><th>Area from the product</th>"
        "<th>Area from the sample</th><th>Relative gap</th><th>Corners</th>"
        "<th>Area of the misreading</th></tr>"
    )
    body = ""
    for row in record["rows"]:
        body += (
            f"<tr><td>{row['height']:g}</td><td>{row['shape']}</td>"
            f"<td>${row['length_x']:g} \\times {row['length_z']:g}$</td>"
            f"<td>{row['area_product']:.6f}</td><td>{row['area_sampled']:.6f}</td>"
            f"<td>{row['relative_gap']:.3e}</td><td>{row['corner_count']}</td>"
            f"<td>{row['area_of_misread_cut']:.6f}</td></tr>"
        )
    return f"<table><thead>{head}</thead><tbody>{body}</tbody></table>\n"


def part3_tables(record):
    """Build the tables of the checked values of part 3.

    Args:
        record: The record of part 3.

    Returns:
        The tables as HTML.
    """
    surface_head = (
        "<tr><th>Patch</th><th>Equation</th><th>Largest residual</th>"
        "<th>Every point inside</th><th>Outward step leaves</th><th>Inward step stays</th>"
        "<th>Area</th></tr>"
    )
    surface_body = ""
    for item in record["surfaces"]:
        surface_body += (
            f"<tr><td>${item['name'][0]}_{{{item['name'][1:]}}}$</td>"
            f"<td>${item['equation']}$</td>"
            f"<td>{item['largest_residual']:.3e}</td>"
            f"<td>{'yes' if item['all_inside'] else 'no'}</td>"
            f"<td>{'yes' if item['outward_step_outside'] else 'no'}</td>"
            f"<td>{'yes' if item['inward_step_inside'] else 'no'}</td>"
            f"<td>{item['area']:.6f}</td></tr>"
        )
    corner_head = (
        "<tr><th>Corner</th><th>Point</th><th>Patches that hold the point</th></tr>"
    )
    corner_body = ""
    for name, item in record["corners"].items():
        coordinates = ", ".join(f"{value:g}" for value in item["point"])
        corner_body += (
            f"<tr><td>${name}$</td><td>$({coordinates})$</td>"
            f"<td>{item['surface_count']}</td></tr>"
        )
    edge_head = (
        "<tr><th>Edge</th><th>Equations</th><th>Largest residual on its two patches</th>"
        "<th>Smallest residual on the other three</th><th>Arc length</th>"
        "<th>Chord length</th></tr>"
    )
    edge_body = ""
    for item in record["edges"]:
        equations = ", ".join(
            f"${piece}$" for piece in item["description"].split(" and ")
        )
        label = f"$e_{{{item['name'][1:]}}}$"
        edge_body += (
            f"<tr><td>{label} from ${item['from']}$ to ${item['to']}$</td>"
            f"<td>{equations}</td>"
            f"<td>{item['largest_residual']:.3e}</td><td>{item['residual_other']:.6f}</td>"
            f"<td>{item['arc_length']:.6f}</td><td>{item['chord_length']:.6f}</td></tr>"
        )
    return (
        "<h4>The five patches</h4>\n"
        f"<table><thead>{surface_head}</thead><tbody>{surface_body}</tbody></table>\n"
        "<h4>The five corners</h4>\n"
        f"<table><thead>{corner_head}</thead><tbody>{corner_body}</tbody></table>\n"
        "<h4>The eight edges</h4>\n"
        f"<table><thead>{edge_head}</thead><tbody>{edge_body}</tbody></table>\n"
    )


def part4_tables(record, exact_volume, exact_text):
    """Build the tables of the checked values of part 4.

    Args:
        record: The record of part 4.
        exact_volume: The exact volume as a number of the record of part 1.
        exact_text: The exact volume as a text of the record of part 1.

    Returns:
        The tables as HTML.
    """
    volume = record["volume"]
    volume_rows = (
        f"<tr><td>The divergence theorem on the closed mesh</td>"
        f"<td>{volume['mesh']:.12f}</td><td>{volume['slices']:.12f}</td>"
        f"<td>{volume['relative_gap']:.3e}</td></tr>"
        f"<tr><td>The iterated integral of the exercise</td>"
        f"<td>{volume['iterated_integral']:.12f}</td>"
        f"<td>${exact_text}$ = {exact_volume:.12f}</td>"
        f"<td>{abs(volume['iterated_integral'] - exact_volume) / exact_volume:.3e}</td></tr>"
    )
    area_rows = ""
    for item in record["areas"]:
        area_rows += (
            f"<tr><td>${item['equation']}$</td><td>{item['mesh_area']:.6f}</td>"
            f"<td>{item['integral_area']:.6f}</td><td>{item['relative_gap']:.3e}</td></tr>"
        )
    cut_rows = ""
    for item in record["cuts"]:
        cut_rows += (
            f"<tr><td>{item['height']:g}</td><td>{item['drawn_area']:.6f}</td>"
            f"<td>{item['area_from_limits']:.6f}</td><td>{item['relative_gap']:.3e}</td></tr>"
        )
    label_rows = ""
    for item in record["labels"]:
        coordinates = ", ".join(f"{value:g}" for value in item["point"])
        label_rows += (
            f"<tr><td>${item['equation']}$</td><td>$({coordinates})$</td>"
            f"<td>{item['residual_on_own_surface']:.3e}</td>"
            f"<td>{item['nearest_other_surface']:.3f}</td>"
            f"<td>{'yes' if item['inside_region'] else 'no'}</td></tr>"
        )
    projection = record["projection"]
    return (
        "<h4>The mesh and the volume</h4>\n"
        f'<p class="scope-note">The number of triangles is {record["triangle_count"]}, the '
        f"subdivision is {record['subdivision']}, and the count of the edges that belong to one "
        f"triangle is {record['boundary_edge_count']}.</p>\n"
        "<table><thead><tr><th>Method</th><th>Computed value</th><th>Compared value</th>"
        f"<th>Relative gap</th></tr></thead><tbody>{volume_rows}</tbody></table>\n"
        "<h4>The area of each patch</h4>\n"
        "<table><thead><tr><th>Patch</th><th>Area of the mesh</th><th>Area of the integral</th>"
        f"<th>Relative gap</th></tr></thead><tbody>{area_rows}</tbody></table>\n"
        "<h4>The cut of the drawn mesh</h4>\n"
        "<table><thead><tr><th>Height</th><th>Area measured on the mesh</th>"
        f"<th>Area from the limits</th><th>Relative gap</th></tr></thead>"
        f"<tbody>{cut_rows}</tbody></table>\n"
        "<h4>The projection on the plane $x = 0$</h4>\n"
        "<table><thead><tr><th>Quantity</th><th>Computed value</th></tr></thead><tbody>"
        f"<tr><td>Fraction of the rectangle that reaches the solid</td>"
        f"<td>{projection['covered_fraction']:.6f}</td></tr>"
        f"<tr><td>Area of the rectangle outside the disk of radius $2$</td>"
        f"<td>{projection['area_outside_disk']:.6f}</td></tr>"
        f"<tr><td>Number of sample points</td><td>{projection['sample_count']}</td></tr>"
        "</tbody></table>\n"
        "<h4>The label points</h4>\n"
        "<table><thead><tr><th>Patch</th><th>Point</th><th>Residual on its own equation</th>"
        f"<th>Smallest residual on the other four</th><th>Inside the solid</th></tr></thead>"
        f"<tbody>{label_rows}</tbody></table>\n"
    )


def check_page(page):
    """Stop the script when the composed page holds a fault.

    Args:
        page: The text of the composed page.

    Raises:
        AssertionError: The page holds a split control word or an unpaired math delimiter.
    """
    probe = page.replace("\\ ", "__thin_space__")
    split_word = re.search(r"\\\s", probe)
    assert split_word is None, (
        "a LaTeX control word is broken by a space at: "
        f"{probe[max(0, split_word.start() - 40):split_word.start() + 10]}"
    )
    assert page.count("$") % 2 == 0, "the count of the math delimiters is odd"
    assert page.count("$$") % 2 == 0, "the count of the display math delimiters is odd"
    assert page.count("data:image/png;base64,") == 5, "a figure did not reach the page"
    for span in re.findall(r"\$\$(.+?)\$\$", page, flags=re.S):
        assert span.count("{") == span.count("}"), f"unbalanced braces in: {span[:80]}"
    for span in re.findall(r"(?<!\$)\$([^$]+)\$(?!\$)", page):
        assert span.count("{") == span.count("}"), f"unbalanced braces in: {span[:80]}"
        assert not span.rstrip().endswith("\\"), f"a control word ends the span: {span[:80]}"
    for part, step in (
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (4, 1),
        (4, 2),
    ):
        marker = f"part {part}, step {step}:"
        assert marker in page.lower(), f"the title of Part {part}, Step {step} is absent"


def build_page():
    """Build the text of the composed page.

    Returns:
        The page as a text.
    """
    records = {name: load_record(name) for name in ("part1", "part2", "part3", "part4")}
    steps = {
        name: render_markdown((STEPS_DIRECTORY / f"{name}.md").read_text(encoding="utf-8"))
        for name in (
            "part1_step1",
            "part1_step2",
            "part2_step1",
            "part2_step2",
            "part3_step1",
            "part3_step2",
            "part4_step1",
            "part4_step2",
        )
    }
    figure1 = figure_block(
        "part1_figure1",
        "Figure 1. The two laws that bound the solid in the two vertical planes. Left: the cut by "
        "the plane $z = 0$ is the region $0 \\le x \\le 4 - y^{2}$ under the parabola. Right: the "
        "cut by the plane $x = 0$ is the triangle $0 \\le z \\le 2 - y$. The corner $T$ is the top "
        "of the solid in both panels.",
    )
    figure2 = figure_block(
        "part2_figure1",
        "Figure 2. The horizontal cut at the heights $0$, $0.5$, $1$, $1.5$, and $2$. Each cut is "
        "a rectangle, and each rectangle holds the next one. At $y = 2$ the cut is the single "
        "point $T$, and its area is $0$. The areas are the values of "
        "$A(y) = (4 - y^{2})(2 - y)$.",
    )
    figure3 = figure_block(
        "part3_figure1",
        "Figure 3. The five patches of the boundary, one panel for each patch, with the corners "
        "of each patch. Each corner carries the letter of the corner table. The last panel gives "
        "the coordinates of the corners.",
    )
    figure4 = figure_block(
        "part4_figure1",
        "Figure 4. The assembled solid. The four far patches have an opacity above one half, so "
        "the body reads as a closed body. Each label stands at a point of the patch that it "
        "names. The patch $y = 0$ is the far face in this point of view, so its label is absent "
        "and Figure 3 shows it alone.",
    )
    figure5 = figure_block(
        "part4_figure2",
        "Figure 5. The three projections of the solid. The middle panel is the projection on the "
        "plane $y = 0$, with the dashed disk $x^{2} + z^{2} \\le 4$ for contrast. The projection "
        "is the rectangle of area $8$, and the disk is not the projection.",
    )

    parts = []
    parts.append(
        "<h1>Sketch the solid of an iterated integral</h1>\n"
        '<p class="subtitle">Calculus: Early Transcendentals, Section 15.7, Exercise 28. '
        "A verified tutorial: every number on this page comes from a script that prints the "
        "computed value and the expected value.</p>\n"
        '<div class="statement">\n'
        "<h2 style=\"margin-top:0\">The problem</h2>\n"
        '<div class="quote">Sketch the solid whose volume is given by the iterated integral.</div>\n'
        '<div class="math-block">$$\\int_{0}^{2}\\int_{0}^{\\,2-y}\\int_{0}^{\\,4-y^{2}} '
        "dx\\,dz\\,dy$$</div>\n"
        "<p>The integral holds three pairs of limits, the order $dx\\,dz\\,dy$, and the integrand "
        "$1$. These data are the only data of the problem. The problem asks for one product: a "
        "sketch of the solid. It asks for no number and no evaluation of the integral.</p>\n"
        "</div>\n"
    )

    parts.append(
        "<h2>Part 1. Read the limits as a region of space</h2>\n"
        "<p>The first part turns the three pairs of limits into a set of points. The set is the "
        "solid that the sketch must show.</p>\n"
        + steps["part1_step1"]
        + "\n"
        + figure1
        + "\n"
        + steps["part1_step2"]
        + "\n"
        + '<div class="answer"><span class="label">Final answer of Part 1</span>\n'
        "<p>The solid is $R = \\{(x,y,z) : 0 \\le y \\le 2,\\ 0 \\le z \\le 2-y,\\ "
        "0 \\le x \\le 4-y^{2}\\}$. It lies in the box $[0,4] \\times [0,2] \\times [0,2]$, and "
        "it touches all six faces of that box.</p></div>\n"
        "<h3>The checked values of Part 1</h3>\n" + part1_tables(records["part1"])
    )

    parts.append(
        "<h2>Part 2. Cut the solid at a fixed height</h2>\n"
        "<p>The second part reads the shape of one horizontal cut. The cut is the object that the "
        "reader of a sketch must recognize first.</p>\n"
        + steps["part2_step1"]
        + "\n"
        + figure2
        + "\n"
        + steps["part2_step2"]
        + "\n"
        + '<div class="answer"><span class="label">Final answer of Part 2</span>\n'
        "<p>At the height $y$ the cut is the rectangle $[0, 4-y^{2}] \\times [0, 2-y]$ with area "
        "$A(y) = (4-y^{2})(2-y)$. The areas at $y = 0, 0.5, 1, 1.5, 2$ are $8$, $5.625$, $3$, "
        "$0.875$, and $0$. The cut at $y = 2$ is the single point $T = (0,2,0)$.</p></div>\n"
        "<h3>The checked values of Part 2</h3>\n" + part2_tables(records["part2"])
    )

    parts.append(
        "<h2>Part 3. Name the patches, the corners, and the edges</h2>\n"
        "<p>The third part gives the boundary of the solid a name for each piece, so that the "
        "drawing and the reader can point at the same piece.</p>\n"
        + steps["part3_step1"]
        + "\n"
        + figure3
        + "\n"
        + steps["part3_step2"]
        + "\n"
        + '<div class="answer"><span class="label">Final answer of Part 3</span>\n'
        "<p>The boundary is the union of five patches: $y = 0$, $x = 0$, $z = 0$, $y + z = 2$, and "
        "$x = 4-y^{2}$. It has five corners $A$, $B$, $C$, $D$, $T$ and eight edges. Every edge "
        "lies on two patches, so the boundary is closed.</p></div>\n"
        "<h3>The checked values of Part 3</h3>\n" + part3_tables(records["part3"])
    )

    parts.append(
        "<h2>Part 4. Draw the solid and check the drawing</h2>\n"
        "<p>The fourth part draws the solid under fixed rules, and then measures the drawing "
        "against the limits.</p>\n"
        + steps["part4_step1"]
        + "\n"
        + steps["part4_step2"]
        + "\n"
        + figure4
        + "\n"
        + figure5
        + "\n"
        + '<div class="answer"><span class="label">Final answer of Part 4 and of the '
        "exercise</span>\n"
        "<p>The answer to the exercise is the sketch of the solid: the body inside the box "
        "$[0,4] \\times [0,2] \\times [0,2]$, closed by the five patches $y = 0$, $x = 0$, "
        "$z = 0$, $y + z = 2$, and $x = 4-y^{2}$, with the corners $A$, $B$, $C$, $D$, $T$ and a "
        "rectangular cut at every height below $y = 2$. The problem asks for this sketch and for "
        "no number.</p></div>\n"
        "<h3>The checked values of Part 4</h3>\n"
        + part4_tables(
            records["part4"],
            records["part1"]["volume"]["exact_value"],
            records["part1"]["volume"]["exact_text"],
        )
    )

    parts.append(
        "<h2>What the checks can and cannot tell</h2>\n"
        "<p>Part 4 measures a volume of the drawn mesh and compares it with the volume of the "
        "cuts. This comparison does not detect a misreading of the limits, because the misreading "
        "<span>$0 \\le x \\le 4 - z^{2}$</span> gives the same volume in this problem. The "
        "comparison that detects the misreading is the comparison of the shapes: the cut is a "
        "rectangle and not a disk, and the projection is the rectangle of area $8$ and not the "
        "disk of area $2\\pi$. Part 2 and Part 4 give that comparison, and both of them can "
        "fail.</p>\n"
    )

    body = "\n".join(parts)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>The solid of an iterated integral: a verified tutorial</title>\n"
        + KATEX_HEAD
        + "<style>"
        + STYLE
        + "</style>\n</head>\n<body>\n"
        + body
        + "\n<script>"
        + KATEX_START
        + "</script>\n</body>\n</html>\n"
    )


def main():
    """Compose the page, check it, and write the two copies."""
    page = build_page()
    check_page(page)
    for path in OUTPUT_FILES:
        path.write_text(page, encoding="utf-8")
        print(f"page written to {path}")
    print(f"page size: {len(page)} bytes")


if __name__ == "__main__":
    main()
