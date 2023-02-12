import asyncio
from contextvars import ContextVar

import pytest

blah = ContextVar("blah")


@pytest.fixture
async def my_context_var():
    blah.set("hello")
    assert blah.get() == "hello"
    yield blah


async def test_context_propagates_from_fixture(my_context_var):
    """
    For this to pass, the commandline flag `--py311-task` or pytest.ini config must contain:
    ```
    py311_task = true
    ```

    This serves as proof that the experimental patch for pytest-asyncio finally allows for proper
    context propagation.
    """
    assert my_context_var.get() == "hello"


@pytest.fixture
async def dummy_fixture():
    before = id(asyncio.current_task())
    yield
    after = id(asyncio.current_task())

    assert before == after


async def test_async_fixture_setup_and_finalize_run_in_same_asyncio_task(dummy_fixture):
    # This passes if no exceptions thrown in dummy_fixture
    assert True
