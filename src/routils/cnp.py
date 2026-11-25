"""Validation of the Romanian personal numeric code (CNP).

Layout: S YY MM DD JJ NNN C
  S   sex and century (1/2: 1900s, 3/4: 1800s, 5/6: 2000s, 7/8: residents, 9: foreigners)
  YYMMDD  date of birth
  JJ  county code (01-52, or 70 for registrations without a county)
  NNN serial number
  C   check digit: sum of the first 12 digits times 279146358279, modulo 11 (10 becomes 1)
"""

import datetime as _dt

_WEIGHTS = "279146358279"
_CENTURY = {"1": 1900, "2": 1900, "3": 1800, "4": 1800, "5": 2000, "6": 2000}


def cnp_check_digit(first12: str) -> int:
    """Return the check digit for the first 12 digits of a CNP."""
    if len(first12) != 12 or not first12.isdigit():
        raise ValueError("expected exactly 12 digits")
    rest = sum(int(d) * int(w) for d, w in zip(first12, _WEIGHTS)) % 11
    return 1 if rest == 10 else rest


def cnp_birth_date(value: str):
    """Return the date of birth encoded in a CNP, or None if it cannot be determined.

    For residents and foreigners (S = 7, 8, 9) the century is not encoded, so None is returned.
    """
    century = _CENTURY.get(value[:1])
    if century is None:
        return None
    try:
        return _dt.date(century + int(value[1:3]), int(value[3:5]), int(value[5:7]))
    except ValueError:
        return None


def is_valid_cnp(value: str) -> bool:
    """Return True if ``value`` is a well-formed CNP with a plausible date, county and check digit."""
    if not isinstance(value, str):
        return False
    cnp = value.replace(" ", "")
    if len(cnp) != 13 or not cnp.isdigit() or cnp[0] == "0":
        return False
    if cnp[0] in _CENTURY:
        if cnp_birth_date(cnp) is None:
            return False
    else:
        # century unknown: check month/day against a leap year
        try:
            _dt.date(2000, int(cnp[3:5]), int(cnp[5:7]))
        except ValueError:
            return False
    county = int(cnp[7:9])
    if not (1 <= county <= 52 or county == 70):
        return False
    return cnp_check_digit(cnp[:12]) == int(cnp[12])
