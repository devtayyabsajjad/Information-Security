from cryptography.fernet import Fernet

def generate_key() -> bytes:
    """
    Generate a new Fernet key.
    """
    return Fernet.generate_key()

def encrypt_text(plain_bytes: bytes, key: bytes) -> bytes:
    """
    Encrypt bytes using the provided Fernet key.
    """
    f = Fernet(key)
    return f.encrypt(plain_bytes)

def decrypt_text(cipher_bytes: bytes, key: bytes) -> bytes:
    """
    Decrypt bytes using the provided Fernet key.
    """
    f = Fernet(key)
    return f.decrypt(cipher_bytes)
