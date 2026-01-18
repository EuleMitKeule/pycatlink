"""Utility functions for CatLink integration."""

import base64
import hashlib
from typing import Any, cast

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from .const import RSA_PUBLIC_KEY, SIGN_KEY


class CryptUtils:
    """Cryptographic utilities for CatLink API."""

    @staticmethod
    def sign_parameters(parameters: dict[str, Any]) -> str:
        """Generate MD5 signature for request parameters."""
        sorted_items = sorted(parameters.items())
        params_with_key = [f"{key}={value}" for key, value in sorted_items]
        params_with_key.append(f"key={SIGN_KEY}")
        params_string = "&".join(params_with_key)
        return hashlib.md5(params_string.encode()).hexdigest().upper()

    @staticmethod
    def encrypt_password(password: str) -> str:
        """Encrypt password using RSA public key encryption."""
        md5_hash = hashlib.md5(password.encode()).hexdigest().lower()
        sha1_hash = hashlib.sha1(md5_hash.encode()).hexdigest().upper()

        public_key = cast(
            rsa.RSAPublicKey,
            serialization.load_der_public_key(
                base64.b64decode(RSA_PUBLIC_KEY), default_backend()
            ),
        )

        encrypted = public_key.encrypt(sha1_hash.encode(), padding.PKCS1v15())
        return base64.b64encode(encrypted).decode()
