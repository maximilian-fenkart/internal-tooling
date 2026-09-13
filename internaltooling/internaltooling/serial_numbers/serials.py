"""Serial number formatting for Sodex IT hardware."""

from . import config


def format_serial(hardware_type: str, number: int) -> str:
    """Return a serial such as ``SIT-LAP-000001``."""
    if hardware_type not in config.HARDWARE_TYPES:
        allowed = ", ".join(config.HARDWARE_TYPES)
        raise ValueError(f"Unknown hardware type {hardware_type!r}. Expected one of: {allowed}")
    if number < config.SERIAL_MIN or number > config.SERIAL_MAX:
        raise ValueError(
            f"Serial number {number} is outside {config.SERIAL_MIN:0{config.SERIAL_DIGITS}d}"
            f"-{config.SERIAL_MAX:0{config.SERIAL_DIGITS}d}"
        )
    return (
        f"{config.SERIAL_PREFIX}-{hardware_type}-"
        f"{number:0{config.SERIAL_DIGITS}d}"
    )


def iter_serials(hardware_type: str, start: int, end: int):
    """Yield ``(number, serial)`` pairs from ``start`` to ``end`` inclusive."""
    if start > end:
        raise ValueError(f"Start {start} is greater than end {end}")
    for number in range(start, end + 1):
        yield number, format_serial(hardware_type, number)
