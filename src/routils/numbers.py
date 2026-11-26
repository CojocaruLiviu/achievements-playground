"""Romanian numbers in words, as written on invoices, contracts and cheques.

Romanian number words agree in gender with the noun they count:

* masculine: ``doi lei``, ``douăzeci și unu de lei``
* feminine: ``două mii``, ``douăzeci și una de mii``
* neuter: ``două milioane``, ``douăzeci și unu de milioane``

Counts whose last two digits are 00 or 20..99 take the preposition ``de``
before the noun (``douăzeci de lei``, ``o sută de lei``); 1..19 do not
(``nouăsprezece lei``, ``o sută cinci lei``). :func:`needs_de` exposes that rule.
"""

_UNITS = ["zero", "unu", "doi", "trei", "patru", "cinci", "șase", "șapte", "opt", "nouă"]
_TEENS = ["zece", "unsprezece", "doisprezece", "treisprezece", "paisprezece", "cincisprezece",
          "șaisprezece", "șaptesprezece", "optsprezece", "nouăsprezece"]
_TENS = ["", "", "douăzeci", "treizeci", "patruzeci", "cincizeci", "șaizeci", "șaptezeci", "optzeci", "nouăzeci"]

# (value, singular, plural, gender of the noun)
_SCALES = [
    (10**9, "un miliard", "miliarde", "n"),
    (10**6, "un milion", "milioane", "n"),
    (10**3, "o mie", "mii", "f"),
]

GENDERS = ("m", "f", "n")


def needs_de(n: int) -> bool:
    """Return True if a count of ``n`` takes ``de`` before the noun (``20 de lei``)."""
    r = abs(n) % 100
    return n != 0 and (r == 0 or r >= 20)


def _unit(d: int, gender: str) -> str:
    if d == 1:
        return "una" if gender == "f" else "unu"
    if d == 2:
        return "doi" if gender == "m" else "două"
    return _UNITS[d]


def _below_100(n: int, gender: str) -> str:
    if n < 10:
        return _unit(n, gender)
    if n < 20:
        if n == 12 and gender != "m":
            return "douăsprezece"
        return _TEENS[n - 10]
    tens, unit = divmod(n, 10)
    if unit == 0:
        return _TENS[tens]
    return f"{_TENS[tens]} și {_unit(unit, gender)}"


def _below_1000(n: int, gender: str) -> str:
    hundreds, rest = divmod(n, 100)
    parts = []
    if hundreds == 1:
        parts.append("o sută")
    elif hundreds > 1:
        parts.append(f"{_unit(hundreds, 'f')} sute")
    if rest:
        parts.append(_below_100(rest, gender))
    return " ".join(parts)


def _scaled(count: int, singular: str, plural: str, gender: str) -> str:
    if count == 1:
        return singular
    words = _below_1000(count, gender)
    return f"{words} de {plural}" if needs_de(count) else f"{words} {plural}"


def number_to_words(n: int, gender: str = "m") -> str:
    """Spell the integer ``n`` in Romanian.

    ``gender`` is the gender of the counted noun: ``"m"`` (default), ``"f"`` or ``"n"``.

    >>> number_to_words(1234)
    'o mie două sute treizeci și patru'
    >>> number_to_words(22, gender="f")
    'douăzeci și două'
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("expected an int")
    if gender not in GENDERS:
        raise ValueError(f"gender must be one of {GENDERS}")
    if n < 0:
        return "minus " + number_to_words(-n, gender)
    if n >= 10**12:
        raise ValueError("numbers of 10^12 or more are not supported")
    if n == 0:
        return "zero"
    parts = []
    for value, singular, plural, noun_gender in _SCALES:
        count, n = divmod(n, value)
        if count:
            parts.append(_scaled(count, singular, plural, noun_gender))
    if n:
        parts.append(_below_1000(n, gender))
    return " ".join(parts)
