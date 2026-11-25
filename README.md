# routils

Small, dependency-free Python utilities for Romanian and Moldovan data.

## Planned

- [x] IDNP (Moldova) validation: `routils.idnp.is_valid_idnp`
- CNP (Romania) validation
- IBAN validation for MD and RO accounts
- Numbers to words in Romanian (for invoices and contracts)
- Diacritics: fix mojibake, normalize ş/ţ to ș/ț, strip diacritics

## Development

```
python -m venv .venv
.venv/Scripts/python -m pip install pytest   # Windows
.venv/Scripts/python -m pytest
```

## License

MIT
