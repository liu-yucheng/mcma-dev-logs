# MCMA Literature Review Webpage

This folder holds the GitHub Pages site for the AI-assisted literature review from `.raw_data/lit-review-20260904/mcma-ai-assisted-review.md` (Sep. 04, 2026). It accompanies the experiment site `dev-logs-20260824`.

## Files

- `index.html` - Overview page: report profile, executive summary, the four research gaps, a reading guide, and a glossary of key terms.
- `benchmarks.html` - Chapter 1: the evolving landscape of multimodal mathematical reasoning evaluation (MathVista, MMMU, MathVerse, MATH-Vision, and the generative/agentic benchmarking gap).
- `agents.html` - Chapter 2: agentic frameworks and their limitations (code-as-policy, multi-agent systems, sketching as reasoning, adaptive architectures).
- `toolchain.html` - Chapter 3: the visualization toolchain, a tale of two tools (`matplotlib.pyplot` ubiquity vs. the `PGFplots` research void).
- `sketching.html` - Chapter 4: 3D surface sketching and fundamental spatial-reasoning challenges.
- `pedagogy.html` - Chapter 5: the unaddressed challenge of pedagogical effectiveness.
- `recommendations.html` - Chapter 6: conclusion and strategic recommendations for the four research gaps.
- `references.html` - The full citation data behind the report: numbered references, additional sources (not directly cited), and other sources.

The pages share the site-wide `styles.css` (in the parent `docs/` folder) and load no external libraries. They need no internet connection.

## About the citation numbering

The source report uses two parallel citation-numbering schemes: the in-text markers in the chapter pages and the grouped reference list reproduced on `references.html`. The chapter pages keep the in-text markers as written in the report, and each marker links to the reference entry that matches its context. The reference data itself is unchanged from the raw report.

## Data provenance

The review data lives in `.raw_data/lit-review-20260904/mcma-ai-assisted-review.md`. The pages read no live data; all content and citations come from that file.

## Publish on GitHub Pages

The site is static and self-contained. Serve the `docs/` folder (or this folder on a static host), or copy it to a `gh-pages` branch as described in `../dev-logs-20260824/README.md` (Option A / C).

Copyright (C) 2026 Yucheng Liu. Licensed under the GNU AGPL 3.0.
