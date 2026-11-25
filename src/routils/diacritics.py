"""Helpers for Romanian diacritics.

* ``fix_mojibake`` repairs text that was UTF-8 but got decoded as Latin-1/CP1252
  (``"BucureÈ™ti"`` -> ``"București"``).
* ``normalize_diacritics`` replaces the legacy cedilla letters ş ţ Ş Ţ with the
  correct comma-below letters ș ț Ș Ț.
* ``strip_diacritics`` removes all diacritics (``"Țară"`` -> ``"Tara"``), useful
  for slugs, file names and systems that only accept ASCII.
"""

import unicodedata

_CEDILLA_TO_COMMA = str.maketrans({
    "ş": "ș",  # ş -> ș
    "Ş": "Ș",  # Ş -> Ș
    "ţ": "ț",  # ţ -> ț
    "Ţ": "Ț",  # Ţ -> Ț
})


def normalize_diacritics(text: str) -> str:
    """Replace cedilla ş/ţ (and capitals) with comma-below ș/ț."""
    return text.translate(_CEDILLA_TO_COMMA)


def strip_diacritics(text: str) -> str:
    """Remove diacritics, keeping the base letters."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def fix_mojibake(text: str, max_rounds: int = 3) -> str:
    """Undo UTF-8 text that was wrongly decoded as CP1252 or Latin-1.

    Repeats up to ``max_rounds`` times for double-encoded text. Text that does
    not look like mojibake is returned unchanged.
    """
    for _ in range(max_rounds):
        fixed = None
        for codec in ("cp1252", "latin-1"):
            try:
                fixed = text.encode(codec).decode("utf-8")
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
        if fixed is None or fixed == text:
            return text
        text = fixed
    return text
