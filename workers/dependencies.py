import asyncio

_loop = None

def get_event_loop():
    global _loop
    if _loop is None:
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop

def run_async(coro):
    return get_event_loop().run_until_complete(coro)