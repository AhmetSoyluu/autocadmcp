import asyncio

from autocad_mcp_server.services.execution_queue import ExecutionQueue


def test_execution_queue_runs_tasks() -> None:
    queue = ExecutionQueue()

    async def operation() -> str:
        await asyncio.sleep(0)
        return "ok"

    result = asyncio.run(queue.run(operation))

    assert result == "ok"
