"""Compose the tutorial page of the session from the step files and the check records.

The composer reads one Markdown step file per step, replaces every placeholder with a value
that a verification script printed, inserts every figure as a Base64 data uniform resource
identifier, and asserts the page rules of the session before it writes the page.

Constants:
    WORKSPACE: The product directory, one level above this script.
    STEP_DIRECTORY: The directory of the step files.
    OUTPUT_DIRECTORY: The directory of the JSON records of the checks.
    FIGURE_DIRECTORY: The directory of the PNG files.
    REPORT_PATH: The path of the composed page.
    PART_TITLES: The heading of each part.
    KATEX_HEAD: The style sheet and the script of the mathematics renderer.
    MATH_PATTERN: The pattern of one inline or displayed mathematics span.
"""

import base64
import glob
import json
import os
import re

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP_DIRECTORY = os.path.join(WORKSPACE, "steps")
OUTPUT_DIRECTORY = os.path.join(WORKSPACE, "code", "outputs")
FIGURE_DIRECTORY = os.path.join(WORKSPACE, "code", "figures")
REPORT_PATH = os.path.join(WORKSPACE, "report.html")

PART_TITLES = {
    1: "Part 1. The solid, its volume, and its three projections",
    2: "Part 2. The two orders with $z$ innermost",
    3: "Part 3. The two orders with $y$ innermost",
    4: "Part 4. The two orders with $x$ innermost",
    5: "Part 5. The checks and the six answers",
}

KATEX_HEAD = (
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">\n'
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>\n'
    '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>'
)

MATH_PATTERN = re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$")

STYLE = """
:root { color-scheme: light; }
body { margin: 0 auto; max-width: 52rem; padding: 2.5rem 1.5rem 4rem; background: #fbfaf7;
       color: #1b1b1b; font-family: Cambria, "Times New Roman", serif; font-size: 1.02rem;
       line-height: 1.62; }
header.title { border-bottom: 2px solid #1b1b1b; margin-bottom: 1.6rem; padding-bottom: 0.8rem; }
h1 { font-size: 1.7rem; margin: 0 0 0.3rem; letter-spacing: 0.01em; }
h2 { font-size: 1.28rem; margin: 2.4rem 0 0.6rem; padding-bottom: 0.25rem; border-bottom: 1px solid #c9c4b8; }
h3 { font-size: 1.05rem; margin: 1.8rem 0 0.5rem; color: #2b2b2b; }
p { margin: 0.55rem 0; }
.statement { background: #f2eee4; border-left: 4px solid #8a7c5c; padding: 0.9rem 1.1rem; margin: 1rem 0 1.4rem; }
nav.toc { background: #f6f3ec; border: 1px solid #ded8c9; padding: 0.8rem 1.1rem; margin: 1.2rem 0 2rem; }
nav.toc ol { margin: 0.3rem 0 0 1.1rem; padding: 0; }
nav.toc a { color: #3a4a63; text-decoration: none; }
nav.toc a:hover { text-decoration: underline; }
figure { margin: 1.4rem 0; text-align: center; }
figure img { max-width: 100%; height: auto; border: 1px solid #d8d2c4; background: #ffffff; }
figcaption { font-size: 0.9rem; color: #4a4a4a; margin-top: 0.45rem; text-align: left; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.93rem; }
th, td { border: 1px solid #cfc9ba; padding: 0.32rem 0.5rem; text-align: left; vertical-align: top; }
th { background: #efece3; }
tbody tr:nth-child(even) { background: #f7f5ef; }
code { font-family: Consolas, "Courier New", monospace; font-size: 0.88em; background: #efebdf;
       padding: 0.05rem 0.28rem; border-radius: 3px; }
ul, ol { margin: 0.5rem 0 0.7rem 1.3rem; padding: 0; }
li { margin: 0.25rem 0; }
.pass { color: #1d6b33; font-weight: 600; }
.fail { color: #8c1d1d; font-weight: 600; }
.katex { font-family: XITS, "Cambria Math", Cambria, serif; }
footer { margin-top: 3rem; border-top: 1px solid #c9c4b8; padding-top: 0.8rem;
         font-size: 0.86rem; color: #55504a; }
"""


def escape_text(text):
    """Escape the two characters that confuse an HTML parser.

    Args:
        text: The text to escape.

    Returns:
        The text with the characters & and < escaped.
    """
    return text.replace("&", "&amp;").replace("<", "&lt;")


