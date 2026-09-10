# MCMA Experiment Webpage

This folder holds the GitHub Pages site for the MCMA calculus experiment from `.raw_data/dev-logs-20260824` (Aug 21 ~ 27, 2026).

## Files

- `index.html` - Overview page with the summary and the key-term glossary.
- `experiment.html` - Experiment page. It covers the design, the bare-model baseline, the MCMA agent, the tools, and the data files.
- `briefing.html` - Results Briefing page with the per-model table and the charts.
- `explorer.html` - Results Explorer page: a two-pane, Windows 11 style file browser over every recorded result. Each pane has a navigation toolbar (back/forward/up/home) and an editable address bar that uses `/` as the path separator (type a path and press Enter to jump), plus a single main list of the current folder with `.` / `..` virtual entries; subdirectories and files open with a single click. Both panes start at the root, which lists `canonical-solutions/` and the model directories. Leaf nodes (`canonical-solution.html`, `remarks.html`, `qna.html`, `qna_&lt;timestamp&gt;.html`) follow the tree of `explorer/`; two pages can be viewed side by side.
- `explorer/` - the generated leaf pages, one per recorded result (canonical solutions, model remarks, chat transcripts, and `qna_&lt;timestamp&gt;.html` shortcut redirects) plus the images they embed.
- `preview.css` - half-pane styles for the generated detail pages so they read well in the explorer's side-by-side viewers on 16:9 FHD and larger screens.
- `styles.css` - shared styles for all pages.
- `lightbox.css` and `lightbox.js` - the shared image viewer. Click any image marked with the `zimg` class to open it. The viewer supports zoom in, zoom out, reset, and pan. The `+` and `-` keys zoom. The `0` key resets. The `Esc` key closes.
- `experiments/` - the page images (state graph etc.), referenced only from the Experiment page.

The pages load Chart.js and KaTeX from a CDN. They need an internet connection for the charts and for math rendering. The tables carry the same data without JavaScript.

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

The experiment data lives in `.raw_data/dev-logs-20260824`. The pages read no live data. All numbers in the pages come from the `attempts`/`remarks` records in that folder.

Copyright (C) 2026 Yucheng Liu. Licensed under the GNU AGPL 3.0.