import asyncio
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

import typer
from dotenv import load_dotenv

from pycatlink.c08 import CatlinkC08Device
from pycatlink.client import CatlinkApiClient

from .account import CatlinkAccount
from .const import (
    ENV_CATLINK_PASSWORD,
    ENV_CATLINK_PHONE,
    ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
    HttpMethod,
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


@app.command("fetch")
@syncify
async def api_fetch(
    phone: str = typer.Option(
        ...,
        help="Catlink account phone number (not starting with 0 or country code).",
        envvar=ENV_CATLINK_PHONE,
    ),
    password: str = typer.Option(
        ...,
        help="Catlink account password.",
        envvar=ENV_CATLINK_PASSWORD,
    ),
    phone_international_code: str = typer.Option(
        ...,
        help="Catlink account phone international code.",
        envvar=ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
    ),
    path: str = typer.Option(
        ...,
        help="API path to fetch data from.",
    ),
    parameters: str = typer.Option(
        "",
        help="Query parameters in key1=value1&key2=value2 format.",
    ),
) -> None:
    """GET Request to the Catlink API."""

    config = CatlinkAccountConfig(
        phone=phone,
        password=password,
        phone_international_code=phone_international_code,
    )
    client = CatlinkApiClient(config)

    parameters_dict: dict[str, str] = {}
    if parameters:
        for pair in parameters.split("&"):
            if "=" in pair:
                key, value = pair.split("=", 1)
                parameters_dict[key] = value

    response = await client.request_with_auto_login(
        path=path,
        parameters=parameters_dict,
        method=HttpMethod.GET,
    )

    typer.echo("Response:")
    typer.echo(response)


@app.command()
@syncify
async def pets(
    phone: str = typer.Option(
        ...,
        help="Catlink account phone number (not starting with 0 or country code).",
        envvar=ENV_CATLINK_PHONE,
    ),
    password: str = typer.Option(
        ...,
        help="Catlink account password.",
        envvar=ENV_CATLINK_PASSWORD,
    ),
    phone_international_code: str = typer.Option(
        ...,
        help="Catlink account phone international code.",
        envvar=ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
    ),
) -> None:
    """Print the list of pets associated with the account."""

    config = CatlinkAccountConfig(
        phone=phone,
        password=password,
        phone_international_code=phone_international_code,
    )

    account = CatlinkAccount(config)

    typer.echo("Fetching pets...")

    pets = await account.get_pets()

    typer.echo(f"Found {len(pets)} pet(s)")

    for i, pet in enumerate(pets):
        typer.echo(f"Pet {i + 1}")
        typer.echo(pet)


@app.command()
@syncify
async def devices(
    phone: str = typer.Option(
        ...,
        help="Catlink account phone number (not starting with 0 or country code).",
        envvar=ENV_CATLINK_PHONE,
    ),
    password: str = typer.Option(
        ...,
        help="Catlink account password.",
        envvar=ENV_CATLINK_PASSWORD,
    ),
    phone_international_code: str = typer.Option(
        ...,
        help="Catlink account phone international code.",
        envvar=ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
    ),
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
    phone: str = typer.Option(
        ...,
        help="Catlink account phone number (not starting with 0 or country code).",
        envvar=ENV_CATLINK_PHONE,
    ),
    password: str = typer.Option(
        ...,
        help="Catlink account password.",
        envvar=ENV_CATLINK_PASSWORD,
    ),
    phone_international_code: str = typer.Option(
        ...,
        help="Catlink account phone international code.",
        envvar=ENV_CATLINK_PHONE_INTERNATIONAL_CODE,
    ),
    device_id: str = typer.Argument(
        ...,
        help="ID of the device to get details for.",
    ),
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

    typer.echo(f"Refreshing data for device ID {device_id}...")

    await device.refresh()

    typer.echo(f"Info for device ID {device_id}:")
    typer.echo(device.device_info)

    if not isinstance(device, (CatlinkC08Device,)):
        typer.echo("Detailed information fetching is only supported for C08 devices.")
        raise typer.Exit(code=0)

    typer.echo(f"Details for device ID {device_id}:")
    typer.echo(device.device_details)

    typer.echo(f"Stats for device ID {device_id}:")
    typer.echo(device.device_stats)

    typer.echo(f"Logs for device ID {device_id}:")
    typer.echo(device.device_logs)

    typer.echo(f"Pet stats for device ID {device_id}:")
    typer.echo(device.pet_stats)

    typer.echo(f"Linked pets for device ID {device_id}:")
    typer.echo(device.linked_pets)

    typer.echo(f"Selectable pets for device ID {device_id}:")
    typer.echo(device.selectable_pets)

    typer.echo(f"WiFi info for device ID {device_id}:")
    typer.echo(device.wifi_info)

    typer.echo(f"Notice configurations for device ID {device_id}:")
    typer.echo(device.notice_configs)

    typer.echo(f"About device information for device ID {device_id}:")
    typer.echo(device.about_device)


if __name__ == "__main__":
    load_dotenv()
    app()