def escape_outside_math(text):
    """Escape one text and keep every mathematics span unchanged.

    Args:
        text: The text to escape.

    Returns:
        The text with the characters & and < escaped. A mathematics span keeps its control
        words and loses only the two characters that an HTML parser would read as markup.
    """
    parts = []
    position = 0
    for match in MATH_PATTERN.finditer(text):
        parts.append(escape_text(text[position : match.start()]))
        parts.append(escape_text(match.group(0)))
        position = match.end()
    parts.append(escape_text(text[position:]))
    return "".join(parts)


def load_records():
    """Read the check record of every part and merge the values under a part prefix.

    Returns:
        A tuple of the merged values, the records, and the total number of checks.
    """
    values = {}
    records = []
    for path in sorted(glob.glob(os.path.join(OUTPUT_DIRECTORY, "part*_results.json"))):
        with open(path, encoding="utf-8") as stream:
            record = json.load(stream)
        part = int(record["part"])
        passed = sum(1 for item in record["checks"] if item["passed"])
        values["p%d.check_count" % part] = len(record["checks"])
        values["p%d.check_passed" % part] = passed
        for key, value in record["values"].items():
            values["p%d.%s" % (part, key)] = value
        records.append(record)
    values["checks.total"] = sum(len(record["checks"]) for record in records)
    values["checks.passed"] = sum(1 for record in records for item in record["checks"] if item["passed"])
    return values, records


def fill_placeholders(text, values):
    """Replace every placeholder of one text with the value that a script printed.

    Args:
        text: The text with the placeholders.
        values: The merged values of the check records.

    Returns:
        The text with every placeholder replaced.
    """
    missing = []

    def replace(match):
        key = match.group(1)
        if key not in values:
            missing.append(key)
            return match.group(0)
        value = values[key]
        return value if isinstance(value, str) else str(value)

    filled = re.sub(r"\{\{([^}]+)\}\}", replace, text)
    return filled, missing


def figure_element(line, values):
    """Build one figure element with an inline Base64 image.

    Args:
        line: The line of the step file that starts with the figure marker.
        values: The merged values, used for the caption.

    Returns:
        The HTML of the figure.
    """
    body = line.strip()[len("!figure") :].strip()
    file_name, _, caption = body.partition("|")
    file_name = file_name.strip()
    caption = caption.strip()
    path = os.path.join(FIGURE_DIRECTORY, file_name)
    with open(path, "rb") as stream:
        encoded = base64.b64encode(stream.read()).decode("ascii")
    caption = fill_placeholders(caption, values)[0]
    return (
        '<figure><img alt="%s" src="data:image/png;base64,%s">'
        "<figcaption>%s</figcaption></figure>" % (escape_text(file_name), encoded, escape_outside_math(caption))
    )


