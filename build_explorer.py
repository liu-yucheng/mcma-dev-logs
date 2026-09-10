#!/usr/bin/env python3
"""Build the ./webpage/explorer/ tree and regenerate explorer.html.

Reads the experiment-results tree, generates:
  - canonical-solution.html  (from problem.png + solution.png)
  - remarks.html             (from remarks.json)
  - qna.html                 (from <timestamp>_qna.md, or a fallback from
    <timestamp>_human.md when the run produced no transcript)
  - qna_<timestamp>.html     (a shortcut leaf at <model>/<problem>/ that
    redirects to the deep <chat>/qna.html)
copies them plus every image / tex they reference into
webpage/explorer/ preserving the folder tree structure, and finally
injects the resulting tree into webpage/explorer.html so the explorer
can render it without any runtime directory listing.
"""
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

import markdown as markdown_lib

ROOT = Path(r"D:\Program-Files\MCMA-Toolchain\dev-logs")
SRC = ROOT / ".raw_data" / "dev-logs-20260824" / "experiment-results"
DST = ROOT / "webpage" / "explorer"
PAGE = ROOT / "webpage" / "explorer.html"

KATEX_CSS = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"
KATEX_JS = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"
AUTORENDER_JS = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"

HLJS_CSS = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css"
HLJS_JS = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"
HLJS_LATEX = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/latex.min.js"

HTML_EXTENSIONS = ["tables", "fenced_code"]


def base_for(rel_path: str) -> str:
    """Relative prefix from a leaf file (under webpage/explorer/) to the
    webpage root, where styles.css / preview.css / lightbox.css live."""
    depth = len(Path(rel_path).parts) - 1
    return "../" * (depth + 1)


