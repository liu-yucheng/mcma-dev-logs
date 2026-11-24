"""Record the checks of one part and write the markdown summary that the page quotes.

The summary table is the only source of a verified number in the composed page.  One row is two
values that two different methods compute, the difference of the two values, and a tolerance that
the statement of the problem supports.
"""

import pathlib

OUTPUT_DIRECTORY = pathlib.Path(__file__).resolve().parent / "outputs"
"""Directory that holds the summary table of each part."""


class CheckLog:
    """Hold the checks of one part and write them as a markdown table."""

    def __init__(self, part_name: str) -> None:
        """Create an empty log for one part of the tutorial.

        Args:
            part_name: Name of the part, used as the file name of the summary.
        """
        self.part_name = part_name
        self.rows: list[tuple[str, str, str, str, str]] = []
        self.all_passed = True

    def record(
        self,
        name: str,
        computed: float | str,
        reference: float | str,
        difference: float | str,
        passed: bool,
    ) -> None:
        """Record one check and print its four values.

        Args:
            name: Short name of the check, which the step file quotes.
            computed: Value that the first method computes.
            reference: Value that the second method computes.
            difference: Difference of the two values, or the standard error distance.
            passed: Whether the difference lies inside the tolerance of the check.
        """
        computed_text = f"{computed:.12g}" if isinstance(computed, float) else str(computed)
        reference_text = f"{reference:.12g}" if isinstance(reference, float) else str(reference)
        difference_text = f"{difference:.3e}" if isinstance(difference, float) else str(difference)
        status = "pass" if passed else "FAIL"
        if not passed:
            self.all_passed = False
        self.rows.append((name, computed_text, reference_text, difference_text, status))
        print(
            f"{name} | computed={computed_text} | reference={reference_text} "
            f"| difference={difference_text} | {status}",
            flush=True,
        )

    def require_all_passed(self) -> None:
        """Raise an error when one check of this part failed."""
        if not self.all_passed:
            failed = [row[0] for row in self.rows if row[4] != "pass"]
            raise RuntimeError(f"{self.part_name} has failed checks: {failed}")

    def summary_lines(self) -> list[str]:
        """Return the markdown lines of the summary table."""
        lines = [
            "| Check | Computed value | Reference value | Difference | Status |",
            "| --- | --- | --- | --- | --- |",
        ]
        for name, computed, reference, difference, status in self.rows:
            lines.append(f"| {name} | {computed} | {reference} | {difference} | {status} |")
        return lines

    def write(self) -> pathlib.Path:
        """Write the markdown summary of this part and return its path."""
        OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIRECTORY / f"{self.part_name}_summary.md"
        path.write_text("\n".join(self.summary_lines()) + "\n", encoding="utf-8")
        print(f"{self.part_name}: {len(self.rows)} checks, "
              f"{0 if self.all_passed else 1} failed part(s)", flush=True)
        return path
