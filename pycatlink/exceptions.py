"""Custom exceptions for CatLink integration."""

from typing import Any


class CatlinkError(Exception):
    """Base exception for all CatLink errors."""

    pass


class CatlinkLoginError(CatlinkError):
    """Exception raised when login fails."""

    def __init__(self, phone: str, response: dict[str, Any]) -> None:
        """Initialize the login error."""
        error_msg = response.get("msg", "Unknown error")
        super().__init__(f"Login failed for {phone}: {error_msg}")


class CatlinkRequestError(CatlinkError):
    """Exception raised when an API request fails."""

    def __init__(
        self, method: str, url: str, parameters: dict[str, Any] | None = None
    ) -> None:
        """Initialize the request error."""
        super().__init__(f"Request {method} {url} failed with parameters {parameters}")
