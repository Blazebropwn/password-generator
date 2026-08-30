import string
import stat
import os

import pytest

from password_generator import AMBIGUOUS, generate_password, save_passwords


def test_requested_length():
    assert len(generate_password(length=32)) == 32


def test_selected_groups_are_present():
    password = generate_password(length=32, use_numbers=True, use_specials=True)
    assert any(ch.isalpha() for ch in password)
    assert any(ch.isdigit() for ch in password)
    assert any(ch in string.punctuation for ch in password)


def test_excludes_ambiguous_characters():
    password = generate_password(length=256, exclude_ambiguous=True)
    assert not set(password) & AMBIGUOUS


def test_rejects_length_shorter_than_selected_groups():
    with pytest.raises(ValueError, match="at least 3"):
        generate_password(length=2)


def test_saved_password_file_is_private(tmp_path):
    output = save_passwords(["secret"], str(tmp_path / "passwords.txt"))
    assert output.read_text() == "secret\n"
    if os.name != "nt":
        assert stat.S_IMODE(output.stat().st_mode) == 0o600
