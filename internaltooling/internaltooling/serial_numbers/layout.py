"""A4 grid layout for serial stickers."""

from dataclasses import dataclass

from . import config


@dataclass(frozen=True)
class StickerGrid:
    cols: int
    rows: int
    sticker_width_mm: float
    sticker_height_mm: float
    gap_mm: float
    offset_x_mm: float
    offset_y_mm: float

    @property
    def stickers_per_page(self) -> int:
        return self.cols * self.rows

    def sticker_origin(self, index_on_page: int) -> tuple[float, float]:
        """Bottom-left corner of a sticker in millimetres (PDF coordinates)."""
        col = index_on_page % self.cols
        row_from_top = index_on_page // self.cols
        x = self.offset_x_mm + col * (self.sticker_width_mm + self.gap_mm)
        y = self.offset_y_mm + (self.rows - 1 - row_from_top) * (
            self.sticker_height_mm + self.gap_mm
        )
        return x, y


def build_grid(
    *,
    sticker_width_cm: float | None = None,
    sticker_height_cm: float | None = None,
    page_width_mm: float | None = None,
    page_height_mm: float | None = None,
    margin_mm: float | None = None,
    gap_mm: float | None = None,
) -> StickerGrid:
    sticker_width_cm = config.STICKER_WIDTH_CM if sticker_width_cm is None else sticker_width_cm
    sticker_height_cm = config.STICKER_HEIGHT_CM if sticker_height_cm is None else sticker_height_cm
    page_width_mm = config.PAGE_WIDTH_MM if page_width_mm is None else page_width_mm
    page_height_mm = config.PAGE_HEIGHT_MM if page_height_mm is None else page_height_mm
    margin_mm = config.PAGE_MARGIN_MM if margin_mm is None else margin_mm
    gap_mm = config.STICKER_GAP_MM if gap_mm is None else gap_mm
    sticker_w = sticker_width_cm * 10.0
    sticker_h = sticker_height_cm * 10.0
    usable_w = page_width_mm - 2 * margin_mm
    usable_h = page_height_mm - 2 * margin_mm
    cols = int((usable_w + gap_mm) // (sticker_w + gap_mm))
    rows = int((usable_h + gap_mm) // (sticker_h + gap_mm))
    if cols < 1 or rows < 1:
        raise ValueError("Sticker size does not fit on the page with the current margins")

    grid_w = cols * sticker_w + (cols - 1) * gap_mm
    grid_h = rows * sticker_h + (rows - 1) * gap_mm
    offset_x = (page_width_mm - grid_w) / 2.0
    offset_y = (page_height_mm - grid_h) / 2.0
    return StickerGrid(
        cols=cols,
        rows=rows,
        sticker_width_mm=sticker_w,
        sticker_height_mm=sticker_h,
        gap_mm=gap_mm,
        offset_x_mm=offset_x,
        offset_y_mm=offset_y,
    )
