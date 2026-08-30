#!/usr/bin/env python3
"""Cryptographically secure command-line password generator."""

from __future__ import annotations

import argparse
import os
import secrets
import string
from pathlib import Path

AMBIGUOUS = set("O0Il1|`'\"")


def _clean(chars: str, exclude_ambiguous: bool) -> str:
    return "".join(ch for ch in chars if ch not in AMBIGUOUS) if exclude_ambiguous else chars


def generate_password(length: int = 16, use_numbers: bool = True, use_specials: bool = True, exclude_ambiguous: bool = False) -> str:
    """Generate a password with at least one character from each selected group."""
    groups = [_clean(string.ascii_letters, exclude_ambiguous)]
    if use_numbers:
        groups.append(_clean(string.digits, exclude_ambiguous))
    if use_specials:
        groups.append(_clean(string.punctuation, exclude_ambiguous))
    if length < len(groups):
        raise ValueError(f"Length must be at least {len(groups)} for the selected character groups")
    password = [secrets.choice(group) for group in groups]
    pool = "".join(groups)
    password.extend(secrets.choice(pool) for _ in range(length - len(password)))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def save_passwords(passwords: list[str], path: str) -> Path:
    output = Path(path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(output, flags, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write("\n".join(passwords) + "\n")
    os.chmod(output, 0o600)
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate cryptographically secure passwords.")
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length (default: 16)")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords (default: 1)")
    parser.add_argument("--no-numbers", action="store_true", help="Exclude digits")
    parser.add_argument("--no-specials", action="store_true", help="Exclude punctuation")
    parser.add_argument("--exclude-ambiguous", action="store_true", help="Avoid visually ambiguous characters")
    parser.add_argument("--save", metavar="FILE", help="Optionally save passwords to a file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.length <= 0:
        parser.error("Length must be greater than zero")
    if args.count <= 0:
        parser.error("Count must be greater than zero")
    try:
        passwords = [generate_password(args.length, not args.no_numbers, not args.no_specials, args.exclude_ambiguous) for _ in range(args.count)]
    except ValueError as exc:
        parser.error(str(exc))
    print("\n".join(passwords))
    if args.save:
        print(f"Saved to {save_passwords(passwords, args.save).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
