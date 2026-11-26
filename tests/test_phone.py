import pytest

from routils.phone import format_phone, is_mobile, normalize_phone, parse_phone


@pytest.mark.parametrize(
    "value, e164",
    [
        ("069123456", "+37369123456"),
        ("+373 69 123 456", "+37369123456"),
        ("00373-22-123-456", "+37322123456"),
        ("(022) 12 34 56", "+37322123456"),
        ("0722 123 456", "+40722123456"),
        ("+40 722.123.456", "+40722123456"),
        ("0040212345678", "+40212345678"),
    ],
)
def test_normalize(value, e164):
    assert normalize_phone(value) == e164


@pytest.mark.parametrize(
    "value",
    ["", "123", "69123456", "0691234567890", "+3736912345", "+40072212345", "+44 20 7946 0958", "0069123456", "06912345a", None, 69123456],
)
def test_invalid(value):
    assert normalize_phone(value) is None


def test_parse():
    assert parse_phone("069123456") == ("MD", "69123456")
    assert parse_phone("0722123456") == ("RO", "722123456")


def test_format():
    assert format_phone("069123456") == "+373 69 123 456"
    assert format_phone("0722123456") == "+40 722 123 456"
    assert format_phone("abc") is None


@pytest.mark.parametrize("value, expected", [("069123456", True), ("079123456", True), ("022123456", False), ("0722123456", True), ("0212345678", False), ("x", False)])
def test_is_mobile(value, expected):
    assert is_mobile(value) is expected
