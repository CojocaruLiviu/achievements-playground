import pytest

from routils.cui import cui_check_digit, is_valid_cui, normalize_cui


@pytest.mark.parametrize("value", ["14399840", "RO14399840", "ro 1439 9840", "1590082", "18547290"])
def test_valid(value):
    assert is_valid_cui(value)


@pytest.mark.parametrize("value", ["14399841", "1590083", "1", "12345678901", "RO", "RO12A4", "", None, 14399840])
def test_invalid(value):
    assert not is_valid_cui(value)


def test_check_digit():
    assert cui_check_digit("1439984") == 0
    assert cui_check_digit("159008") == 2


def test_check_digit_rejects_bad_input():
    with pytest.raises(ValueError):
        cui_check_digit("1234567890")
    with pytest.raises(ValueError):
        cui_check_digit("12a")


def test_normalize():
    assert normalize_cui(" RO 14399840 ") == "14399840"
    with pytest.raises(TypeError):
        normalize_cui(14399840)
