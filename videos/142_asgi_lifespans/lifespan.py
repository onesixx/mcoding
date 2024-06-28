import asyncio
import enum
import traceback
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastapi import FastAPI
from rich import print
from starlette.types import ASGIApp, Scope, Receive, Send


@asynccontextmanager
async def lifespan(the_app):
    logger.info("Starting up...")
    the_app.db = await init_db()
    the_app.s3_client = await init_boto_s3()
    the_app.redis_client = await init_redis()
    the_app.settings.dynamic = await read_dynamic_settings(the_app.db)
    the_app.sanity_check_settings()
    the_app.spawn_metrics_worker()
    yield
    logger.info("Shutting down...")
    await the_app.save_metrics(the_app.db)
    await email_devops()  # :)


@asynccontextmanager
async def lifespan(the_app):
    async with asyncio.timeout(10):  # use asyncio.wait_for if Python < 3.11
        print("startup things")
        await startup_wait(the_app)
    try:
        yield {"machine_id": 42}  # state copied to every request
    finally:
        async with asyncio.timeout(10):
            await shutdown_wait(the_app)
            print("shutdown things")


@asynccontextmanager
async def lifespan(the_app):
    print("startup things")
    yield
    print("shutdown things")


app = FastAPI(lifespan=lifespan)


@app.on_event("startup")  # DEPRECATED
async def startup_event():
    ...


@app.on_event("shutdown")  # DEPRECATED
async def shutdown_event():
    ...


@asynccontextmanager
async def lifespan(the_app):
    async with asyncio.timeout(30):  # Python 3.11+ or asyncio.wait_for
        await could_hang_forever()
    try:
        yield
    finally:
        async with asyncio.timeout(30):
            print("shutdown things")


@dataclass
class Lifespan:
    app: ASGIApp

    async def __aenter__(self):
        async with asyncio.timeout(10):
            print("startup things")
            await startup_wait(self.app)

        return {"machine_id": 42}

    async def __aexit__(self, exc_type, exc_value, tb) -> bool | None:
        async with asyncio.timeout(10):
            print("shutdown things")
            await shutdown_wait(self.app)
        return None


async def startup_wait(app):
    await asyncio.sleep(5)


async def shutdown_wait(app):
    await asyncio.sleep(5)


class App:
    def __init__(self, *, lifespan):
        self.lifespan = lifespan

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        scope["app"] = self
        print(scope)
        if scope["type"] == "lifespan":
            await self.handle_lifespan(scope, receive, send)

    async def handle_lifespan(self, scope: Scope, receive: Receive, send: Send):
        assert scope["type"] == "lifespan"
        message = await receive()
        assert message["type"] == "lifespan.startup"
        started = False
        app = scope.get("app")
        try:
            async with self.lifespan(app) as state:
                if state is not None:
                    scope["state"].update(state)
                await send({"type": "lifespan.startup.complete"})
                started = True
                message = await receive()
                assert message["type"] == "lifespan.shutdown"
        except BaseException:
            event_type = (
                "lifespan.shutdown.failed" if started else "lifespan.startup.failed"
            )
            await send({"type": event_type, "message": traceback.format_exc()})
            raise
        await send({"type": "lifespan.shutdown.complete"})


class AsgiEventType(enum.StrEnum):
    LIFESPAN_STARTUP = "lifespan.startup"
    LIFESPAN_STARTUP_COMPLETE = "lifespan.startup.complete"
    LIFESPAN_STARTUP_FAILED = "lifespan.startup.failed"

    LIFESPAN_SHUTDOWN = "lifespan.shutdown"
    LIFESPAN_SHUTDOWN_COMPLETE = "lifespan.shutdown.complete"
    LIFESPAN_SHUTDOWN_FAILED = "lifespan.shutdown.failed"

    ...


app = App()


def main():
    import uvicorn

    uvicorn.run(app, port=5000, log_level="info", timeout_graceful_shutdown=3)


if __name__ == "__main__":
    main()
