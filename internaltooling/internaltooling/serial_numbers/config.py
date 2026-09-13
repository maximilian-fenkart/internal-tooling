"""Runtime settings for the serial-number sticker generator.

Edit values in ``bin/generate-serial-stickers.py``. These are library defaults.
"""

from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DATA_DIR = _PACKAGE_DIR / "source-data"


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "internaltooling" / "setup.py").is_file() and (parent / "bin").is_dir():
            return parent
    return Path.cwd()


# --- Paths -----------------------------------------------------------------
_REPO_ROOT = _repo_root()
LOGO_PATH = SOURCE_DATA_DIR / "Sodex_Primary_Logo_White.svg"
OUTPUT_DIR = _REPO_ROOT / "data"

# --- Serial number format --------------------------------------------------
# Example: SIT-LAP-000001
SERIAL_PREFIX = "SIT"
HARDWARE_TYPES = ("LAP", "PHO", "PER", "MON")
SERIAL_DIGITS = 6
SERIAL_MIN = 1
SERIAL_MAX = 999_999

# Inclusive batch to print this run (must be within SERIAL_MIN..SERIAL_MAX).
GENERATE_TYPES = HARDWARE_TYPES
GENERATE_START = 1
GENERATE_END = 48

# Split large batches so each PDF stays printable.
MAX_PAGES_PER_PDF = 50

# --- Sticker geometry (centimetres) ----------------------------------------
STICKER_WIDTH_CM = 4.0
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
SERIAL_FONT_MAX_PT = 9.0
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
