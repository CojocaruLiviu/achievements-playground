"""IBAN validation with extra checks for Moldovan and Romanian accounts.

The generic check (ISO 13616): move the first four characters to the end,
replace letters with numbers (A=10 ... Z=35) and the result modulo 97 must be 1.
"""

import re

# Lengths for the countries this package focuses on, plus common neighbours.
IBAN_LENGTHS = {
    "MD": 24,
    "RO": 24,
    "UA": 29,
    "BG": 22,
    "HU": 28,
    "DE": 22,
    "IT": 27,
    "FR": 27,
    "PL": 28,
    "TR": 26,
    "GB": 22,
}

_SHAPE = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]+$")


def compact_iban(value: str) -> str:
    """Remove spaces and dashes and uppercase the IBAN."""
    return re.sub(r"[\s-]", "", value).upper()


def format_iban(value: str) -> str:
    """Return the IBAN in groups of four characters, e.g. ``MD24 AG00 ...``."""
    iban = compact_iban(value)
    return " ".join(iban[i:i + 4] for i in range(0, len(iban), 4))


def _mod97(iban: str) -> int:
    rearranged = iban[4:] + iban[:4]
    return int("".join(str(int(ch, 36)) for ch in rearranged)) % 97


def is_valid_iban(value: str) -> bool:
    """Return True if ``value`` is a valid IBAN.

    Countries listed in ``IBAN_LENGTHS`` must also have the right length;
    other countries only get the shape and mod-97 checks.
    """
    if not isinstance(value, str):
        return False
    iban = compact_iban(value)
    if not _SHAPE.match(iban) or not 15 <= len(iban) <= 34:
        return False
    expected = IBAN_LENGTHS.get(iban[:2])
    if expected is not None and len(iban) != expected:
        return False
    return _mod97(iban) == 1


def iban_bank_code(value: str) -> str:
    """Return the bank code for MD and RO IBANs (characters 5-8, e.g. ``AG00``, ``BTRL``)."""
    iban = compact_iban(value)
    if iban[:2] not in ("MD", "RO"):
        raise ValueError("bank code extraction is only supported for MD and RO IBANs")
    return iban[4:8]
