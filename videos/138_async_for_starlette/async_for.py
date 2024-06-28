import asyncio
import time
from collections.abc import Iterable, Awaitable


async def use_api(x: int):
    await asyncio.sleep(0.1)  # fake lag
    return 2 * x


async def await_rate_limited(awaitables, rate: float):
    max_sleep_duration = 1 / rate
    for aw in awaitables:
        start = time.perf_counter()
        yield await aw
        elapsed = time.perf_counter() - start
        await asyncio.sleep(max(0.0, max_sleep_duration - elapsed))


class AwaitRateLimited:
    def __init__(self, awaitables: Iterable[Awaitable], rate: float):
        self.awaitables = iter(awaitables)
        self.max_sleep_duration = 1 / rate
        self.last_iter_at: float | None = None

    def __aiter__(self):
        return self

    async def wait_if_needed(self):
        if self.last_iter_at is None:
            return
        now = time.perf_counter()
        elapsed = now - self.last_iter_at
        await asyncio.sleep(max(0.0, self.max_sleep_duration - elapsed))

    async def __anext__(self):
        await self.wait_if_needed()
        self.last_iter_at = time.perf_counter()
        try:
            awaitable = next(self.awaitables)
        except StopIteration:
            raise StopAsyncIteration
        return await awaitable


async def main():
    awaitables = (use_api(x) for x in range(10))
    start = time.perf_counter()
    async for result in AwaitRateLimited(awaitables, rate=5.0):
        elapsed = time.perf_counter() - start
        print(f"[{elapsed:.2f}s] Got result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
