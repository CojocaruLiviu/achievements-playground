import pytest

from routils.idnp import idnp_check_digit, is_valid_idnp


@pytest.mark.parametrize("value", ["2002000000008", "0987654321014", "2003040506073", "2002 0000 0000 8"])
def test_valid(value):
    assert is_valid_idnp(value)


@pytest.mark.parametrize(
    "value",
    ["2002000000009", "200200000000", "20020000000080", "200200000000A", "", None, 2002000000008],
)
def test_invalid(value):
    assert not is_valid_idnp(value)


def test_check_digit():
    # 2*7 + 2*7 = 28 -> 8
    assert idnp_check_digit("200200000000") == 8


def test_check_digit_rejects_bad_input():
    with pytest.raises(ValueError):
        idnp_check_digit("123")
