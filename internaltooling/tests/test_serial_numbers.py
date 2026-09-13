from pathlib import Path

import pytest

from internaltooling.serial_numbers.layout import build_grid
from internaltooling.serial_numbers.pdf import generate_sticker_pdfs
from internaltooling.serial_numbers.serials import format_serial, iter_serials


def test_format_serial_uses_prefix_type_and_six_digits() -> None:
    assert format_serial("LAP", 1) == "SIT-LAP-000001"
    assert format_serial("PHO", 42) == "SIT-PHO-000042"
    assert format_serial("PER", 999_999) == "SIT-PER-999999"
    assert format_serial("MON", 12) == "SIT-MON-000012"


def test_format_serial_rejects_unknown_type() -> None:
    with pytest.raises(ValueError, match="Unknown hardware type"):
        format_serial("USB", 1)


def test_format_serial_rejects_out_of_range() -> None:
    with pytest.raises(ValueError, match="outside"):
        format_serial("LAP", 0)
    with pytest.raises(ValueError, match="outside"):
        format_serial("LAP", 1_000_000)


def test_iter_serials_is_inclusive() -> None:
    pairs = list(iter_serials("LAP", 1, 3))
    assert [serial for _number, serial in pairs] == [
        "SIT-LAP-000001",
        "SIT-LAP-000002",
        "SIT-LAP-000003",
    ]


def test_default_sticker_grid_fits_a4() -> None:
    grid = build_grid()
    assert grid.cols == 4
    assert grid.rows == 12
    assert grid.stickers_per_page == 48
    x, y = grid.sticker_origin(0)
    assert x == pytest.approx(grid.offset_x_mm)
    assert y == pytest.approx(
        grid.offset_y_mm + (grid.rows - 1) * (grid.sticker_height_mm + grid.gap_mm)
    )


def test_generate_sticker_pdfs_writes_pdf(tmp_path: Path) -> None:
    paths = generate_sticker_pdfs(
        hardware_types=("LAP",),
        start=1,
        end=2,
        output_dir=tmp_path,
    )
    assert len(paths) == 1
    assert paths[0].name == "SIT-LAP-000001-000002.pdf"
    data = paths[0].read_bytes()
    assert data.startswith(b"%PDF")
    assert len(data) > 1000
