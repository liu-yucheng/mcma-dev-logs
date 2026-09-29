# MCMA Experiment Webpage

This folder holds the GitHub Pages site for the MCMA calculus experiment from `.raw_data/dev-logs-20260929` (Sep 23 ~ 29, 2026).

## Files

- `index.html` - Overview page with the summary and the key-term glossary.
- `experiment.html` - Experiment page. It covers the design, the bare-model baseline, the MCMA agent, the tools, and the data files, and lists the categories of statistical data the experiment collects (success and attempt counts, token usage, time usage, cost).
- `briefing.html` - Results Briefing chapter. It combines the former Results Briefing and Statistics pages into one chapter with four sections: Success Rates (per-model solved/first-attempt/attempt counts and charts), Time Usage (chat durations), Cost-effectiveness (estimated CNY and USD), and Token Usage (`usages.json` totals and averages with cache-read and reasoning breakdowns).
- `explorer.html` - Results Explorer page: a two-pane, Windows 11 style file browser over every recorded result. Each pane has a navigation toolbar (back/forward/up/home) and an editable address bar that uses `/` as the path separator (type a path and press Enter to jump), plus a single main list of the current folder with `.` / `..` virtual entries; subdirectories and files open with a single click. Both panes start at the root, which lists `canonical-solutions/` and the model directories. Leaf nodes (`canonical-solution.html`, `remarks.html`, `qna_&lt;timestamp&gt;.html`) follow the tree of `explorer/`; two pages can be viewed side by side.
- `explorer/` - the generated leaf pages, one per recorded result (canonical solutions, model remarks, chat transcripts, and `qna_&lt;timestamp&gt;.html` shortcut redirects) plus the images and `.tex` sources they embed.
- `demo-video.html` - Demo page. No standalone recording was published for this log; it points to the transcript replay in the Results Explorer and the earlier log's demo video.
- `experiments/` - the page images (the agent state graph), referenced from the Agents page.

Shared styles (`styles.css`, `preview.css`, `lightbox.css`, `lightbox.js`) live one level up in `docs/`, alongside the pages of every dev log.

The pages load Chart.js and KaTeX from a CDN. They need an internet connection for the charts and for math rendering. The tables carry the same data without JavaScript.

## Data and statistics

The experiment data lives in `.raw_data/dev-logs-20260929`. Problem set: Stewart Calculus Chapter 15, Sections 7, 8, and 9 (multivariable integrals with plotting requirements), 24 exercises. Six configurations ran: one tools-disabled model (deepseek-flash) and five MCMA agents (deepseek-flash, gemma-4-26b-a4b-it, glm-5.3-flash, MiniMax-M3, qwen-3.8-omni-flash).

The tools-disabled model failed all 24 problems (0%). The MCMA agents produced plots within 5 attempts in 118 of the 120 cases (98%). The only two failures belong to gemma-4-26b-a4b-it on problems 15.7.23 and 15.7.50, where none of the five attempts included an image in the solution.

The pages read no live data. All numbers in the pages come from the per-problem `chat_&lt;timestamp&gt;/` attempt records and the `canonical-solutions/` scans in that folder. Per-attempt outcomes in the explorer's `remarks.html` pages follow a fixed per-session rule: without a `manual_remarks.txt`, the last `chat_&lt;timestamp&gt;/` attempt (in natural order) is the successful one &mdash; its final solution carries the graphical plots &mdash; and every attempt before it is a failed attempt. The two gemma failures (15.7.23 and 15.7.50) carry a `manual_remarks.txt`, and in those sessions every attempt is marked failed.

## Publish on GitHub Pages

The site is self-contained. Any static file server can serve it.

Option A (gh-pages branch):
```
git branch gh-pages
git switch gh-pages
git add --force webpage
git commit -m "Add MCMA experiment page"
git push origin gh-pages
```
Then set the Pages source to the `gh-pages` branch, root folder.

Option B (docs folder):
1. Copy this folder's content to `docs/` in the repo.
2. In the repo settings, set Pages source to `Deploy from a branch`.
3. Select the branch and the `/docs` folder.

Option C (any static host):
Serve the `webpage/` folder as-is. The pages need no build step.

## Data provenance

The pages read no live data. All numbers come from the attempt records and the canonical scans in `.raw_data/dev-logs-20260929`.

Copyright (C) 2026 Yucheng Liu. Licensed under the GNU AGPL 3.0.
