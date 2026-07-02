from database.users import (
    create_user,
    verify_user,
    user_exists,
    load_users
)


print("=" * 50)
print("Testing User Module")
print("=" * 50)

# Create a test user
created = create_user(
    "Test User",
    "test@example.com",
    "password123"
)

print(f"User created: {created}")

# Check existence
print(f"User exists: {user_exists('test@example.com')}")

# Verify correct password
user = verify_user(
    "test@example.com",
    "password123"
)

print(f"Login successful: {user is not None}")

# Verify wrong password
wrong = verify_user(
    "test@example.com",
    "wrongpassword"
)

print(f"Wrong password rejected: {wrong is None}")

print("\nCurrent users:")
print(load_users())