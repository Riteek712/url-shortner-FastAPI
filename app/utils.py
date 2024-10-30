import secrets
import string

def generate_short_code(length=10):
    """Function to generate a 10-character random string."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def encode_url(id: int) -> str:
    """Encode an ID into a short string."""
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    encoded = []

    while id > 0:
        val = id % base
        encoded.append(characters[val])
        id //= base

    return ''.join(reversed(encoded))
