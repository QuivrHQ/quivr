import asyncio


def create_queue() -> asyncio.Queue:
    return asyncio.Queue()


async def event_generator(queue: asyncio.Queue):
    while True:
        result = await queue.get()
        # Yield the result as bytes
        yield (str(result) + "\n").encode("utf-8")
