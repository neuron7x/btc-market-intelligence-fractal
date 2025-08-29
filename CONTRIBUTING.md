# Contributing Guidelines

Дякуємо, що хочете зробити внесок у **BTC Market Intelligence Fractal** 🚀

## Як працювати з кодом
- Використовуйте Python ≥ 3.11.
- Усі залежності мають бути встановлені через:
  ```bash
  pip install -r requirements.txt -c constraints.txt
  ```

## Release gating rules
- Усі тесты та snapshot-и мають проходити.
- Файл SBOM (`provenance/sbom.spdx.json`) та `CHECKSUMS.SHA256` повинні існувати.
- Жоден артефакт у `dist/` не може перевищувати 25 MB.
