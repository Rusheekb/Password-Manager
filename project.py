import json
import os
import random
import string
from cryptography.fernet import Fernet

PASSWORDS_FILE = "passwords.json"
KEY_FILE = "secret.key"


def main():
    load_key()
    while True:
        print("\n=== Password Manager ===")
        print("1. Generate & save a password")
        print("2. Retrieve a password")
        print("3. List all services")
        print("4. Delete a password")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            service = input("Service name (e.g. gmail): ").strip().lower()
            password = generate_password()
            save_password(service, password)
            print(f"Password saved for {service}: {password}")
        elif choice == "2":
            service = input("Service name: ").strip().lower()
            password = retrieve_password(service)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print(f"No password found for {service}")
        elif choice == "3":
            services = list_services()
            if services:
                print("\nSaved services:")
                for s in services:
                    print(f"  - {s}")
            else:
                print("No passwords saved yet.")
        elif choice == "4":
            service = input("Service name to delete: ").strip().lower()
            if delete_password(service):
                print(f"Deleted password for {service}")
            else:
                print(f"No password found for {service}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def generate_password(length=16):
    """Generate a strong random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


def load_key():
    """Load or create an encryption key."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return f.read()


def get_fernet():
    """Return a Fernet instance using the stored key."""
    key = load_key()
    return Fernet(key)


def save_password(service, password):
    """Encrypt and save a password for a service."""
    f = get_fernet()
    encrypted = f.encrypt(password.encode()).decode()
    passwords = load_passwords()
    passwords[service] = encrypted
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file)


def retrieve_password(service):
    """Retrieve and decrypt a password for a service."""
    f = get_fernet()
    passwords = load_passwords()
    if service in passwords:
        return f.decrypt(passwords[service].encode()).decode()
    return None


def list_services():
    """Return a list of all saved service names."""
    return list(load_passwords().keys())


def delete_password(service):
    """Delete a password for a service. Returns True if deleted, False if not found."""
    passwords = load_passwords()
    if service in passwords:
        del passwords[service]
        with open(PASSWORDS_FILE, "w") as file:
            json.dump(passwords, file)
        return True
    return False


def load_passwords():
    """Load passwords from file."""
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(PASSWORDS_FILE, "r") as file:
        return json.load(file)


if __name__ == "__main__":
    main()
