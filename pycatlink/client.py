from time import time
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientConnectorError, ClientSession, ContentTypeError

from .const import (
    API_LOGIN_PASSWORD,
    DATA_KEY_TOKEN,
    DEFAULT_REQUEST_TIMEOUT,
    ERROR_CODE_TOKEN_EXPIRED,
    HEADER_LANGUAGE,
    HEADER_TOKEN,
    HEADER_USER_AGENT,
    PARAMETER_INTERNATIONAL_CODE,
    PARAMETER_MOBILE,
    PARAMETER_NONCESTR,
    PARAMETER_PASSWORD,
    PARAMETER_PLATFORM,
    PARAMETER_SIGN,
    PARAMETER_TOKEN,
    PASSWORD_MAX_LENGTH,
    PLATFORM_ANDROID,
    RESPONSE_DATA,
    RESPONSE_RETURN_CODE,
    USER_AGENT,
    HttpMethod,
)
from .exceptions import CatlinkError, CatlinkLoginError, CatlinkRequestError
from .models import CatlinkAccountConfig
from .utils import CryptUtils


class CatlinkApiClient:
    """Client for interacting with the Catlink API."""

    def __init__(self, config: CatlinkAccountConfig) -> None:
        """Initialize the client."""
        self.config = config
        self.session = ClientSession()

    async def disconnect(self) -> None:
        """Disconnect the account."""
        await self.session.close()

    @property
    def password(self) -> str:
        """Return the encrypted password."""
        if len(self.config.password) <= PASSWORD_MAX_LENGTH:
            return CryptUtils.encrypt_password(self.config.password)
        return self.config.password

    async def async_login(self) -> None:
        """Login the account and store the authentication token."""
        response = await self.request(
            path=API_LOGIN_PASSWORD,
            method=HttpMethod.POST,
            parameters={
                PARAMETER_PLATFORM: PLATFORM_ANDROID,
                PARAMETER_INTERNATIONAL_CODE: self.config.phone_international_code,
                PARAMETER_MOBILE: str(self.config.phone),
                PARAMETER_PASSWORD: self.password,
            },
        )

        token = response.get(RESPONSE_DATA, {}).get(DATA_KEY_TOKEN)
        if not token:
            raise CatlinkLoginError(self.config.phone, response)

        self.config.token = token

    async def request(
        self,
        path: str,
        method: HttpMethod,
        parameters: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Request the API with automatic signing and token management."""
        url = urljoin(self.config.api_base, path)
        prepared_params = self._prepare_parameters(parameters)

        request_kwargs = {
            "timeout": DEFAULT_REQUEST_TIMEOUT,
            "headers": {
                HEADER_LANGUAGE: self.config.language,
                HEADER_USER_AGENT: USER_AGENT,
                HEADER_TOKEN: self.config.token or "",
            },
            "params" if method == HttpMethod.GET else "data": prepared_params,
            **kwargs,
        }

        try:
            response = await self.session.request(method.value, url, **request_kwargs)
            response_data = await response.json()
        except (ClientConnectorError, TimeoutError, ContentTypeError) as exception:
            raise CatlinkRequestError(method.value, url, prepared_params) from exception

        if not isinstance(response_data, dict):
            raise CatlinkRequestError(method.value, url, prepared_params)

        return response_data

    async def request_with_auto_login(
        self,
        path: str,
        method: HttpMethod,
        parameters: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make a request with automatic login and token refresh on expiration."""
        if not self.config.token:
            await self.async_login()

        response = await self.request(
            path=path,
            method=method,
            parameters=parameters,
            **kwargs,
        )

        # Retry once if token expired
        if response.get(RESPONSE_RETURN_CODE) == ERROR_CODE_TOKEN_EXPIRED:
            await self.async_login()
            response = await self.request(
                path=path,
                method=method,
                parameters=parameters,
                **kwargs,
            )

        return response

    async def request_with_return_code(
        self,
        path: str,
        method: HttpMethod,
        parameters: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Make a request and check the return code."""
        response = await self.request_with_auto_login(
            path=path,
            method=method,
            parameters=parameters,
            **kwargs,
        )

        return_code = response.get(RESPONSE_RETURN_CODE, 0)
        if return_code != 0:
            raise CatlinkError(f"Command failed with code {return_code}")

    def _prepare_parameters(self, parameters: dict[str, Any] | None) -> dict[str, Any]:
        """Prepare request parameters with signature and token."""
        params = parameters.copy() if parameters else {}

        params[PARAMETER_NONCESTR] = int(time() * 1000)
        if self.config.token:
            params[PARAMETER_TOKEN] = self.config.token
        params[PARAMETER_SIGN] = CryptUtils.sign_parameters(params)

        return params
