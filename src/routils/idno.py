"""Validation of the Moldovan state identification number of legal entities (IDNO).

An IDNO has 13 digits and starts with ``1`` (IDNPs of natural persons start
with ``0`` or ``2``). Its last digit is checked with the same 7-3-1 weights as
the IDNP, see :mod:`routils.idnp`.
"""

from routils.idnp import idnp_check_digit, is_valid_idnp


def is_valid_idno(value: str) -> bool:
    """Return True if ``value`` is a well-formed IDNO with a correct check digit.

    Spaces are ignored.
    """
    if not isinstance(value, str):
        return False
    digits = value.replace(" ", "")
    if len(digits) != 13 or not digits.isdigit() or digits[0] != "1":
        return False
    return idnp_check_digit(digits[:12]) == int(digits[12])


def md_code_kind(value: str):
    """Classify a Moldovan 13-digit code: ``"IDNO"`` (company), ``"IDNP"`` (person) or ``None``."""
    if is_valid_idno(value):
        return "IDNO"
    if is_valid_idnp(value):
        return "IDNP"
    return None
