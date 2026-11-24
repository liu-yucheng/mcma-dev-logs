"""Build report.html from the template and the figures.

The script reads report.template.html, replaces each figure token with a Base64
data uniform resource identifier, and writes report.html.  The page then needs no
image file, and it opens without a web server.

Returns:
    The process exit status: 0 on success.
"""

from __future__ import annotations

import base64
from pathlib import Path

WORKSPACE: Path = Path(__file__).resolve().parent.parent
"""Root directory of the session workspace."""

TEMPLATE_PATH: Path = WORKSPACE / "report.template.html"
"""Path of the page template with the figure tokens."""

OUTPUT_PATH: Path = WORKSPACE / "report.html"
"""Path of the composed page."""

FIGURE_TOKENS: dict[str, Path] = {
    "__FIG1__": WORKSPACE / "code" / "figures" / "part1_figure1.png",
    "__FIG2__": WORKSPACE / "code" / "figures" / "part2_figure1.png",
    "__FIG3__": WORKSPACE / "code" / "figures" / "part3_figure1.png",
    "__FIG4__": WORKSPACE / "code" / "figures" / "part4_figure1.png",
}
"""Map from the token in the template to the image file."""


def to_data_uri(image_path: Path) -> str:
    """Return the Base64 data uniform resource identifier of an image file.

    Args:
        image_path: Path of a PNG file.

    Returns:
        A string of the form data:image/png;base64,....
    """
    payload = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def main() -> int:
    """Compose the page and write it.

    Returns:
        The process exit status: 0 on success.
    """
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, image_path in FIGURE_TOKENS.items():
        text = text.replace(token, to_data_uri(image_path))
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
