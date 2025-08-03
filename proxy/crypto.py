import os, time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 256-бит ключ (32 байта)
MASTER_KEY = bytes.fromhex("0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
TTL_SEC = 12 * 3600

class KeyRing:
    def __init__(self):
        self._key_id = int(time.time() // TTL_SEC)
        self._key = self._derive_key(self._key_id)

    def _derive_key(self, key_id: int) -> bytes:
        # HKDF-like: просто SHA-256(key_id || MASTER_KEY)
        import hashlib
        return hashlib.sha256(self._key_id.to_bytes(4, "big") + MASTER_KEY).digest()

    def current(self):
        now = int(time.time() // TTL_SEC)
        if now != self._key_id:
            self._key_id = now
            self._key = self._derive_key(now)
        return str(self._key_id), self._key

    def get(self, key_id: str):
        return self._derive_key(int(key_id))

keyring = KeyRing()

def encrypt(plaintext: bytes):
    key_id, key = keyring.current()
    aes = AESGCM(key)
    iv = os.urandom(12)
    ct = aes.encrypt(iv, plaintext, None)
    return key_id, iv, ct

def decrypt(key_id: str, iv: bytes, ciphertext: bytes) -> bytes:
    key = keyring.get(key_id)
    aes = AESGCM(key)
    return aes.decrypt(iv, ciphertext, None)
