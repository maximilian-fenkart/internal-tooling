#!/usr/bin/env python3
"""Generate A4 PDF sheets of Sodex IT hardware serial stickers.

Edit the constants below, then run this script.
"""

from pathlib import Path

import internaltooling
from internaltooling.serial_numbers import config
from internaltooling.serial_numbers.cli import main

# --- Paths -----------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[1]
_SOURCE_DATA_DIR = Path(internaltooling.__file__).resolve().parent / "source-data"
LOGO_PATH = _SOURCE_DATA_DIR / "Sodex_Primary_Logo_White.svg"
OUTPUT_DIR = _REPO_ROOT / "data"

# --- Serial number format --------------------------------------------------
# Example: SIT-LAP-000001
SERIAL_PREFIX = "SIT"
HARDWARE_TYPES = ("LAP", "PHO", "PER", "MON", "COM")
SERIAL_DIGITS = 5
SERIAL_MIN = 1
SERIAL_MAX = 99_999

# Inclusive batch to print this run (must be within SERIAL_MIN..SERIAL_MAX).
GENERATE_TYPES = HARDWARE_TYPES
GENERATE_START = 1
GENERATE_END = 99_999
GENERATE_END = 48

# Split large batches so each PDF stays printable.
MAX_PAGES_PER_PDF = 50

# --- Sticker geometry (centimetres) ----------------------------------------
STICKER_WIDTH_CM = 4.5
STICKER_HEIGHT_CM = 2.0

# --- Page layout (millimetres) ---------------------------------------------
PAGE_WIDTH_MM = 210.0  # A4
PAGE_HEIGHT_MM = 297.0  # A4
PAGE_MARGIN_MM = 10.0
STICKER_GAP_MM = 2.0
STICKER_PADDING_MM = 1.5
STICKER_INNER_GAP_MM = 1.5
STICKER_BORDER_MM = 0.15
STICKER_CORNER_RADIUS_MM = 2.0
QR_BORDER_MODULES = 1
QR_CORNER_RADIUS_MM = 0.8

# --- Brand colours ---------------------------------------------------------
COLOR_DARK_BLUE = "#012439"
COLOR_ICON_BLUE = "#00ACF0"
COLOR_OFF_WHITE = "#E3EDF1"
COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"

PAGE_BACKGROUND = COLOR_WHITE
STICKER_BACKGROUND = COLOR_DARK_BLUE
STICKER_BORDER_COLOR = COLOR_ICON_BLUE
SERIAL_TEXT_COLOR = COLOR_WHITE
QR_FILL = COLOR_BLACK
QR_BACKGROUND = COLOR_WHITE


def _apply_config() -> None:
    for name, value in globals().items():
        if name.isupper() and hasattr(config, name):
            setattr(config, name, value)


if __name__ == "__main__":
    _apply_config()
    raise SystemExit(main())
