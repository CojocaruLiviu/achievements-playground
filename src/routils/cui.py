"""Validation of the Romanian company tax code (CUI / CIF).

A CUI has 2 to 10 digits; the last one is a check digit. The other digits are
left-padded with zeros to 9 positions, multiplied by the key ``753217532``,
summed, multiplied by 10 and taken modulo 11 (a result of 10 becomes 0).
VAT payers write it with an ``RO`` prefix (``RO14399840``).
"""

_KEY = "753217532"


def cui_check_digit(body: str) -> int:
    """Return the check digit for a CUI without its last digit (1 to 9 digits)."""
    if not body.isdigit() or not 1 <= len(body) <= 9:
        raise ValueError("expected 1 to 9 digits")
    total = sum(int(d) * int(k) for d, k in zip(body.zfill(9), _KEY)) * 10 % 11
    return 0 if total == 10 else total


def normalize_cui(value: str) -> str:
    """Strip spaces and an optional ``RO`` prefix: ``"RO 1439 9840"`` -> ``"14399840"``."""
    if not isinstance(value, str):
        raise TypeError("expected a string")
    v = value.replace(" ", "").upper()
    return v[2:] if v.startswith("RO") else v


def is_valid_cui(value: str) -> bool:
    """Return True if ``value`` is a well-formed CUI/CIF with a correct check digit.

    Spaces and an ``RO`` prefix are accepted.
    """
    if not isinstance(value, str):
        return False
    digits = normalize_cui(value)
    if not digits.isdigit() or not 2 <= len(digits) <= 10:
        return False
    return cui_check_digit(digits[:-1]) == int(digits[-1])
