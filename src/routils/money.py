"""Amounts of money in Romanian words (``o sută douăzeci de lei și cincizeci de bani``).

Supported currencies: ``RON`` and ``MDL`` (lei / bani) and ``EUR`` (euro / eurocenți).
"""

from decimal import ROUND_HALF_UP, Decimal

from routils.numbers import needs_de, number_to_words

# currency -> ((singular, plural, gender) for units, (singular, plural, gender) for cents)
CURRENCIES = {
    "RON": (("leu", "lei", "m"), ("ban", "bani", "m")),
    "MDL": (("leu", "lei", "m"), ("ban", "bani", "m")),
    "EUR": (("euro", "euro", "m"), ("eurocent", "eurocenți", "m")),
}


def count_noun(n: int, singular: str, plural: str, gender: str = "m") -> str:
    """Return ``n`` followed by the correctly inflected noun.

    >>> count_noun(1, "leu", "lei")
    'un leu'
    >>> count_noun(20, "leu", "lei")
    'douăzeci de lei'
    """
    if n == 1:
        return ("o " if gender == "f" else "un ") + singular
    words = number_to_words(n, gender)
    return f"{words} de {plural}" if needs_de(n) else f"{words} {plural}"


def amount_to_words(amount, currency: str = "RON", show_zero_cents: bool = False) -> str:
    """Spell a money amount in Romanian.

    ``amount`` may be an int, a :class:`~decimal.Decimal` or a numeric string;
    it is rounded to two decimals. Floats are accepted but converted through
    ``str`` to avoid binary rounding surprises.

    >>> amount_to_words("123.50")
    'o sută douăzeci și trei de lei și cincizeci de bani'
    >>> amount_to_words(1, "EUR")
    'un euro'
    """
    try:
        units_noun, cents_noun = CURRENCIES[currency.upper()]
    except (KeyError, AttributeError):
        raise ValueError(f"unsupported currency: {currency!r}") from None
    if isinstance(amount, bool):
        raise TypeError("expected a number")
    value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if value < 0:
        return "minus " + amount_to_words(-value, currency, show_zero_cents)
    units = int(value)
    cents = int((value - units) * 100)
    text = count_noun(units, *units_noun) if units or not cents else ""
    if cents or show_zero_cents:
        cents_text = count_noun(cents, *cents_noun)
        text = f"{text} și {cents_text}" if text else cents_text
    return text
