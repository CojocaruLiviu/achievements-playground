import pytest

from routils.diacritics import fix_mojibake, normalize_diacritics, strip_diacritics


def test_normalize_cedilla():
    assert normalize_diacritics("Bucureşti Ţara") == "București Țara"


def test_normalize_keeps_correct_text():
    assert normalize_diacritics("București, Țară") == "București, Țară"


@pytest.mark.parametrize(
    "src, expected",
    [("Țară", "Tara"), ("Brașov, Iași", "Brasov, Iasi"), ("Chișinău", "Chisinau"), ("abc", "abc")],
)
def test_strip(src, expected):
    assert strip_diacritics(src) == expected


GOOD = ["București", "Chișinău", "Brașov – Sinaia", "Transfăgărășan"]


@pytest.mark.parametrize("good", GOOD)
def test_fix_mojibake_cp1252(good):
    assert fix_mojibake(good.encode("utf-8").decode("cp1252")) == good


@pytest.mark.parametrize("good", GOOD)
def test_fix_mojibake_latin1(good):
    assert fix_mojibake(good.encode("utf-8").decode("latin-1")) == good


@pytest.mark.parametrize("text", ["café", "naïve"])
def test_fix_mojibake_leaves_latin1_words(text):
    assert fix_mojibake(text) == text


def test_fix_mojibake_double_encoded():
    good = "Iași"
    broken = good.encode("utf-8").decode("latin-1").encode("utf-8").decode("latin-1")
    assert fix_mojibake(broken) == good


@pytest.mark.parametrize("text", ["plain ascii", "București", "Ўзбек", ""])
def test_fix_mojibake_leaves_clean_text(text):
    assert fix_mojibake(text) == text