def page_skeleton(title: str, base: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; MCMA results explorer</title>
<link rel="stylesheet" href="{base}styles.css">
<link rel="stylesheet" href="{base}preview.css">
<link rel="stylesheet" href="{base}lightbox.css">
<link rel="stylesheet" href="{KATEX_CSS}">
<link rel="stylesheet" href="{HLJS_CSS}">
<script defer src="{KATEX_JS}"></script>
<script defer src="{AUTORENDER_JS}"></script>
<script defer src="{HLJS_JS}"></script>
<script defer src="{HLJS_LATEX}"></script>
<script defer src="{base}lightbox.js"></script>
</head>
<body>
{body_html}
<script>
document.addEventListener("DOMContentLoaded", function () {{
  renderMathInElement(document.body, {{
    delimiters: [
      {{ left: "$$", right: "$$", display: true }},
      {{ left: "\\\\[", right: "\\\\]", display: true }},
      {{ left: "\\\\(", right: "\\\\)", display: false }},
      {{ left: "$", right: "$", display: false }}
    ],
    throwOnError: false
  }});
  if (window.hljs) {{
    hljs.configure({{ languages: ["latex", "markdown", "python", "bash", "json"] }});
    hljs.highlightAll();
  }}
}});
</script>
</body>
</html>
"""


def footer_html(path_display: str) -> str:
    return f"""<footer class="site">
  <div class="container">
    <p><strong>MCMA &mdash; Math-Capable Multimodal Agents.</strong> Record <code>{path_display}</code>, experiment log <code>dev-logs-20260824</code>. Licensed under the GNU AGPL 3.0.</p>
  </div>
</footer>"""


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# --------------------------------------------------------------------------
# markdown -> HTML (qna / fallback human transcripts)
# --------------------------------------------------------------------------

MATH_TOKENS = []


def _protect_math(t: str) -> str:
    def rep(m):
        MATH_TOKENS.append(m.group(0))
        return "@@MATH%d@@" % (len(MATH_TOKENS) - 1)

    t = re.sub(r"\$\$(?:\s)?(.*?)(?:\s)?\$\$", rep, t, flags=re.S)
    t = re.sub(r"\\\[(.*?)\\\]", rep, t, flags=re.S)
    t = re.sub(r"\\\((.*?)\\\)", rep, t, flags=re.S)
    t = re.sub(r"(?<!@@MATH)(?<!\w)\$([^$\n]+?)\$", rep, t)
    return t


# Glyphs that break monospace alignment when they appear verbatim inside a
# fenced code block. Replace them with their ASCII (fixed-width) equivalent
# so every line of a rendered code block stays column-aligned.
CODE_ASCII_MAP = {
    "\u00b1": "+/-",  # PLUS-MINUS SIGN -> "+/-"
}


def _normalize_code_nonascii(t: str) -> str:
    """Rewrite non-ASCII glyphs inside fenced code blocks to ASCII.

    Only the interior of ```fenced``` blocks is touched, so the raw glyphs
    in prose / KaTeX math outside code blocks are preserved as-is.
    """
    if not CODE_ASCII_MAP:
        return t

    def rep(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        for ch, repl in CODE_ASCII_MAP.items():
            body = body.replace(ch, repl)
        return head + body + tail

    return re.sub(r"(?ms)^(```[^\n]*\n)(.*?)(^```[ \t]*$)", rep, t)


def _image_figure(url: str, alt: str) -> str:
    url = url.replace("\\", "/")
    name = os.path.basename(url.rstrip("/"))
    alt = name if not alt else alt
    return (
        '<figure class="refimg"><img class="zimg" src="%s" alt="%s">'
        '<figcaption>%s</figcaption></figure>'
        % (html_escape(url), html_escape(alt), html_escape(name))
    )


def md_to_html(md_text: str, add_note: str = "") -> str:
    global MATH_TOKENS
    MATH_TOKENS = []
    t = _protect_math(md_text)
    t = _normalize_code_nonascii(t)

    # message turns
    t = re.sub(
        r"`\[ Begin message\. Type: (\w+)Message\. \]`",
        lambda m: '\n\n<div class="turn %s">\n\n'
        % ("human" if m.group(1).lower() == "human" else "ai"),
        t,
    )
    t = re.sub(r"`\[ End message\. Type: \w+Message\. \]`", "\n\n</div>\n\n", t)
    t = re.sub(r"`\[Begin Problem\]`", '\n\n<div class="seg">Problem</div>\n\n', t)
    t = re.sub(r"`\[End Problem\]`", '\n\n<div class="seg seg-end">End of problem</div>\n\n', t)
    t = re.sub(r"`\[Begin Answer\]`", '\n\n<div class="seg">Answer</div>\n\n', t)
    t = re.sub(r"`\[End Answer\]`", '\n\n<div class="seg seg-end">End of answer</div>\n\n', t)

    # "(Image `x`. Alt text: y.)" references
    t = re.sub(
        r"\(Image `([^`]+)`\.\s*Alt text:\s*([^)]*?)\)",
        lambda m: (
            "\n\n"
            if m.group(1).strip() == "problem.png"
            else _image_figure(m.group(1).strip(), m.group(2).strip())
        ),
        t,
    )
    # markdown image links  ![alt](url)
    t = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: _image_figure(m.group(2).strip(), m.group(1).strip()),
        t,
    )

    body = markdown_lib.markdown(t, extensions=HTML_EXTENSIONS)
    # restore protected math
    for i, tok in enumerate(MATH_TOKENS):
        body = body.replace("@@MATH%d@@" % i, tok)

    if add_note:
        body = (
            '<div class="note-warn">%s</div>\n' % html_escape(add_note)
        ) + body
    return body


def collect_md_assets(md_text: str) -> list:
    """Return the files a transcript references relative to its containing dir."""
    md_text = re.sub(r"(?s)^```.*?^```", "", md_text, count=0, flags=re.M) if "```" in md_text else md_text
    md_text = re.sub(r"(?s)```.*?```", "", md_text)
    assets = set()
    for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", md_text):
        assets.add(m.group(2).strip())
    for m in re.finditer(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)", md_text):
        assets.add(m.group(1).strip())
    for m in re.finditer(r"\(Image `([^`]+)`", md_text):
        assets.add(m.group(1).strip())
    result = []
    for a in assets:
        a = re.sub(r"^\.?[/\\]+", "", a)
        if not a or a == "problem.png":
            continue
        result.append(a)
    return sorted(result)


def resolve_asset(chat_dir: Path, name: str) -> Path | None:
    """Resolve a referenced asset: chat dir first, then <ts>_qna subfolder."""
    cand = [chat_dir / name]
    head = name.split("/")[0].split("\\")[0]
    if "_" in head:
        ts = head[:-4] if head.endswith("_qna") else None
    # try <chat>/<ts>_qna/<basename> when the name is a bare qna image
    if "/" not in name and "\\" not in name:
        for sub in chat_dir.iterdir():
            if sub.is_dir() and sub.name.endswith("_qna"):
                cand.append(sub / name)
    for c in cand:
        if c.is_file():
            return c
    return None


def copy_file(src: Path, rel: str) -> None:
    dst = DST / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def dedupe_qna_images(chat_dst: Path) -> None:
    """Remove every non-`*_qna/` image from a generated chat dir.

    Each chat record keeps its transcript images only inside the
    `*_qna/` subfolder.  The rendered plot copies (`*_pyplot_*.png`,
    `*_pgfplots_*.png`) and any other image files at the chat root are
    duplicates of those transcript images and get deleted.  Their
    `<figure>` blocks in qna.html are dropped too, since the surviving
    `*_qna/` figure already shows the same content.
    """
    qna_dirs = [p for p in chat_dst.iterdir() if p.is_dir() and p.name.endswith("_qna")]
    root_pngs = sorted(chat_dst.glob("*.png"))
    if not root_pngs:
        return

    html = chat_dst / "qna.html"
    if html.is_file():
        txt = html.read_text(encoding="utf-8")
        fig_re = re.compile(r'<figure class="refimg">.*?</figure>', re.S)
        fig_blocks = list(fig_re.finditer(txt))

        edits = []
        for m in fig_blocks:
            img = re.search(r'<img[^>]*\bsrc="([^"]+)"', m.group(0))
            if not img:
                continue
            src = img.group(1).strip().replace("\\", "/").lstrip("./")
            heads = src.split("/", 1)
            in_qna = "/" in src and any(hs == qd.name for hs in [heads[0]] for qd in qna_dirs)
            if in_qna:
                continue
            s, e = m.span()
            if txt[e:e + 3] == ". )" or txt[e:e + 2] == ".)":
                trailing = 2 if txt[e:e + 2] == ".)" else 3
            else:
                trailing = 0
            edits.append((s, e + trailing, ""))
        for s, e, repl in sorted(edits, reverse=True):
            txt = txt[:s] + repl + txt[e:]
        html.write_text(txt, encoding="utf-8")

    for f in root_pngs:
        f.unlink()


# --------------------------------------------------------------------------
# leaf page generators
# --------------------------------------------------------------------------

def gen_canonical(prob_dir: Path, problem: str) -> None:
    rel = "canonical-solutions/%s/canonical-solution.html" % problem
    base = base_for(rel)
    for img in ("problem.png", "solution.png"):
        src = prob_dir / img
        if src.is_file():
            copy_file(src, "canonical-solutions/%s/%s" % (problem, img))
    intro = (
        "The printed exercise and the reference (canonical) solution as scanned "
        "from the problem bank. Click an image to zoom."
    )
    body = f"""<header class="site">
  <div class="container">
    <div class="kicker">Canonical solution</div>
    <h1>{html_escape(problem)}</h1>
    <p class="lede">{intro}</p>
  </div>
</header>
<main class="container">
<section>
  <p class="small">Path: <code>canonical-solutions/{html_escape(problem)}</code></p>
  <div class="gallery">
    <figure><img class="zimg" src="problem.png" alt="Printed problem for {html_escape(problem)}."><figcaption>Problem <code>{html_escape(problem)}</code>. Click to zoom.</figcaption></figure>
    <figure><img class="zimg" src="solution.png" alt="Canonical solution for {html_escape(problem)}."><figcaption>Canonical solution. Click to zoom.</figcaption></figure>
  </div>
</section>
</main>
{footer_html('canonical-solutions/%s' % problem)}
"""
    (DST / rel).parent.mkdir(parents=True, exist_ok=True)
    (DST / rel).write_text(page_skeleton(problem + " — canonical solution", base, body), encoding="utf-8")


def gen_remarks(model: str, prob_dir: Path, problem: str) -> None:
    rel = "%s/%s/remarks.html" % (model, problem)
    base = base_for(rel)
    rj = json.loads((prob_dir / "remarks.json").read_text(encoding="utf-8"))
    count = int(rj.get("attempt_count", 0))
    worked = rj.get("attempt_worked_as_expected", [])
    reasons = rj.get("reattempt_reasons", [])
    rows = []
    for i in range(max(count, 1)):
        ok = worked[i] if i < len(worked) else None
        reason = reasons[i] if i < len(reasons) else None
        badge = '<span class="badge good">worked</span>' if ok else (
            '<span class="badge bad">failed</span>' if ok is False else '<span class="badge">n/a</span>'
        )
        reason_txt = "—" if reason is None else html_escape(str(reason))
        rows.append(
            "<tr><td class=\"num\">attempt %d</td><td>%s</td><td>%s</td></tr>"
            % (i + 1, badge, reason_txt)
        )
    body = f"""<header class="site">
  <div class="container">
    <div class="kicker">Model remarks</div>
    <h1>{html_escape(problem)}</h1>
    <p class="lede">Run bookkeeping for <code>{html_escape(model)}</code>: how many attempts were taken, whether each attempt produced the expected output, and why any re-attempt was needed.</p>
  </div>
</header>
<main class="container">
<section>
  <p class="small">Path: <code>{html_escape(model)}/{html_escape(problem)}</code></p>
  <table>
    <thead><tr><th>Aspect</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Attempt count</td><td class="num">{count}</td></tr>
      <tr><td>Worked as expected</td><td>{"yes" if all(w is True for w in worked) and count else "no"}</td></tr>
    </tbody>
  </table>
  <h3>Per-attempt detail</h3>
  <table>
    <thead><tr><th>#</th><th>Outcome</th><th>Re-attempt reason</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</section>
</main>
{footer_html('%s/%s' % (model, problem))}
"""
    (DST / rel).parent.mkdir(parents=True, exist_ok=True)
    (DST / rel).write_text(page_skeleton(problem + " — remarks · " + model, base, body), encoding="utf-8")


def gen_qna(model: str, problem: str, chat_dir: Path) -> None:
    rel = "%s/%s/%s/qna.html" % (model, problem, chat_dir.name)
    base = base_for(rel)
    qna_files = sorted(chat_dir.glob("*_qna.md"))
    if qna_files:
        md_path = qna_files[0]
        md_text = md_path.read_text(encoding="utf-8")
        note = ""
        title_src = "{0}/{1}/{2}".format(model, problem, chat_dir.name)
        ts = md_path.name[:-7]  # strip _qna.md
    else:
        human = sorted(chat_dir.glob("*_human.md"))
        if human:
            md_path = human[0]
            md_text = md_path.read_text(encoding="utf-8")
            ts = md_path.name[:-9]  # strip _human.md
        else:
            ts = chat_dir.name.replace("chat_", "")
            md_text = ""
        note = (
            "This run produced no assistant transcript. The record only contains "
            "the human (user) message%s; there is no answer from the agent."
            % ("" if human else " — even that is missing")
        )
        title_src = "{0}/{1}/{2}".format(model, problem, chat_dir.name)
    # copy referenced assets
    for asset in collect_md_assets(md_text):
        src = resolve_asset(chat_dir, asset)
        if src:
            copy_file(src, "%s/%s/%s/%s" % (model, problem, chat_dir.name, asset))
        else:
            print(f"  [warn] missing asset {asset} in {chat_dir.name}")
    body_html = md_to_html(md_text, add_note=note)
    if not body_html.strip():
        body_html = '<p class="small">No transcript content recorded for this chat.</p>'
    body = f"""<header class="site">
  <div class="container">
    <div class="kicker">Question &amp; answer transcript</div>
    <h1>{html_escape(ts)}</h1>
    <p class="lede">The <code>_qna.md</code> record: the problem given to the agent and the agent&rsquo;s answer, with the plots it produced.</p>
  </div>
</header>
<main class="container">
<p class="small">Path: <code>{html_escape(title_src)}</code></p>
{body_html}
</main>
{footer_html(title_src)}
"""
    (DST / rel).parent.mkdir(parents=True, exist_ok=True)
    (DST / rel).write_text(page_skeleton(ts + " — Q&amp;A · " + model, base, body), encoding="utf-8")

    # drop duplicate / non-`*_qna/` images copied into the chat dir
    dedupe_qna_images(DST / model / problem / chat_dir.name)

    # shortcut leaf at <model>/<problem>/qna_<timestamp>.html so the transcript
    # is reachable by the shorter path instead of <chat>/qna.html
    gen_qna_shortcut(model, problem, chat_dir, ts)


def gen_qna_shortcut(model: str, problem: str, chat_dir: Path, ts: str) -> None:
    rel = "%s/%s/qna_%s.html" % (model, problem, ts)
    deep = "%s/%s/%s/qna.html" % (model, problem, chat_dir.name)
    body = f"""<header class="site">
  <div class="container">
    <div class="kicker">Question &amp; answer transcript</div>
    <h1>{html_escape(ts)}</h1>
    <p class="lede">Shortcut to the Q&amp;A transcript; the full record lives at <code>{html_escape(deep)}</code>.</p>
  </div>
</header>
<main class="container">
  <p class="small">Shortcut: <code>{html_escape(rel)}</code> &rarr; <code>{html_escape(deep)}</code></p>
  <div class="note-warn">This is a shortcut page &mdash; redirecting to the full transcript.</div>
  <p>If you are not redirected automatically, <a href="{html_escape(chat_dir.name + '/qna.html')}">open the Q&amp;A transcript</a>.</p>
  <script>window.location.replace("{chat_dir.name}/qna.html");</script>
</main>
{footer_html('%s/%s' % (model, problem))}
"""
    (DST / rel).parent.mkdir(parents=True, exist_ok=True)
    (DST / rel).write_text(
        page_skeleton(ts + " — Q&amp;A · " + model, base_for(rel), body), encoding="utf-8"
    )


# --------------------------------------------------------------------------
# tree scan for the explorer
# --------------------------------------------------------------------------

def _scan_tree(dir_path: Path, root_rel: str) -> list:
    """Returns a list of nodes: {'n': name, 'p': relpath} for html leaves, or
    {'n': name, 'c': [...]} for directories that contain html leaves."""
    nodes = []
    for entry in sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        rel = (root_rel + "/" + entry.name).lstrip("/")
        if entry.is_dir():
            children = _scan_tree(entry, rel)
            if children:
                nodes.append({"n": entry.name, "c": children})
        elif entry.name.endswith(".html"):
            nodes.append({"n": entry.name, "p": rel, "t": "html"})
        elif entry.suffix.lower() == ".png":
            pass
    return nodes


def build_tree() -> list:
    if not DST.is_dir():
        return []
    return _scan_tree(DST, "")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> None:
    models = [d.name for d in SRC.iterdir() if d.is_dir() and d.name != "canonical-solutions"]
    problems = sorted(
        p.name
        for p in (SRC / "canonical-solutions").iterdir()
        if p.is_dir() and (p / "problem.png").is_file() and (p / "solution.png").is_file()
    )

    if DST.is_dir():
        shutil.rmtree(DST)
    DST.mkdir(parents=True, exist_ok=True)

    # canonical solutions
    for problem in problems:
        gen_canonical(SRC / "canonical-solutions" / problem, problem)

    # model remarks + chats
    for model in models:
        model_dir = SRC / model
        if not model_dir.is_dir():
            continue
        for prob_dir in sorted(model_dir.iterdir()):
            if not prob_dir.is_dir() or not (prob_dir / "remarks.json").is_file():
                continue
            problem = prob_dir.name
            gen_remarks(model, prob_dir, problem)
            for chat_dir in sorted(prob_dir.iterdir()):
                if chat_dir.is_dir() and chat_dir.name.startswith("chat_"):
                    gen_qna(model, problem, chat_dir)

    tree = build_tree()
    tree_src = json.dumps(tree, ensure_ascii=False)

    page = PAGE.read_text(encoding="utf-8")
    begin = "//RESULTS_TREE:BEGIN"
    end = "//RESULTS_TREE:END"
    if begin in page and end in page:
        head = page.split(begin, 1)[0]
        tail = page.split(end, 1)[1]
        page = (
            head
            + begin
            + "\n"
            + "  var RESULTS_TREE = "
            + tree_src
            + ";\n"
            + "  "
            + end
            + tail
        )
    else:
        marker = "@@RESULTS_TREE@@"
        if marker not in page:
            raise SystemExit("explorer.html lacks the RESULTS_TREE markers or @@RESULTS_TREE@@ placeholder")
        page = page.replace(marker, tree_src)
    PAGE.write_text(page, encoding="utf-8")

    print("problems:", len(problems))
    print("leaf html files written:", sum(
        1 for _ in DST.rglob("*.html")
    ))
    print("explorer.html tree injected; leaf nodes:", sum(leaves(n) for n in tree) if tree else 0)


def leaves(n):
    if "c" in n:
        c = 0
        for ch in n["c"]:
            c += leaves(ch)
        return c
    return 1


if __name__ == "__main__":
    main()