def inline(text):
    """Convert the inline markup of one line to HTML.

    Args:
        text: One line of a step file.

    Returns:
        The line as HTML with bold text and inline code.
    """
    escaped = escape_outside_math(text)

    def code(match):
        return "<code>%s</code>" % match.group(1)

    escaped = re.sub(r"`([^`]+)`", code, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def block_kind(lines, index):
    """Return the kind of the block that starts at one line.

    Args:
        lines: The lines of one step file.
        index: The index of the line.

    Returns:
        One of the words heading, table, bullet, number, figure, and text. A line of
        displayed mathematics joins the paragraph around it, so that a sentence keeps one
        paragraph from its first word to its last.
    """
    line = lines[index]
    if line.startswith("# "):
        return "heading"
    if line.startswith("## "):
        return "heading"
    if line.startswith("|"):
        return "table"
    if line.startswith("- "):
        return "bullet"
    if re.match(r"^\d+\. ", line):
        return "number"
    if line.startswith("!figure"):
        return "figure"
    return "text"


def join_continuations(lines):
    """Join each indented continuation line to the list item above it.

    Args:
        lines: The lines of one step file.

    Returns:
        The lines with every wrapped list item on one line.
    """
    joined = []
    for line in lines:
        if line.startswith(("  ", "\t")) and joined and joined[-1].startswith(("- ", "|")) is False:
            if joined[-1].startswith(("- ", "$")):
                joined[-1] = joined[-1].rstrip() + " " + line.strip()
                continue
        if line.startswith(("  ", "\t")) and joined and joined[-1].startswith("- "):
            joined[-1] = joined[-1].rstrip() + " " + line.strip()
            continue
        joined.append(line)
    return joined


def render_step(text, values, figure_register):
    """Render one step file to HTML.

    Args:
        text: The text of the step file.
        values: The merged values of the check records.
        figure_register: The list that collects the figure numbers of the page.

    Returns:
        The HTML of the step.
    """
    lines = join_continuations([line.rstrip("\n") for line in text.split("\n")])
    html = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        kind = block_kind(lines, index)
        if kind == "heading":
            marks = len(line) - len(line.lstrip("#"))
            level = 2 if marks >= 2 else 3
            html.append("<h%d>%s</h%d>" % (level, inline(line[marks:].strip()), level))
            index += 1
        elif kind == "display":
            block = [line]
            index += 1
            while index < len(lines) and not lines[index].startswith("$$"):
                block.append(lines[index])
                index += 1
            if index < len(lines):
                block.append(lines[index])
                index += 1
            html.append('<p class="display">%s</p>' % escape_text(" ".join(block)))
        elif kind == "figure":
            html.append(figure_element(line, values))
            figure_register.append(line)
            index += 1
        elif kind == "table":
            rows = []
            while index < len(lines) and lines[index].startswith("|"):
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            rows = [row for row in rows if not all(set(cell) <= set("- ") and cell for cell in row)]
            header = rows[0]
            body = rows[1:]
            parts = ["<table><thead><tr>"]
            parts.extend("<th>%s</th>" % inline(cell) for cell in header)
            parts.append("</tr></thead><tbody>")
            for row in body:
                parts.append("<tr>")
                parts.extend("<td>%s</td>" % inline(cell) for cell in row)
                parts.append("</tr>")
            parts.append("</tbody></table>")
            html.append("".join(parts))
        elif kind in ("bullet", "number"):
            tag = "ul" if kind == "bullet" else "ol"
            items = []
            while index < len(lines) and lines[index].startswith(("- ", "1. ")):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[index]).strip())
                index += 1
            html.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(item) for item in items), tag))
        else:
            paragraph = [line.strip()]
            index += 1
            while index < len(lines) and lines[index].strip() and block_kind(lines, index) == "text":
                paragraph.append(lines[index].strip())
                index += 1
            html.append("<p>%s</p>" % inline(" ".join(paragraph)))
    return "\n".join(html)


def check_table(record):
    """Render the check table of one part.

    Args:
        record: The decoded check record of the part.

    Returns:
        The HTML of the table.
    """
    parts = ["<table><thead><tr><th>Check</th><th>Computed</th><th>Expected</th><th>Result</th></tr></thead><tbody>"]
    for item in record["checks"]:
        mark = '<span class="pass">pass</span>' if item["passed"] else '<span class="fail">fail</span>'
        parts.append(
            "<tr><td>%s</td><td><code>%s</code></td><td><code>%s</code></td><td>%s</td></tr>"
            % (
                escape_outside_math(str(item["name"])),
                escape_text(str(item["computed"])),
                escape_text(str(item["expected"])),
                mark,
            )
        )
    parts.append("</tbody></table>")
    return "".join(parts)


def assert_page(page):
    """Assert every rule of the composed page.

    Args:
        page: The text of the composed page.

    Raises:
        AssertionError: When one rule does not hold.
    """
    control = re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", page)
    assert control is None, "the page holds a control character"
    assert "[WRONG_VALUE]" not in page, "the page holds an unresolved wrong value placeholder"
    assert "[CORRECT_VALUE]" not in page, "the page holds an unresolved correct value placeholder"
    assert "{{" not in page, "the page holds an unresolved placeholder"
    for line in page.split("\n"):
        assert line.count("$") % 2 == 0, "a line holds an odd count of dollars: %r" % line[:120]
    for item in re.findall(r"<li>(.*?)</li>", page, flags=re.S):
        text = re.sub(r"<[^>]+>", "", item).strip()
        assert text.endswith("."), "a list item does not end with a full stop: %r" % text[:80]
    for item in re.findall(r"<p>(.*?)</p>", page, flags=re.S):
        text = re.sub(r"<[^>]+>", "", item).strip()
        assert not text or not text[0].islower(), "a paragraph starts with a lower case word: %r" % text[:80]
    for cell in re.findall(r"<t[hd]>(.*?)</t[hd]>", page, flags=re.S):
        plain = MATH_PATTERN.sub("", re.sub(r"<[^>]+>", "", cell))
        assert "\\" not in plain, "a table cell holds a control word outside mathematics: %r" % plain[:80]
        assert "<" not in plain, "a table cell holds a raw angle bracket: %r" % plain[:80]
    prose = re.sub(r"<script.*?</script>", "", page, flags=re.S)
    prose = re.sub(r"<style.*?</style>", "", prose, flags=re.S)
    prose = re.sub(r"<[^>]+>", "", prose)
    prose = MATH_PATTERN.sub("", prose)
    for line in prose.splitlines():
        assert "\\" not in line, "a control word stands outside mathematics: %r" % line.strip()[:90]
    for caption in re.findall(r"<figcaption>(.*?)</figcaption>", page, flags=re.S):
        plain = MATH_PATTERN.sub("", caption)
        assert "\\" not in plain, "a caption holds a control word outside mathematics: %r" % plain[:80]
        assert "<" not in plain, "a caption holds a raw angle bracket: %r" % plain[:80]
    assert "<code></code>" not in page, "an inline code element is empty"


