def encode_url(id: int) -> str:
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    encoded = []

    while id > 0:
        val = id % base
        encoded.append(characters[val])
        id //= base

    return ''.join(reversed(encoded))
