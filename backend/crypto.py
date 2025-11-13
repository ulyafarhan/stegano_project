# crypto.py
def encrypt(data: bytes, key: int) -> bytes:
    return bytes([(b + key) % 256 for b in data])

def decrypt(data: bytes, key: int) -> bytes:
    return bytes([(b - key) % 256 for b in data])