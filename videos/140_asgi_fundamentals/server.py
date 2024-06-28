from collections.abc import MutableMapping, Callable, Awaitable
from typing import Any

from rich import print

# from starlette.applications import Starlette
# from starlette.requests import Request
# from starlette.responses import PlainTextResponse

type Scope = MutableMapping[str, Any]
type Message = MutableMapping[str, Any]
type Receive = Callable[[], Awaitable[Message]]
type Send = Callable[[Message], Awaitable[None]]
type ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]


async def handle_lifetime(scope: Scope, receive: Receive, send: Send):
    assert scope["type"] == "lifespan"

    while True:
        message = await receive()
        print(f"Got message:", message)

        if message["type"] == "lifespan.startup":
            # scope["state"]["GlobalKey"] = "Value"
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})
            break


async def echo_endpoint(scope: Scope, receive: Receive, send: Send):
    data = []
    while True:
        print("Waiting for message...")
        message = await receive()
        print(f"Received message:", message)

        if message["type"] == "http.disconnect":
            return

        assert message["type"] == "http.request"

        data.append(message["body"])

        if not message["more_body"]:
            break

    response_message = {
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain")],
    }
    print("Sending response start:", response_message)
    await send(response_message)

    response_message = {
        "type": "http.response.body",
        "body": b"echo: " + b"".join(data),
        "more_body": False,
    }
    print("Sending response body:", response_message)
    await send(response_message)


async def status_endpoint(scope: Scope, receive: Receive, send: Send):
    response_message = {
        "type": "http.response.start",
        "status": 204,  # http no content
    }
    print("Sending response start:", response_message)
    await send(response_message)

    response_message = {
        "type": "http.response.body",
        "body": b"",
        "more_body": False,
    }
    print("Sending response body:", response_message)
    await send(response_message)


async def error_endpoint(scope: Scope, receive: Receive, send: Send):
    response_message = {
        "type": "http.response.start",
        "status": 400,
    }
    print("Sending response start:", response_message)
    await send(response_message)

    response_message = {
        "type": "http.response.body",
        "body": b"",
        "more_body": False,
    }
    print("Sending response body:", response_message)
    await send(response_message)


async def handle_http(scope: Scope, receive: Receive, send: Send):
    assert scope["type"] == "http"

    if scope["path"] == "/echo" and scope["method"] == "POST":
        await echo_endpoint(scope, receive, send)
    elif scope["path"] == "/status" and scope["method"] == "GET":
        await status_endpoint(scope, receive, send)
    else:
        await error_endpoint(scope, receive, send)


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    print(f"Beginning connection. Scope: ", scope)

    if scope["type"] == "lifespan":
        await handle_lifetime(scope, receive, send)
    elif scope["type"] == "http":
        await handle_http(scope, receive, send)

    print(f"Ending connection")


def main():
    import uvicorn

    uvicorn.run(
        app,
        port=5000,
        log_level="info",
        use_colors=False,
        # root_path="/api",
    )


if __name__ == "__main__":
    main()
