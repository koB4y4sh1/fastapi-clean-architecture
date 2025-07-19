# /// script # noqa: CPY001
# dependencies = [
#   "semantic-kernel[mcp]",
# ]
# ///
# Copyright (c) Microsoft. All rights reserved.
import os
# os.environ['HTTP_PROXY'] = "http://gate-i.taisei.co.jp:8080"
# os.environ['HTTPS_PROXY'] = "http://gate-i.taisei.co.jp:8080"
import argparse
import logging
from typing import Annotated, Any, Literal,Optional
from pydantic import BaseModel, Field

import anyio
from collections.abc import Awaitable, Callable
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions import kernel_function
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


# Define a simple plugin for the sample
# Define a simple plugin for the sample
class BookingPlugin:
    """A sample Booking Plugin used for the sample."""

    @kernel_function(description="Asks for a booking, will return 'confirmed' or 'denied' and the reason why denied.")
    def book_a_table(
        self,
        restaurant: Annotated[Literal["AAA", "BBB", "CCC"], "The name of the restaurant."],
        day: Annotated[str, "Day of the week"],
        time: Annotated[int, "The hour of the booking (whole hours only)"],
        number_of_guests: Annotated[int, "The number of guests."],
    ) -> Annotated[str, "Confirmed or denied and the reason why denied."]:
        # Define restaurant-specific business hours and holidays
        restaurant_hours = {
            "AAA": {"open": 12, "close": 23, "holiday": "Monday"},
            "BBB": {"open": 10, "close": 21, "holiday": "Tuesday"},
            "CCC": {"open": 11, "close": 23, "holiday": "Wednesday"},
        }

        # Check if required parameters are provided
        if not restaurant:
            return "denied, Please specify a restaurant."
        if not day:
            return "denied, Please specify a day of the week."
        if not time:
            return "denied, Please specify a booking time."

        # Check if the restaurant exists
        if restaurant not in restaurant_hours:
            return "denied, Invalid restaurant name."

        # Check if the day is a holiday
        if day == restaurant_hours[restaurant]["holiday"]:
            return f"denied, {restaurant} is closed on {day}. Please choose another day."

        # Check if the time is within business hours
        if time < restaurant_hours[restaurant]["open"] or time > restaurant_hours[restaurant]["close"]:
            return f"denied, {restaurant} is open from {restaurant_hours[restaurant]['open']}:00 to {restaurant_hours[restaurant]['close']}:00. Please choose a time within business hours."

        # Confirm the booking
        return "confirmed"

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

    settings = AzureChatPromptExecutionSettings(temperature=0.2, max_tokens=1000, top_p=0.2)
    # settings.response_format = StructuredResult
    kernel = Kernel()
    # Register the plugin to the kernel
    kernel.add_plugin(BookingPlugin(), plugin_name="BookingPlugin")
    # Add the filter to the kernel as a function invocation filter
    # A function invocation filter is called during when the kernel executes a function
    kernel.add_filter(FilterTypes.FUNCTION_INVOCATION, retry_filter)

    agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        # name="Booker",
        name="Booker",
        instructions="Create a booking for the user, this is for the following restaurants: "
        "AAA, BBB, CCC.",
        # plugins=[BookingPlugin()],  # add the sample plugin to the agent
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
