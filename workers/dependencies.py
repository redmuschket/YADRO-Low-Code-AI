import asyncio
import threading

_loop = None
_loop_thread = None
_loop_lock = threading.Lock()


def get_event_loop():
    global _loop, _loop_thread

    with _loop_lock:
        if _loop is None or _loop.is_closed():
            _loop = asyncio.new_event_loop()
            _loop_thread = threading.Thread(target=_loop.run_forever, daemon=True)
            _loop_thread.start()

    return _loop


def run_async(coro, timeout=None):
    loop = get_event_loop()

    if timeout:
        async def coro_with_timeout():
            return await asyncio.wait_for(coro, timeout=timeout)

        future = asyncio.run_coroutine_threadsafe(coro_with_timeout(), loop)
    else:
        future = asyncio.run_coroutine_threadsafe(coro, loop)

    try:
        return future.result(timeout=timeout + 5 if timeout else None)
    except Exception as e:
        future.cancel()
        raise