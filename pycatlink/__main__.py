import asyncio
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Annotated, Any, ParamSpec, TypeVar

import typer
from dotenv import load_dotenv

from .account import CatlinkAccount
from .const import (
    ENV_CATLINK_PASSWORD,
    ENV_CATLINK_PHONE,
    ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
)
from .models import CatlinkAccountConfig

app = typer.Typer()

P = ParamSpec("P")
R = TypeVar("R")


def syncify(f: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, R]:
    """Decorator to convert async function to sync by running with asyncio.run."""

    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@app.command()
@syncify
async def devices(
    phone: Annotated[
        str,
        typer.Option(
            ...,
            help="Catlink account phone number (not starting with 0 or country code).",
            envvar=ENV_CATLINK_PHONE,
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            ...,
            help="Catlink account password.",
            envvar=ENV_CATLINK_PASSWORD,
        ),
    ],
    phone_international_code: Annotated[
        str,
        typer.Option(
            help="Catlink account phone international code.",
            envvar=ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
        ),
    ],
) -> None:
    """Print the list of devices associated with the account."""

    config = CatlinkAccountConfig(
        phone=phone,
        password=password,
        phone_international_code=phone_international_code,
    )

    account = CatlinkAccount(config)

    typer.echo("Fetching devices...")

    devices = await account.get_devices()

    typer.echo(f"Found {len(devices)} device(s)")

    for i, device in enumerate(devices):
        typer.echo(f"Device {i + 1}")
        typer.echo(device.device_info)


@app.command()
@syncify
async def device(
    phone: Annotated[
        str,
        typer.Option(
            ...,
            help="Catlink account phone number (not starting with 0 or country code).",
            envvar=ENV_CATLINK_PHONE,
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            ...,
            help="Catlink account password.",
            envvar=ENV_CATLINK_PASSWORD,
        ),
    ],
    phone_international_code: Annotated[
        str,
        typer.Option(
            help="Catlink account phone international code.",
            envvar=ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
        ),
    ],
    device_id: Annotated[
        str,
        typer.Argument(
            ...,
            help="ID of the device to get details for.",
        ),
    ],
) -> None:
    """Print detailed information for a specific device."""

    config = CatlinkAccountConfig(
        phone=phone,
        password=password,
        phone_international_code=phone_international_code,
    )

    account = CatlinkAccount(config)

    typer.echo("Fetching devices...")

    devices = await account.get_devices()

    device = next(
        (device for device in devices if str(device.device_info.id) == device_id), None
    )
    if not device:
        typer.echo(f"Device with ID {device_id} not found.")
        raise typer.Exit(code=1)

    typer.echo(f"Info for device ID {device_id}:")
    typer.echo(device.device_info)
    if device.device_info.current_error_message:
        typer.echo(f"  Error: {device.device_info.current_error_message}")

    device_details = await device.device_details
    if not device_details:
        typer.echo("No detailed information available for this device.")
        raise typer.Exit(code=0)

    typer.echo(f"Details for device ID {device_id}:")
    typer.echo(device_details)


if __name__ == "__main__":
    load_dotenv()
    app()
