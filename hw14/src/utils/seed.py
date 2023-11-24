import sys
import random

from anyio import Path


SCRIPT_DIR = Path(__file__).parent
print(f"{SCRIPT_DIR=}")
sys.path.append(str(SCRIPT_DIR.parent))


# Thanks FTKV:  https://raw.githubusercontent.com/FTKV/python-web-hw13/main/src/utils/seed.py

# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3/16985066#16985066

import asyncio
import json
import platform

import aiohttp
import faker

try:
    from src.conf.config import settings
except ImportError:
    from conf.config import settings


ACCESS_TOKEN = ""

NUMBER_CONTACTS = 10


fake_data = faker.Faker("uk_UA")


async def get_fake_contacts():
    for _ in range(NUMBER_CONTACTS):
        # yield (lambda x: [x[1], x[2]] if len(x) == 3 else [x[0], x[1]])(fake_data.name().split(" ")) + [
        #     fake_data.email(),
        #     fake_data.phone_number(),
        #     fake_data.date(),
        #     fake_data.address(),
        # ]
        yield [
            fake_data.first_name(),
            fake_data.last_name(),
            fake_data.email(),
            fake_data.phone_number(),
            fake_data.date(),
            fake_data.address(),
            random.choice([False, True])
        ]


async def send_data_to_api() -> None:
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    session = aiohttp.ClientSession()
    async for first_name, last_name, email, phone, birthday, address, favorite in get_fake_contacts():
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "birthday": birthday,
            "address": address,
            "favorite": favorite,
        }
        try:
            # print(f"{data=}")
            result = await session.post(
                f"http://{settings.app_host}:{settings.app_port}/api/contacts",
                headers=headers,
                data=json.dumps(data),
            )
            if result.status == 429:
                print(f"ERROR: {result.status=}, sleep")
                await asyncio.sleep(6)
                print()
            elif result.status != 201:
                print(
                    f"ERROR: {result.status=}, Try set token. Get token link "
                    f"http://{settings.app_host}:{settings.app_port}/api/auth/login"
                )
                break
        except aiohttp.ClientOSError as err:
            print(f"Connection error: {str(err)}")
            break
    await session.close()
    print("Done")


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(send_data_to_api())
