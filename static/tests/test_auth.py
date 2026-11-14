import sys
from pathlib import Path
from app import app, validate_username, validate_email, validate_password
from werkzeug.security import check_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


import database
import pytest


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    test_db = tmp_path / "test_users.db"

    monkeypatch.setattr(database, "DATABASE", str(test_db))

    database.create_table()

    return database


def test_register_user(test_database):
    result = test_database.register_user(
        "testuser", "test@example.com", "Password123!"
    )

    assert result is True


def test_duplicate_username(test_database):
    test_database.register_user(
        "testuser", "test@example.com", "Password123!"
    )

    result = test_database.register_user(
        "testuser", "another@example.com", "Password456!"
    )

    assert result is False


def test_duplicate_email(test_database):
    test_database.register_user(
        "testuser", "test@example.com", "Password123!"
    )

    result = test_database.register_user(
        "anotheruser", "test@example.com", "Password456!"
    )

    assert result is False


def test_successful_login(test_database):
    test_database.register_user(
        "testuser", "test@example.com", "Password123!"
    )

    user = test_database.authenticate_user(
        "testuser", "Password123!"
    )

    assert user is not None


def test_incorrect_password(test_database):
    test_database.register_user(
        "testuser", "test@example.com", "Password123!"
    )

    user = test_database.authenticate_user(
        "testuser", "WrongPassword!"
    )

    assert user is None


def test_password_is_hashed(test_database):
    password = "Password123!"

    test_database.register_user(
        "testuser", "test@example.com", password
    )

    conn = test_database.get_connection()

    user = conn.execute(
        "SELECT password FROM users WHERE username = ?",
        ("testuser",)
    ).fetchone()

    conn.close()

    stored_password = user["password"]

    assert stored_password != password

    assert check_password_hash(stored_password, password)

def test_csrf_protection():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = True

    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "Password123!"
        }
    )

    assert response.status_code == 400

from app import validate_username, validate_email, validate_password


def test_valid_username():
    assert validate_username("john123") is True


def test_invalid_username():
    assert validate_username("jo") is False


def test_valid_email():
    assert validate_email("john@example.com") is True


def test_invalid_email():
    assert validate_email("johnexample.com") is False


def test_valid_password():
    assert validate_password("Password123") is True


def test_invalid_password():
    assert validate_password("password") is False

def test_password_hashes_are_unique(test_database):
    password = "Password123!"

    test_database.register_user(
        "user1", "user1@example.com", password
    )

    test_database.register_user(
        "user2", "user2@example.com", password
    )

    conn = test_database.get_connection()

    users = conn.execute(
        "SELECT password FROM users"
    ).fetchall()

    conn.close()

    assert users[0]["password"] != users[1]["password"]