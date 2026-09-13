"""Run the serial-number sticker generator using the active config."""

from . import config
from .pdf import generate_sticker_pdfs


def main() -> int:
    paths = generate_sticker_pdfs(
        hardware_types=config.GENERATE_TYPES,
        start=config.GENERATE_START,
        end=config.GENERATE_END,
        output_dir=config.OUTPUT_DIR,
    )
    print(f"Wrote {len(paths)} PDF(s) to {config.OUTPUT_DIR}")
    for path in paths:
        print(path)
    return 0
