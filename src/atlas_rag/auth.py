from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any

from fastapi import HTTPException, status

from atlas_rag.config import get_settings
from atlas_rag.models import Role, UserRecord


def hash_password(password: str, salt: str | None = None) -> str:
    salt_value = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_value.encode("utf-8"), 120_000)
    return f"{salt_value}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    salt_value, expected_hash = password_hash.split("$", maxsplit=1)
    candidate = hash_password(password, salt_value).split("$", maxsplit=1)[1]
    return secrets.compare_digest(candidate, expected_hash)


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("utf-8")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def issue_token(username: str, role: Role, ttl_minutes: int | None = None) -> tuple[str, int]:
    settings = get_settings()
    expires_at = int(time.time()) + 60 * (ttl_minutes or settings.token_ttl_minutes)
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": username, "role": role, "exp": expires_at}
    signing_input = ".".join(
        [
            _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8")),
            _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8")),
        ]
    )
    signature = hmac.new(
        settings.jwt_secret.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return f"{signing_input}.{_b64url_encode(signature)}", expires_at


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        header_part, payload_part, signature_part = token.split(".")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token") from exc

    signing_input = f"{header_part}.{payload_part}"
    expected_signature = hmac.new(
        settings.jwt_secret.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(_b64url_encode(expected_signature), signature_part):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature")

    payload = json.loads(_b64url_decode(payload_part))
    if int(payload["exp"]) <= int(time.time()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    return payload


def seed_users() -> dict[str, UserRecord]:
    return {
        "alice.finance": UserRecord(
            username="alice.finance",
            password_hash=hash_password("FinanceDemo123"),
            display_name="Alice Finance",
            role="finance",
        ),
        "harry.hr": UserRecord(
            username="harry.hr",
            password_hash=hash_password("HrDemo123"),
            display_name="Harry HR",
            role="hr",
        ),
        "erin.exec": UserRecord(
            username="erin.exec",
            password_hash=hash_password("ExecDemo123"),
            display_name="Erin Executive",
            role="executive",
        ),
        "emma.employee": UserRecord(
            username="emma.employee",
            password_hash=hash_password("EmployeeDemo123"),
            display_name="Emma Employee",
            role="employee",
        ),
    }

