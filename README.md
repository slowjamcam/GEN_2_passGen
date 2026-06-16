# Password Generator (Windows-focused)

A lightweight, easy-to-use password generator and optional storage utilities, optimized for Windows users. Generate secure passwords with customizable difficulty levels, validate user-supplied passwords, and optionally save them to a local CSV file.

## Features

- **Interactive password generation** with Easy, Medium, Hard, and Very Hard difficulty levels
- **Custom password validation** — supply your own password and validate it meets security requirements
- **Local CSV storage** — save passwords with titles and notes to `%APPDATA%\PasswordGenerator\stored_passwords.csv`
- **No external dependencies** for basic usage (cryptography is optional and disabled by default)
- **Windows-native** — batch scripts for easy setup and launching

## What's Included

- `GEN_G2.py` — the main interactive password generator
- `plaintext_store.py` — helper to append password entries to a CSV file
- `run.bat` — double-click to run the generator (Windows)
- `setup.bat` — one-click setup to create virtual environment and install dependencies
- `vault.py`, `custom_vault.py` — legacy encrypted-vault implementations (optional, in `legacy_vault/` folder)
- `requirements.txt` — contains `cryptography` (only required if you want to use the vault modules)

## Quick Start (Windows)

### Easiest Way (No PowerShell needed)

1. **Download and Extract** this repository to a folder
2. **Double-click `setup.bat`** to set up the virtual environment and install dependencies
3. **Double-click `run.bat`** to launch the password generator

### Manual Setup (PowerShell)

If you prefer to set up manually:

```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies (optional, only needed for encrypted vault features)
pip install -r requirements.txt

# 3. Run the generator
python .\GEN_G2.py
```

### First-Time Requirements

- **Python 3.7+** installed and added to PATH
  - [Download Python](https://www.python.org/downloads/)
  - **Important**: Check "Add Python to PATH" during installation
- **Command Prompt or PowerShell**
- ~50MB disk space for the virtual environment

## Stored Password Locations

By default, saved passwords are stored in:
```
%APPDATA%\PasswordGenerator\stored_passwords.csv
```

(On most Windows systems, this expands to: `C:\Users\YourUsername\AppData\Roaming\PasswordGenerator\`)

### Opening Saved Passwords

- **Notepad**: `notepad %APPDATA%\PasswordGenerator\stored_passwords.csv`
- **Excel**: Open the file directly
- **PowerShell**:
  ```powershell
  Import-Csv $env:APPDATA\PasswordGenerator\stored_passwords.csv | Format-Table -AutoSize
  ```

When you save a password in the generator, it will ask for a filename. Press Enter to use the default location.

## Security Notes

⚠️ **Important**

- **Plaintext CSV storage**: The default storage saves passwords in plaintext CSV files. This is convenient for temporary use but **NOT SECURE for production passwords**.
- **Do not store real credentials** in the CSV unless you understand the security risks.
- **Windows Event Viewer** may log command line arguments; consider alternative methods for sensitive passwords.

### Encrypted Storage (Advanced)

The repository includes `vault.py` and `custom_vault.py` (in `legacy_vault/`) which provide encrypted storage using:
- **Fernet** (symmetric encryption with `cryptography` library)
- **Custom encryption** (demonstrative purposes)

These are **disabled by default** and require understanding of master password management. Use only if needed.

## Troubleshooting

### "Python is not recognized"
- Python is not installed or not added to PATH
- Solution: [Download Python](https://www.python.org/downloads/) and check "Add Python to PATH" during installation
- Restart your terminal after installing

### `setup.bat` fails with permission errors
- Your antivirus/security software may be blocking file creation
- Solution: Temporarily disable or whitelist the folder, then re-run `setup.bat`

### UTF-8 encoding issues when saving CSV
- Ensure your terminal/PowerShell uses UTF-8 encoding:
  ```powershell
  $OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding
  ```

### Can't access the CSV file after saving
- The file is locked by another application (e.g., Excel)
- Solution: Close other programs accessing the file first

## License

MIT License — see [LICENSE](LICENSE) file for details.

## Contributing

Contributions, issues, and suggestions are welcome! Feel free to open an issue or submit a pull request.
