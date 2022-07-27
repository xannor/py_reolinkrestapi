"""Live Abilities"""

import asyncio
import argparse
from getpass import getpass
import logging

from async_reolink.api import system
from async_reolink.api import commands
from async_reolink.api.const import DEFAULT_USERNAME, DEFAULT_PASSWORD
from async_reolink.rest import Client
from async_reolink.rest.connection import Encryption


class _Arguments(argparse.Namespace):

    hostname: str
    port: int | None
    encryption: Encryption
    username: str
    password: str | None


async def _async_main(args: _Arguments):

    client = Client()
    await client.connect(args.hostname, args.port, encryption=args.encryption)
    if not await client.login(args.username, args.password or DEFAULT_PASSWORD):
        print("Login failed.")
        return

    abilities = await client.get_ability()
    await client.disconnect()

    print(repr(abilities))


logging.root.setLevel(logging.DEBUG)

logging.debug("test")

parser = argparse.ArgumentParser(
    description="Get Live Abilities from Camera")
parser.add_argument(
    "hostname", help="Hostname of device")
parser.add_argument("-p", "--port", type=int,
                    help="Alternate port for api interface", dest="port")
parser.add_argument("--ssl", action='store_const',
                    const=Encryption.HTTPS, default=Encryption.NONE, dest="encryption", help="Use SSL connection")
parser.add_argument("-u", "--user", "--username",
                    default=DEFAULT_USERNAME, help="Username", dest="username")
parser.add_argument("-P", "--pass", "--password",
                    help="Password", default=None, dest="password")

pargs = parser.parse_args(namespace=_Arguments)

if pargs.password is None:
    pargs.password = getpass(prompt=f"Password for {pargs.username}: ")

asyncio.run(_async_main(pargs))
