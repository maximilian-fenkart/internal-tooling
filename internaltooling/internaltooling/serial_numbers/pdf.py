"""Render serial-number stickers onto A4 PDF sheets."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import qrcode
from reportlab.graphics import renderPDF
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

from . import config
from .layout import StickerGrid, build_grid
from .serials import iter_serials

_SERIAL_FONT = "Helvetica-Bold"


def generate_sticker_pdfs(
    *,
    hardware_types: tuple[str, ...] | None = None,
    start: int | None = None,
    end: int | None = None,
    output_dir: Path | None = None,
) -> list[Path]:
    """Write A4 PDF sheets of stickers and return the created file paths."""
    hardware_types = config.GENERATE_TYPES if hardware_types is None else hardware_types
    start = config.GENERATE_START if start is None else start
    end = config.GENERATE_END if end is None else end
    output = Path(output_dir) if output_dir is not None else config.OUTPUT_DIR
    output.mkdir(parents=True, exist_ok=True)
    grid = build_grid()
    serials_per_pdf = grid.stickers_per_page * config.MAX_PAGES_PER_PDF
    logo = _load_logo()
    written: list[Path] = []
    for hardware_type in hardware_types:
        chunk_start = start
        while chunk_start <= end:
            chunk_end = min(chunk_start + serials_per_pdf - 1, end)
            path = output / (
                f"{config.SERIAL_PREFIX}-{hardware_type}-"
                f"{chunk_start:0{config.SERIAL_DIGITS}d}-"
                f"{chunk_end:0{config.SERIAL_DIGITS}d}.pdf"
            )
            _write_pdf(path, hardware_type, chunk_start, chunk_end, grid, logo)
            written.append(path)
            chunk_start = chunk_end + 1
    return written


def _write_pdf(
    path: Path,
    hardware_type: str,
    start: int,
    end: int,
    grid: StickerGrid,
    logo,
) -> None:
    c = canvas.Canvas(
        str(path),
        pagesize=(config.PAGE_WIDTH_MM * mm, config.PAGE_HEIGHT_MM * mm),
    )
    per_page = grid.stickers_per_page
    for index, (_number, serial) in enumerate(iter_serials(hardware_type, start, end)):
        slot = index % per_page
        if slot == 0:
            if index:
                c.showPage()
            _paint_page_background(c)
        x, y = grid.sticker_origin(slot)
        _draw_sticker(c, x, y, grid.sticker_width_mm, grid.sticker_height_mm, serial, logo)
    c.save()


def _paint_page_background(c: canvas.Canvas) -> None:
    c.setFillColor(_color(config.PAGE_BACKGROUND))
    c.rect(
        0,
        0,
        config.PAGE_WIDTH_MM * mm,
        config.PAGE_HEIGHT_MM * mm,
        fill=1,
        stroke=0,
    )


def _draw_sticker(
    c: canvas.Canvas,
    x_mm: float,
    y_mm: float,
    width_mm: float,
    height_mm: float,
    serial: str,
    logo,
) -> None:
    c.setFillColor(_color(config.STICKER_BACKGROUND))
    c.setStrokeColor(_color(config.STICKER_BORDER_COLOR))
    c.setLineWidth(config.STICKER_BORDER_MM * mm)
    c.roundRect(
        x_mm * mm,
        y_mm * mm,
        width_mm * mm,
        height_mm * mm,
        _radius(config.STICKER_CORNER_RADIUS_MM, width_mm, height_mm),
        fill=1,
        stroke=1,
    )

    pad = config.STICKER_PADDING_MM
    inner_h = height_mm - 2 * pad
    qr_size = inner_h
    qr_x = x_mm + width_mm - pad - qr_size
    qr_y = y_mm + pad
    _draw_qr(c, serial, qr_x, qr_y, qr_size)

    left_x = x_mm + pad
    left_w = max(qr_x - config.STICKER_INNER_GAP_MM - left_x, 1.0)
    logo_h = min(inner_h * 0.45, left_w / _logo_aspect(logo))
    logo_w = logo_h * _logo_aspect(logo)
    text_size = _serial_font_size(serial, left_w)
    text_h = text_size * 0.352778  # pt to mm
    stack_h = logo_h + 0.8 + text_h
    stack_y = y_mm + pad + max((inner_h - stack_h) / 2.0, 0.0)
    center_x = left_x + left_w / 2.0

    _draw_logo(
        c,
        logo,
        center_x - logo_w / 2.0,
        stack_y + text_h + 0.8,
        logo_w,
        logo_h,
    )
    c.setFillColor(_color(config.SERIAL_TEXT_COLOR))
    c.setFont(_SERIAL_FONT, text_size)
    c.drawCentredString(center_x * mm, stack_y * mm, serial)


def _draw_qr(c: canvas.Canvas, serial: str, x_mm: float, y_mm: float, size_mm: float) -> None:
    qr = qrcode.QRCode(border=config.QR_BORDER_MODULES, box_size=8)
    qr.add_data(serial)
    qr.make(fit=True)
    image = qr.make_image(fill_color=config.QR_FILL, back_color=config.QR_BACKGROUND).convert(
        "RGB"
    )
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(
        x_mm * mm,
        y_mm * mm,
        size_mm * mm,
        size_mm * mm,
        _radius(config.QR_CORNER_RADIUS_MM, size_mm, size_mm),
    )
    c.clipPath(clip, stroke=0)
    c.drawImage(
        _image_reader(buffer),
        x_mm * mm,
        y_mm * mm,
        width=size_mm * mm,
        height=size_mm * mm,
        mask="auto",
    )
    c.restoreState()


def _image_reader(buffer: BytesIO):
    from reportlab.lib.utils import ImageReader

    return ImageReader(buffer)


def _load_logo():
    if not config.LOGO_PATH.is_file():
        raise FileNotFoundError(f"Sodex logo not found: {config.LOGO_PATH}")
    drawing = svg2rlg(str(config.LOGO_PATH))
    if drawing is None:
        raise RuntimeError(f"Could not parse logo SVG: {config.LOGO_PATH}")
    return drawing


def _logo_aspect(logo) -> float:
    if not logo.width or not logo.height:
        return 3.8
    return logo.width / logo.height


def _draw_logo(c: canvas.Canvas, logo, x_mm: float, y_mm: float, width_mm: float, height_mm: float) -> None:
    if not logo.width or not logo.height:
        return
    scale_x = (width_mm * mm) / logo.width
    scale_y = (height_mm * mm) / logo.height
    c.saveState()
    c.translate(x_mm * mm, y_mm * mm)
    c.scale(scale_x, scale_y)
    renderPDF.draw(logo, c, 0, 0)
    c.restoreState()


def _serial_font_size(serial: str, max_width_mm: float) -> float:
    max_width_pt = max_width_mm * mm
    size = config.SERIAL_FONT_MAX_PT
    while size > 4.0 and stringWidth(serial, _SERIAL_FONT, size) > max_width_pt:
        size -= 0.25
    return size


def _radius(radius_mm: float, width_mm: float, height_mm: float) -> float:
    """Clamp a corner radius so it never exceeds half the shorter side."""
    return min(radius_mm, min(width_mm, height_mm) / 2.0) * mm


def _color(value: str) -> Color:
    return HexColor(value)
