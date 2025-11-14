# crypto_service.py
import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

SALT_SIZE = 16
IV_SIZE = 16
KEY_SIZE = 32 # AES-256
KDF_ITERATIONS = 100000 # Standar keamanan yang baik

def encrypt(payload_bytes: bytes, password: str) -> bytes:
    salt = get_random_bytes(SALT_SIZE)
    
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=KDF_ITERATIONS)
    
    padded_payload = pad(payload_bytes, AES.block_size)
    
    iv = get_random_bytes(IV_SIZE)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    encrypted_data = cipher.encrypt(padded_payload)
    
    # Sesuai desain: [16B SALT] + [16B IV] + [ENCRYPTED DATA]
    return salt + iv + encrypted_data

def decrypt(encrypted_package: bytes, password: str) -> bytes:
    try:
        # Ekstrak komponen dari paket
        salt = encrypted_package[0:SALT_SIZE]
        iv = encrypted_package[SALT_SIZE : SALT_SIZE + IV_SIZE]
        encrypted_data = encrypted_package[SALT_SIZE + IV_SIZE :]
        
        # Turunkan kembali key menggunakan salt yang diekstrak
        key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=KDF_ITERATIONS)
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        padded_payload = cipher.decrypt(encrypted_data)
        
        # Unpad untuk mendapatkan data asli
        payload_bytes = unpad(padded_payload, AES.block_size)
        
        return payload_bytes
    except (ValueError, KeyError, IndexError):
        # Ini akan gagal jika password salah atau data korup
        raise ValueError("Password salah atau data rusak.")