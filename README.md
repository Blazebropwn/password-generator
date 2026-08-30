# Password Generator

A compact Python CLI for generating passwords with the standard-library `secrets` module.

[![CI](https://github.com/Blazebropwn/password-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/Blazebropwn/password-generator/actions/workflows/ci.yml)

## Security choices

- Uses cryptographically secure randomness instead of `random`
- Guarantees at least one character from each selected group
- Never saves generated passwords unless `--save` is explicitly provided
- Can exclude visually ambiguous characters

## Usage

```bash
python password_generator.py
python password_generator.py --length 24 --count 5
python password_generator.py --no-specials
python password_generator.py --exclude-ambiguous
python password_generator.py --save generated_passwords.txt
```

## Development

Python 3.9+ is required. The application has no third-party runtime dependencies.

```bash
pip install -r requirements-dev.txt
pytest
```

## License

MIT
