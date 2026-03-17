import time

import jwt
from pwdlib import PasswordHash

from config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password_hash(password: str, hash_password: str) -> bool:
    return password_hash.verify(password, hash_password)


def create_access_token(
    username: str, expiry: int = settings.jwt_expiry_min
) -> dict[str, str]:
    payload = {"username": username, "expires": time.time() + expiry * 60}
    token = jwt.encode(payload, settings.jwt_hash, algorithm=settings.jwt_algo)
    return {"token": token}


def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.jwt_hash, settings.jwt_algo)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        return
