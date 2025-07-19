# /// script # noqa: CPY001
# dependencies = [
#   "semantic-kernel[mcp]",
# ]
# ///
# Copyright (c) Microsoft. All rights reserved.
import argparse
import logging

import anyio
import os
# os.environ['HTTP_PROXY'] = "http://gate-i.taisei.co.jp:8080"
# os.environ['HTTPS_PROXY'] = "http://gate-i.taisei.co.jp:8080"
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, Any, Literal

from collections.abc import Awaitable, Callable
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.filters.filter_types import FilterTypes
from semantic_kernel.filters import FunctionInvocationContext

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
"""
This sample demonstrates how to expose an Agent as a MCP server.

To run this sample, set up your MCP host (like Claude Desktop or VSCode Github Copilot Agents)
with the following configuration:
```json
{
    "mcpServers": {
        "sk": {
            "command": "uv",
            "args": [
                "--directory=<path to sk project>/semantic-kernel/python/samples/demos/mcp_server",
                "run",
                "agent_mcp_server.py"
            ],
            "env": {
                "AZURE_AI_AGENT_PROJECT_CONNECTION_STRING": "<your azure connection string>",
                "AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME": "<your azure model deployment name>",
            }
        }
    }
}
```
Alternatively, you can run this as a SSE server, by setting the same environment variables as above, 
and running the following command:
```bash
uv --directory=<path to sk project>/semantic-kernel/python/samples/demos/mcp_server \
run agent_mcp_server.py --transport sse --port 8000
```
This will start a server that listens for incoming requests on port 8000.

In both cases, uv will make sure to install semantic-kernel with the mcp extra for you in a temporary venv.
"""

# Define the BaseModel we will use for structured outputs
class Input(BaseModel):
    input_type: str
    input_value: str | list[str] | dict[str, str] = Field(..., description="Input data")

class Output(BaseModel):
    output_type: str
    output_value: str | list[str] | dict[str, str] = Field(..., description="Output data")

class Status(BaseModel):
    phase: Literal["success", "failure", "in_progress"]
    message: Optional[str] = None
    error_code: Optional[str] = None

class Step(BaseModel):
    step_id: str = Field(..., description="UUID of the sub task")
    step_name: str
    explanation: str
    status: Status
    function_name: Optional[str]
    input: Optional[Input]
    output: Output
    steps: Optional[list["Step"]]

class StructuredResult(BaseModel):
    task_id: str = Field(..., description="UUID of the task")
    task_name: str
    explanation: str
    status: Status
    function_name: Optional[str]
    # input: Optional[Input]
    steps: Optional[list["Step"]]
    # output: Output
    result: str

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Semantic Kernel MCP server.")
    parser.add_argument(
        "--transport",
        type=str,
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport method to use (default: stdio).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to use for SSE transport (required if transport is 'sse').",
    )
    return parser.parse_args()

async def retry_filter(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    """A filter that retries the function invocation if it fails.

    The filter uses a binary exponential backoff strategy to retry the function invocation.
    """
    for i in range(MAX_RETRIES):
        try:
            await next(context)
            return
        except Exception as e:
            logger.warning(f"Failed to execute the function: {e}")
            backoff = 2**i
            logger.info(f"Sleeping for {backoff} seconds before retrying")

async def run(transport: Literal["sse", "stdio"] = "stdio", port: int | None = None) -> None:

    kernel = Kernel()
    settings = AzureChatPromptExecutionSettings(temperature=0.2, max_tokens=1000, top_p=0.2)
    # settings.response_format = StructuredResult
    print(Path(os.path.dirname(__file__)).parent.joinpath('mcp').as_posix())
    async with (
        MCPStdioPlugin(
        name="Numerical_Calculation",
        description="Numerical calculation plugin, for numerical calculation for addition and multiplication, call this plugin.",
        command="uv",
        args=[
            f"--directory={Path(os.path.dirname(__file__)).parent.joinpath('mcp').as_posix()}",
            "run",
            "math_mcp_server.py",
        ],

    ) as math_plugin):
        kernel.add_plugin(math_plugin)
        kernel.add_filter(FilterTypes.FUNCTION_INVOCATION, retry_filter)
        agent = ChatCompletionAgent(
            service=AzureChatCompletion(),
            name="Calculator",
            instructions="Answer questions about numerical calculations for addition and multiplication.",
            # plugins=[math_plugin],  # add the sample plugin to the agent
            kernel=kernel,
            arguments=KernelArguments(settings=settings),
        )

        server = agent.as_mcp_server()

        if transport == "sse" and port is not None:
            import nest_asyncio
            import uvicorn
            from mcp.server.sse import SseServerTransport
            from starlette.applications import Starlette
            from starlette.routing import Mount, Route

            sse = SseServerTransport("/messages/")

            async def handle_sse(request):
                async with sse.connect_sse(request.scope, request.receive, request._send) as (
                    read_stream,
                    write_stream,
                ):
                    await server.run(read_stream, write_stream, server.create_initialization_options())

            starlette_app = Starlette(
                debug=True,
                routes=[
                    Route("/sse", endpoint=handle_sse),
                    Mount("/messages/", app=sse.handle_post_message),
                ],
            )
            nest_asyncio.apply()
            uvicorn.run(starlette_app, host="0.0.0.0", port=port)  # nosec
        elif transport == "stdio":
            from mcp.server.stdio import stdio_server

            async def handle_stdin(stdin: Any | None = None, stdout: Any | None = None) -> None:
                async with stdio_server() as (read_stream, write_stream):
                    await server.run(read_stream, write_stream, server.create_initialization_options())

            await handle_stdin()


if __name__ == "__main__":
    args = parse_arguments()
    anyio.run(run, args.transport, args.port)
