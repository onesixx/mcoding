def iter_example():
    for x in y:
        ...  # loop body

    it = iter(y)  # y.__iter__()
    x = next(it)  # it.__next__()
    ...  # loop body
    x = next(it)
    ...  # loop body
    x = next(it)  # eventually raises StopIteration


async def aiter_example():
    async for x in y:
        ...  # loop body

    it = aiter(y)  # y.__aiter__()
    x = await anext(it)  # it.__anext__()
    ...  # loop body
    x = await anext(it)
    ...  # loop body
    x = await anext(it)  # eventually raises StopAsyncIteration


class Iterable:
    def __iter__(self):
        return ...  # return some iterator


class Iterator:
    def __next__(self):
        return ...  # get the next element or raise StopIteration

    def __iter__(self):
        return self


class AsyncIterable:
    def __aiter__(self):
        return ...  # return some async iterator


class AsyncIterator:
    async def __anext__(self):
        return ...  # get the next element or raise StopAsyncIteration

    def __aiter__(self):
        return self
