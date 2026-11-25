import datetime as dt

import pytest

from routils.cnp import cnp_birth_date, cnp_check_digit, is_valid_cnp


@pytest.mark.parametrize("value", ["1800101221144", "2960229400011", "5011231700121", "7002297000158"])
def test_valid(value):
    assert is_valid_cnp(value)


@pytest.mark.parametrize(
    "value",
    [
        "1800101221145",  # wrong check digit
        "1970229400011",  # 29 Feb 1997 does not exist
        "1801301221144",  # month 13
        "1800101991144",  # county 99
        "0800101221144",  # sex digit 0
        "180010122114",
        None,
    ],
)
def test_invalid(value):
    assert not is_valid_cnp(value)


def test_check_digit_remainder_ten_becomes_one():
    # find a prefix whose weighted sum is 10 mod 11 and make sure it maps to 1
    prefix = next(f"1800101{n:05d}" for n in range(100000)
                  if sum(int(d) * int(w) for d, w in zip(f"1800101{n:05d}", "279146358279")) % 11 == 10)
    assert cnp_check_digit(prefix) == 1


def test_birth_date():
    assert cnp_birth_date("1800101221144") == dt.date(1980, 1, 1)
    assert cnp_birth_date("5011231700121") == dt.date(2001, 12, 31)
    assert cnp_birth_date("7002297000158") is None
