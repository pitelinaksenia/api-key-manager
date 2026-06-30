import hashlib
import secrets


def generate_api_key() -> tuple[str, str, str]:

    raw_key = f"sk_live{secrets.token_urlsafe(32)}"
    prefix = raw_key[:16]
    key_hash = hash_key(raw_key)

    return raw_key, prefix, key_hash


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()
