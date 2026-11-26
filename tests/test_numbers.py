import pytest

from routils.numbers import needs_de, number_to_words


@pytest.mark.parametrize(
    "n, words",
    [
        (0, "zero"),
        (1, "unu"),
        (2, "doi"),
        (10, "zece"),
        (11, "unsprezece"),
        (12, "doisprezece"),
        (14, "paisprezece"),
        (16, "șaisprezece"),
        (19, "nouăsprezece"),
        (20, "douăzeci"),
        (21, "douăzeci și unu"),
        (22, "douăzeci și doi"),
        (60, "șaizeci"),
        (99, "nouăzeci și nouă"),
        (100, "o sută"),
        (101, "o sută unu"),
        (200, "două sute"),
        (999, "nouă sute nouăzeci și nouă"),
        (1000, "o mie"),
        (1001, "o mie unu"),
        (1234, "o mie două sute treizeci și patru"),
        (2000, "două mii"),
        (12000, "douăsprezece mii"),
        (20000, "douăzeci de mii"),
        (21000, "douăzeci și una de mii"),
        (100000, "o sută de mii"),
        (1000000, "un milion"),
        (2000000, "două milioane"),
        (21000000, "douăzeci și unu de milioane"),
        (1000000000, "un miliard"),
        (3500000000, "trei miliarde cinci sute de milioane"),
    ],
)
def test_masculine(n, words):
    assert number_to_words(n) == words


@pytest.mark.parametrize("n, words", [(1, "una"), (2, "două"), (12, "douăsprezece"), (22, "douăzeci și două"), (31, "treizeci și una")])
def test_feminine(n, words):
    assert number_to_words(n, gender="f") == words


@pytest.mark.parametrize("n, words", [(1, "unu"), (2, "două"), (21, "douăzeci și unu")])
def test_neuter(n, words):
    assert number_to_words(n, gender="n") == words


def test_negative():
    assert number_to_words(-5) == "minus cinci"


@pytest.mark.parametrize("n, expected", [(0, False), (1, False), (19, False), (20, True), (100, True), (105, False), (120, True), (1000, True)])
def test_needs_de(n, expected):
    assert needs_de(n) is expected


@pytest.mark.parametrize("bad", [1.5, "3", None, True])
def test_rejects_non_int(bad):
    with pytest.raises(TypeError):
        number_to_words(bad)


def test_rejects_bad_gender_and_range():
    with pytest.raises(ValueError):
        number_to_words(3, gender="x")
    with pytest.raises(ValueError):
        number_to_words(10**12)
