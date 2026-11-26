from decimal import Decimal

import pytest

from routils.money import amount_to_words, count_noun


@pytest.mark.parametrize(
    "amount, words",
    [
        (0, "zero lei"),
        (1, "un leu"),
        (2, "doi lei"),
        (19, "nouăsprezece lei"),
        (20, "douăzeci de lei"),
        (101, "o sută unu lei"),
        ("123.50", "o sută douăzeci și trei de lei și cincizeci de bani"),
        (Decimal("2.01"), "doi lei și un ban"),
        ("0.05", "cinci bani"),
        (1000000, "un milion de lei"),
        ("1250.99", "o mie două sute cincizeci de lei și nouăzeci și nouă de bani"),
    ],
)
def test_ron(amount, words):
    assert amount_to_words(amount) == words


def test_mdl_same_nouns_as_ron():
    assert amount_to_words(22, "MDL") == "douăzeci și doi de lei"


@pytest.mark.parametrize(
    "amount, words",
    [(1, "un euro"), (99, "nouăzeci și nouă de euro"), ("10.01", "zece euro și un eurocent"), ("3.02", "trei euro și doi eurocenți")],
)
def test_eur(amount, words):
    assert amount_to_words(amount, "eur") == words


def test_rounding_and_float():
    assert amount_to_words(0.1 + 0.2) == "treizeci de bani"
    assert amount_to_words("4.999") == "cinci lei"


def test_show_zero_cents():
    assert amount_to_words(7, show_zero_cents=True) == "șapte lei și zero bani"


def test_negative():
    assert amount_to_words(-3) == "minus trei lei"


def test_count_noun_feminine():
    assert count_noun(1, "carte", "cărți", "f") == "o carte"
    assert count_noun(2, "carte", "cărți", "f") == "două cărți"


def test_errors():
    with pytest.raises(ValueError):
        amount_to_words(1, "USD")
    with pytest.raises(TypeError):
        amount_to_words(True)
