import pytest
import os
import string
from project import generate_password, save_password, retrieve_password, list_services, delete_password

# Use a separate test file so we don't touch real passwords
TEST_FILE = "test_passwords.json"

@pytest.fixture(autouse=True)
def use_test_file(monkeypatch):
    """Redirect all file operations to a test file."""
    monkeypatch.setattr("project.PASSWORDS_FILE", TEST_FILE)
    yield
    # Clean up test file after each test
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# --- generate_password tests ---

def test_generate_password_length():
    password = generate_password(16)
    assert len(password) == 16

def test_generate_password_default_length():
    password = generate_password()
    assert len(password) == 16

def test_generate_password_custom_length():
    password = generate_password(32)
    assert len(password) == 32

def test_generate_password_is_string():
    assert isinstance(generate_password(), str)

def test_generate_password_has_variety():
    password = generate_password(32)
    has_letter = any(c in string.ascii_letters for c in password)
    has_digit = any(c in string.digits for c in password)
    assert has_letter and has_digit

def test_generate_passwords_are_unique():
    p1 = generate_password()
    p2 = generate_password()
    assert p1 != p2


# --- save and retrieve tests ---

def test_save_and_retrieve():
    save_password("gmail", "mypassword123")
    assert retrieve_password("gmail") == "mypassword123"

def test_retrieve_nonexistent():
    assert retrieve_password("doesnotexist") is None

def test_save_overwrites():
    save_password("gmail", "oldpassword")
    save_password("gmail", "newpassword")
    assert retrieve_password("gmail") == "newpassword"


# --- list_services tests ---

def test_list_services_empty():
    assert list_services() == []

def test_list_services_after_save():
    save_password("gmail", "pass1")
    save_password("netflix", "pass2")
    services = list_services()
    assert "gmail" in services
    assert "netflix" in services

def test_list_services_count():
    save_password("gmail", "pass1")
    save_password("netflix", "pass2")
    assert len(list_services()) == 2


# --- delete tests ---

def test_delete_existing():
    save_password("gmail", "pass1")
    assert delete_password("gmail") == True
    assert retrieve_password("gmail") is None

def test_delete_nonexistent():
    assert delete_password("doesnotexist") == False

def test_delete_removes_from_list():
    save_password("gmail", "pass1")
    save_password("netflix", "pass2")
    delete_password("gmail")
    assert "gmail" not in list_services()
    assert "netflix" in list_services()
