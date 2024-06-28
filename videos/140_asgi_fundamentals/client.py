import asyncio

import httpx

from rich import print


async def data(n):
    for i in range(n):
        await asyncio.sleep(1)
        msg = f"{i}".encode()
        print("Sending data:", msg)
        yield msg


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:5000/some/path?q=123&x=456",
            # "http://127.0.0.1:5000/echo",
            # "http://127.0.0.1:5000/status",
            data=data(5),
            # data={"username": "scott", "password": "tiger"},
        )
        print("Response status:", response.status_code)
        print("Response content:", response.content)


if __name__ == "__main__":
    asyncio.run(main(), debug=False)
