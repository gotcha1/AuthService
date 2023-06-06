import pytest

from app.utils.validate import validate_password, validate_username


@pytest.mark.parametrize(
    "password",
    ["Abcdef123", "Password123", "SecurePassw0rd", "SecurePassw0rd@123"],
)
def test_validate_password_valid(password):
    assert validate_password(password) is None


@pytest.mark.parametrize(
    "password, expected_error",
    [
        ("Ab", "length must be atleast 3 characters"),
        ("Abcdef123" * 4, "length must not exceed 32 characters"),
        ("abcdef123", "should contain atleast one uppercase letter"),
        ("ABCDEF123", "should contain atleast one lowercase letter"),
        ("Abcdefghi", "should contain atleast one number"),
    ],
)
def test_validate_password_invalid(password, expected_error):
    with pytest.raises(Exception, match=expected_error):
        validate_password(password)


@pytest.mark.parametrize(
    "username",
    ["john_doe", "user123", "admin"],
)
def test_validate_username_valid(username):
    assert validate_username(username) is None


@pytest.mark.parametrize(
    "username, expected_error",
    [
        ("ab", "length must be atleast 3 characters"),
        ("abcdefghij" * 4, "length must not exceed 32 characters"),
    ],
)
def test_validate_username_invalid(username, expected_error):
    with pytest.raises(Exception, match=expected_error):
        validate_username(username)
