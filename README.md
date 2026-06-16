# Password Generator (Windows-focused)

A lightweight password generator and optional storage utilities, tuned for use on Windows.

What is in this workspace
- `GEN_G2.py` — the interactive password generator the project currently uses.
- `plaintext_store.py` — helper to append password entries to a CSV file (default on Windows: %APPDATA%\PasswordGenerator\stored_passwords.csv).
- `vault.py`, `custom_vault.py` — legacy encrypted-vault implementations (left in the repo for later development). If you don't need them they can be removed or moved to a `legacy_vault/` folder.
- `requirements.txt` — contains `cryptography` (only required if you want to use the vault modules).

Quick start (PowerShell)

1) Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies only if you plan to use encrypted vaults (optional):

```powershell
pip install -r requirements.txt
```

3) Run the generator:

```powershell
python .\GEN_G2.py
```

Where plaintext CSVs are stored (default)
- The CSV export helper writes to: `%APPDATA%\PasswordGenerator\stored_passwords.csv` by default on Windows.
- When you choose to save a generated or supplied password the script will ask for a filename; pressing Enter uses the default above.
- You can open the CSV using Notepad, Excel, or PowerShell:

```powershell
notepad $env:APPDATA\PasswordGenerator\stored_passwords.csv
Import-Csv $env:APPDATA\PasswordGenerator\stored_passwords.csv | Format-Table -AutoSize
```

Security notes
- The CSV is stored in plaintext. Do NOT keep real production passwords there unless you understand the risk.
- The repo contains `vault.py` and `custom_vault.py` — these implement encrypted storage (Fernet or a demonstrative custom method). They require `cryptography` and are disabled in the generator by default. Use them only if you understand how to manage the master password and dependencies.