def main():
    """Compose the page, assert its rules, and write it.

    Returns:
        The path of the composed page.
    """
    values, records = load_records()
    step_paths = sorted(
        glob.glob(os.path.join(STEP_DIRECTORY, "part*_step*.md")),
        key=lambda path: (
            int(re.search(r"part(\d+)_step(\d+)", os.path.basename(path)).group(1)),
            int(re.search(r"part(\d+)_step(\d+)", os.path.basename(path)).group(2)),
        ),
    )
    assert step_paths, "no step file exists"

    figure_register = []
    sections = {}
    missing = []
    for path in step_paths:
        part = int(re.search(r"part(\d+)_step(\d+)", os.path.basename(path)).group(1))
        with open(path, encoding="utf-8") as stream:
            text = stream.read()
        filled, lost = fill_placeholders(text, values)
        missing.extend(lost)
        sections.setdefault(part, []).append(render_step(filled, values, figure_register))
    assert not missing, "the step files hold unknown placeholders: %s" % ", ".join(sorted(set(missing)))
    values["figures.count"] = len(figure_register)

    statement = (
        "Express the integral $\\iiint_E f(x, y, z)\\,dV$ as an iterated integral in six "
        "different ways, where $E$ is the solid bounded by the given surfaces: "
        "$x = 2$, $y = 2$, $z = 0$, and $x + y - 2z = 2$."
    )

    body = []
    body.append('<header class="title"><h1>A triple integral over a tetrahedron in six orders</h1>')
    body.append("<p>Calculus, early transcendentals, section 15.7, exercise 32.</p></header>")
    body.append('<div class="statement"><p><strong>Problem.</strong> %s</p></div>' % escape_outside_math(statement))

    contents = ['<nav class="toc"><strong>Contents</strong><ol>']
    for part in sorted(sections):
        contents.append('<li class="toc"><a href="#part%d">%s</a></li>' % (part, PART_TITLES[part]))
    contents.append('<li class="toc"><a href="#checks">The verification tables</a></li>')
    contents.append("</ol></nav>")
    body.extend(contents)

    for part in sorted(sections):
        body.append('<section id="part%d">' % part)
        body.append("<h2>%s</h2>" % escape_outside_math(PART_TITLES[part]))
        body.extend(sections[part])
        body.append("</section>")

    body.append('<section id="checks"><h2>The verification tables</h2>')
    body.append(
        "<p>The six verification scripts of the tutorial print %d checks, and %d of them pass. "
        "Every row compares a value that one method computes with a value that a different method "
        "computes.</p>" % (values["checks.total"], values["checks.passed"])
    )
    for record in records:
        body.append("<h3>Part %d</h3>" % record["part"])
        body.append(check_table(record))
    body.append("</section>")

    body.append(
        "<footer><p>Composed from the step files under <code>steps/</code> and the records under "
        "<code>code/outputs/</code>. The figures are Base64 images of the files under "
        "<code>code/figures/</code>. The mathematics is rendered with KaTeX 0.16.11, and the "
        "random seed of the reported samples is %s.</p></footer>" % escape_text(str(values["p1.seed"]))
    )

    page = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>A triple integral over a tetrahedron in six orders</title>\n"
        + KATEX_HEAD
        + "\n<style>"
        + STYLE
        + "</style>\n</head>\n<body>\n"
        + "\n".join(body)
        + "\n<script>\ndocument.addEventListener('DOMContentLoaded', function () {\n"
        "  renderMathInElement(document.body, {\n"
        "    delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}],\n"
        "    throwOnError: false\n  });\n});\n</script>\n</body>\n</html>\n"
    )

    assert_page(page)
    with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as stream:
        stream.write(page)
    print("page written: %s" % REPORT_PATH)
    print("steps: %d, figures: %d, checks: %d of %d" % (len(step_paths), len(figure_register), values["checks.passed"], values["checks.total"]))
    return REPORT_PATH


if __name__ == "__main__":
    main()
