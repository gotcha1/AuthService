import re
import logging


def min_length_validation(input: str, length: int = 2):
    return len(input) > length


def max_length_validation(input: str, length: int = 33):
    return len(input) < length


def uppercase_validation(input: str):
    pattern = r"[A-Z]"
    return bool(re.search(pattern, input))


def lowercase_validation(input: str):
    pattern = r"[a-z]"
    return bool(re.search(pattern, input))


def number_validation(input: str):
    pattern = r"\d"
    return bool(re.search(pattern, input))


conditions = {
    "min_length": min_length_validation,
    "max_length": max_length_validation,
    "one_uppercase": uppercase_validation,
    "one_lowercase": lowercase_validation,
    "one_number": number_validation,
}

validation_errors = {
    "min_length": "length must be atleast 3 characters",
    "max_length": "length must not exceed 32 characters",
    "one_uppercase": "should contain atleast one uppercase letter",
    "one_lowercase": "should contain atleast one lowercase letter",
    "one_number": "should contain atleast one number"
}

username_conditions = ["min_length", "max_length"]
pwd_conditions = ["min_length", "max_length", "one_uppercase", "one_lowercase", "one_number"]


def validate_username(name: str):
    errors = []
    for condition in username_conditions:
        if not conditions[condition](name):
            errors.append(validation_errors[condition])
    if len(errors):
        logging.info(f"[validate_username]username, {name} errors: {errors}")
        raise Exception(create_error_msg(errors))


def validate_password(pwd: str):
    pwd_errors = []
    for condition in pwd_conditions:
        if not conditions[condition](pwd):
            pwd_errors.append(validation_errors[condition])
    if len(pwd_errors):
        logging.info(f"[validate_password]pwd, {pwd} errors: {pwd_errors}")
        raise Exception(create_error_msg(pwd_errors))


def create_error_msg(errors):
    return ", ".join(errors)
