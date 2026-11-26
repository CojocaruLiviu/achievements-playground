# routils

Small, dependency-free Python utilities for Romanian and Moldovan data.

## Planned

- [x] IDNP (Moldova) validation: `routils.idnp.is_valid_idnp`
- [x] CNP (Romania) validation: `routils.cnp.is_valid_cnp`, `cnp_birth_date`
- [x] IBAN validation for MD and RO accounts: `routils.iban.is_valid_iban`, `format_iban`, `iban_bank_code`
- [x] Numbers to words in Romanian: `routils.numbers.number_to_words` (with gender agreement), `needs_de`
- [x] Diacritics: `routils.diacritics.fix_mojibake`, `normalize_diacritics` (ş/ţ -> ș/ț), `strip_diacritics`

## Development

```
python -m venv .venv
.venv/Scripts/python -m pip install pytest   # Windows
.venv/Scripts/python -m pytest
```

## License

MIT
