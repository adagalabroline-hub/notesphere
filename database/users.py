import json
from pathlib import Path
from hashlib import sha256

USERS_FILE = Path("users.json")


def load_users():
    """Load all users from storage."""
    if not USERS_FILE.exists():
        return []

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_users(users):
    """Save all users to storage."""
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def hash_password(password):
    """Hash a password using SHA-256."""
    return sha256(password.encode("utf-8")).hexdigest()


def user_exists(email):
    """Check whether an email is already registered."""
    users = load_users()

    return any(
        user["email"].lower() == email.lower()
        for user in users
    )


def create_user(name, email, password):
    """Create a new user account."""

    if user_exists(email):
        return False

    users = load_users()

    users.append({
        "name": name,
        "email": email.lower(),
        "password": hash_password(password)
    })

    save_users(users)

    return True


def verify_user(email, password):
    """Verify login credentials."""

    users = load_users()
    password_hash = hash_password(password)

    for user in users:
        if (
            user["email"].lower() == email.lower()
            and user["password"] == password_hash
        ):
            return user

    return None