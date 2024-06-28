from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse


async def greet_endpoint(*args, **kwargs):
    return PlainTextResponse("Hello!\n")


async def app(scope, receive, send):
    if scope["type"] != "http":
        return
    response = await greet_endpoint()
    await response(scope, receive, send)


class App:
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return
        response = await greet_endpoint()
        await response(scope, receive, send)


class App:
    def __init__(self):
        self.routes = []

    def add_route(self, path, endpoint):
        self.routes.append((path, endpoint))

    def choose_endpoint(self, scope_path):
        for path, endpoint in self.routes:
            if scope_path != path:
                continue
            return endpoint
        return None

    async def __call__(self, scope, receive, send):
        if not scope["type"] == "http":
            return

        endpoint = self.choose_endpoint(scope["path"])
        if endpoint is None:
            response = PlainTextResponse(status_code=404, content="Not found")
        else:
            response = await endpoint(scope, receive, send)

        await response(scope, receive, send)


app = App()
app = Starlette()
app = FastAPI()

app.add_route("/", greet_endpoint)


def main():
    import uvicorn

    uvicorn.run(
        app,
        port=5000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
