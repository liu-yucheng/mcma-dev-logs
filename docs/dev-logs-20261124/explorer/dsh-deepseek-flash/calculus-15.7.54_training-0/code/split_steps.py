"""Split the drafted step blocks into one file for each step.

The drafting files hold more than one step. This script writes one file
``steps/part<part number>_step<step number>.md`` for each step block and
deletes the drafting files, so that every step has one file of its own.
"""

from __future__ import annotations

import os
import re

DRAFT_NAMES = ("part1_steps.md", "part234_steps.md", "part5_steps.md")
HEADING_PATTERN = re.compile(r"^## Part (\d+), Step (\d+): (.+)$")
SECTION_FIGURE = "FIGURE: part2_figure1.png | The section of $E$ at $y = 0$. The three horizontal chords are the diameters of the sections at $z = 0.25$, $z = 0.5$, and $z = 0.75$; the dashed lines mark the half width $\\sqrt{1 - z}$ of the middle chord."


def main() -> None:
    """Write one file for each step block and remove the drafting files."""
    steps_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "steps")
    blocks: list[tuple[int, int, list[str]]] = []
    for draft_name in DRAFT_NAMES:
        draft_path = os.path.join(steps_directory, draft_name)
        with open(draft_path, encoding="utf-8") as draft_file:
            draft_lines = draft_file.read().splitlines()
        current_part = 0
        current_step = 0
        current_lines: list[str] = []
        for line in draft_lines:
            match = HEADING_PATTERN.match(line)
            if match:
                if current_lines:
                    blocks.append((current_part, current_step, current_lines))
                current_part = int(match.group(1))
                current_step = int(match.group(2))
                current_lines = [line]
            elif current_lines:
                current_lines.append(line)
        if current_lines:
            blocks.append((current_part, current_step, current_lines))

    seen: set[tuple[int, int]] = set()
    for part_number, step_number, block_lines in blocks:
        if (part_number, step_number) in seen:
            raise ValueError("one step number appears twice")
        seen.add((part_number, step_number))
        body = list(block_lines)
        if part_number == 1 and step_number == 3:
            body.insert(len(body) - 1, SECTION_FIGURE)
        output_name = f"part{part_number}_step{step_number}.md"
        output_path = os.path.join(steps_directory, output_name)
        with open(output_path, "w", encoding="utf-8", newline="\n") as output_file:
            output_file.write("\n".join(body).rstrip() + "\n")
        print("wrote", output_name, f"{len(body)} lines")

    for draft_name in DRAFT_NAMES:
        os.remove(os.path.join(steps_directory, draft_name))
    print("step files:", len(seen))


if __name__ == "__main__":
    main()
