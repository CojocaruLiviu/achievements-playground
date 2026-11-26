"""Moldovan and Romanian phone numbers: normalization to E.164, formatting, mobile check.

Accepted inputs (spaces, dots, dashes and parentheses are ignored):

* international: ``+373 69 123 456``, ``0040 722 123 456``
* national: ``069 123 456`` (Moldova, 0 + 8 digits), ``0722 123 456`` (Romania, 0 + 9 digits)
"""

import re

COUNTRIES = {"MD": ("373", 8), "RO": ("40", 9)}
_MOBILE_PREFIX = {"MD": ("6", "7"), "RO": ("7",)}
_STRIP = re.compile(r"[\s.\-()/]")


def parse_phone(value: str):
    """Return ``(country, national_number)`` or ``None`` if ``value`` is not an MD/RO number."""
    if not isinstance(value, str):
        return None
    v = _STRIP.sub("", value)
    if v.startswith("00"):
        v = "+" + v[2:]
    if v.startswith("+"):
        rest = v[1:]
        if not rest.isdigit():
            return None
        for country, (code, length) in COUNTRIES.items():
            if rest.startswith(code) and len(rest) == len(code) + length:
                national = rest[len(code):]
                return (country, national) if national[0] != "0" else None
        return None
    if not v.isdigit() or not v.startswith("0") or v.startswith("00"):
        return None
    national = v[1:]
    for country, (_, length) in COUNTRIES.items():
        if len(national) == length:
            return country, national
    return None


def normalize_phone(value: str):
    """Return the number in E.164 form (``+37369123456``) or ``None`` if it is not valid."""
    parsed = parse_phone(value)
    if not parsed:
        return None
    country, national = parsed
    return f"+{COUNTRIES[country][0]}{national}"


def format_phone(value: str):
    """Return a readable international form: ``+373 69 123 456`` / ``+40 722 123 456``."""
    parsed = parse_phone(value)
    if not parsed:
        return None
    country, n = parsed
    code = COUNTRIES[country][0]
    if country == "MD":
        return f"+{code} {n[:2]} {n[2:5]} {n[5:]}"
    return f"+{code} {n[:3]} {n[3:6]} {n[6:]}"


def is_mobile(value: str) -> bool:
    """Return True for Moldovan (6x, 7x) and Romanian (7x) mobile numbers."""
    parsed = parse_phone(value)
    return bool(parsed) and parsed[1].startswith(_MOBILE_PREFIX[parsed[0]])
