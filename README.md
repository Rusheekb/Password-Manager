# Password Manager

A command-line password manager built in Python that generates, stores, and retrieves encrypted passwords.

## Features
- Generate strong random passwords
- Encrypt and store passwords securely using the `cryptography` library
- Retrieve passwords by service name
- List all saved services
- Delete saved passwords

## Usage

```bash
python project.py
```

Follow the on-screen menu to manage your passwords.

## Dependencies

Install with:
```bash
pip install -r requirements.txt
```

## Files
- `project.py` — main program
- `test_project.py` — pytest tests
- `requirements.txt` — dependencies
- `secret.key` — auto-generated encryption key (do not share this)
- `passwords.json` — encrypted password storage (auto-generated)

## Security Note
Never share your `secret.key` file — it is used to encrypt and decrypt your passwords.
