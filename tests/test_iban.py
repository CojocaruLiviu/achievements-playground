import pytest

from routils.iban import compact_iban, format_iban, iban_bank_code, is_valid_iban

# Example IBANs published in the IBAN registry / by banks for documentation.
VALID = [
    "MD24AG000225100013104168",
    "RO49AAAA1B31007593840000",
    "DE89370400440532013000",
    "GB29NWBK60161331926819",
    "md24 ag00 0225 1000 1310 4168",
]


@pytest.mark.parametrize("value", VALID)
def test_valid(value):
    assert is_valid_iban(value)


@pytest.mark.parametrize(
    "value",
    [
        "MD24AG000225100013104169",  # wrong checksum
        "MD24AG00022510001310416",  # too short for MD
        "RO49AAAA1B310075938400001",  # too long for RO
        "XX",
        "1234AG000225100013104168",
        None,
    ],
)
def test_invalid(value):
    assert not is_valid_iban(value)


def test_compact_and_format():
    assert compact_iban("ro49 aaaa-1b31 0075 9384 0000") == "RO49AAAA1B31007593840000"
    assert format_iban("RO49AAAA1B31007593840000") == "RO49 AAAA 1B31 0075 9384 0000"


def test_bank_code():
    assert iban_bank_code("MD24AG000225100013104168") == "AG00"
    assert iban_bank_code("RO49AAAA1B31007593840000") == "AAAA"
    with pytest.raises(ValueError):
        iban_bank_code("DE89370400440532013000")
