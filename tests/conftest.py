import  asyncio
import pytest
import sys
import nest_asyncio


# Global settings for the event-loop
nest_asyncio.apply()

@pytest.fixture(scope='session')
def event_loop():
    """
    Ensures Windows uses ProactorEventLoop for the entire session.
    Set before async fixtures are created.
    """
    if sys.platform=='win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        loop= asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        yield loop
        loop.close()