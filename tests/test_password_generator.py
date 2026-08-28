import string

from password_generator import generate_password


def test_requested_length():
    assert len(generate_password(length=32)) == 32


def test_selected_groups_are_present():
    password = generate_password(length=32, use_numbers=True, use_specials=True)
    assert any(ch.isalpha() for ch in password)
    assert any(ch.isdigit() for ch in password)
    assert any(ch in string.punctuation for ch in password)
