"""Validation of the Moldovan personal identification number (IDNP).

An IDNP has 13 digits. The last digit is a check digit: the first 12 digits
are multiplied by the repeating weights 7, 3, 1, summed, and the check digit
is that sum modulo 10.
"""

_WEIGHTS = (7, 3, 1)


def idnp_check_digit(first12: str) -> int:
    """Return the check digit for the first 12 digits of an IDNP."""
    if len(first12) != 12 or not first12.isdigit():
        raise ValueError("expected exactly 12 digits")
    return sum(int(d) * _WEIGHTS[i % 3] for i, d in enumerate(first12)) % 10


def is_valid_idnp(value: str) -> bool:
    """Return True if ``value`` is a well-formed IDNP with a correct check digit.

    Spaces are ignored, so ``"2002 0000 0000 9"`` is accepted.
    """
    if not isinstance(value, str):
        return False
    digits = value.replace(" ", "")
    if len(digits) != 13 or not digits.isdigit():
        return False
    return idnp_check_digit(digits[:12]) == int(digits[12])
