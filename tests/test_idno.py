import pytest

from routils.idno import is_valid_idno, md_code_kind


@pytest.mark.parametrize("value", ["1003600000006", "1002600006193", "1014 6000 0000 4"])
def test_valid(value):
    assert is_valid_idno(value)


@pytest.mark.parametrize(
    "value",
    ["1003600000007", "2002000000008", "100360000000", "10036000000060", "100360000000A", "", None, 1003600000006],
)
def test_invalid(value):
    assert not is_valid_idno(value)


@pytest.mark.parametrize(
    "value, kind",
    [("1003600000006", "IDNO"), ("2002000000008", "IDNP"), ("2002000000009", None), ("abc", None)],
)
def test_kind(value, kind):
    assert md_code_kind(value) == kind
