# /// script # noqa: CPY001
# dependencies = [
#   "semantic-kernel[mcp]",
# ]
# ///
# Copyright (c) Microsoft. All rights reserved.
import os
import anyio
import argparse
import logging
from typing import Any, Literal
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.memory.volatile_memory_store import VolatileMemoryStore
from semantic_kernel.connectors.ai.open_ai.services.azure_text_embedding import AzureTextEmbedding
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin

load_dotenv()
logger = logging.getLogger(__name__)
print(os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"))  # 環境変数の読み込み
print(os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT"))  # 環境変数の読み込み
print(os.getenv("AZURE_OPENAI_API_KEY"))  # 環境変数の読み込み

"""
This sample demonstrates how to expose your Semantic Kernel `kernel` instance as a MCP server.

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
                "sk_mcp_server.py"
            ],
            "env": {
                "OPENAI_API_KEY": "<your_openai_api_key>",
                "OPENAI_CHAT_MODEL_ID": "gpt-4o-mini"
            }
        }
    }
}
```

Note: You might need to set the uv to its full path.

Alternatively, you can run this as a SSE server, by setting the same environment variables as above, 
and running the following command:
```bash
uv --directory=<path to sk project>/semantic-kernel/python/samples/demos/mcp_server \
run sk_mcp_server.py --transport sse --port 8000
```
This will start a server that listens for incoming requests on port 8000.

In both cases, uv will make sure to install semantic-kernel with the mcp extra for you in a temporary venv.
"""


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

embedding_gen = AzureTextEmbedding(
    deployment_name=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
    endpoint=os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# @vectorstoremodel(collection_name="tourist_attractions")
# @dataclass
# class TouristAttraction:
#     """Model to store information about tourist attractions."""

#     text: Annotated[str, VectorStoreField("data", is_full_text_indexed=True)]
#     id: Annotated[str, VectorStoreField("key")] = field(default_factory=lambda: str(uuid4()))
#     embedding: Annotated[
#         list[float] | str | None, VectorStoreField("vector", dimensions=1536, embedding_generator=embedding_gen)
#     ] = None

#     def __post_init__(self):
#         if self.embedding is None:
#             self.embedding = self.text

tokyo_tour_guide = "tokyo is a vibrant city with a rich history and culture. It is known for its modern skyscrapers, traditional temples, and bustling streets. The city offers a wide range of attractions, including the iconic Tokyo Tower, the historic Senso-ji Temple in Asakusa, and the trendy shopping district of Shibuya. Visitors can also enjoy delicious Japanese cuisine, explore beautiful parks like Ueno Park, and experience the unique blend of tradition and innovation that defines Tokyo."
yokohama_tour_guide = "Yokohama is a port city located just south of Tokyo. It is known for its beautiful waterfront, historic buildings, and vibrant Chinatown. The city offers attractions such as the iconic Yokohama Landmark Tower, the picturesque Sankeien Garden, and the bustling Minato Mirai district. Visitors can also enjoy delicious Chinese cuisine in Chinatown, explore the Cup Noodles Museum, and take a stroll along the scenic waterfront promenade."
fujisan_tour_guide = "Mount Fuji is Japan's highest peak and an iconic symbol of the country. It is a stratovolcano located about 100 kilometers southwest of Tokyo. The mountain is known for its symmetrical cone shape and is often covered in snow. Visitors can enjoy breathtaking views of Mount Fuji from various locations, including Lake Kawaguchi and the Fuji Five Lakes area. The mountain is also a popular destination for hiking, with several trails leading to its summit."
chiba_tour_guide = "Chiba is a prefecture located east of Tokyo, known for its beautiful coastline, theme parks, and historical sites. It is home to the famous Tokyo Disneyland and Tokyo DisneySea, attracting millions of visitors each year. Chiba also offers attractions such as the Naritasan Shinshoji Temple, the scenic Kujukuri Beach, and the historic Sawara district. Visitors can enjoy fresh seafood, explore the picturesque countryside, and experience the unique culture of Chiba."
nijiironotani_tour_guide = "虹色の谷は、幻想的な景観が広がる架空の観光地です。谷の底には色とりどりの花々が咲き乱れ、季節ごとに異なるパレットで訪れる人々を魅了します。特に、春には桜やチューリップが一斉に咲き誇り、谷をピンクや赤で染め上げます。夜には光るキノコが幻想的な輝きを放ち、星空とのコントラストが夢のような風景を演出します。自然と調和したアート作品も点在し、訪れるたびに新たな感動を提供してくれる場所です。"


collection_id = "tourist_attractions"

#注意：SemanticTextMemoryは削除される予定

async def populate_memory(memory: SemanticTextMemory) -> None:
    # Add some documents to the semantic memory
    await memory.save_information(collection=collection_id, id="info1", text=tokyo_tour_guide)
    await memory.save_information(collection=collection_id, id="info2", text=yokohama_tour_guide)
    await memory.save_information(collection=collection_id, id="info3", text=fujisan_tour_guide)
    await memory.save_information(collection=collection_id, id="info4", text=chiba_tour_guide)
    await memory.save_information(collection=collection_id, id="info5", text=nijiironotani_tour_guide)

async def run(transport: Literal["sse", "stdio"] = "stdio", port: int | None = None) -> None:
    kernel = Kernel()
    # kernel.add_service(embedding_gen)
    # in_memory_store = InMemoryStore()

    # collection = in_memory_store.get_collection(record_type=TouristAttraction)
    # await collection.ensure_collection_exists()

    kernel.add_service(embedding_gen)
    memory = SemanticTextMemory(storage=VolatileMemoryStore(), embeddings_generator=embedding_gen)
    kernel.add_plugin(TextMemoryPlugin(memory), "TextMemoryPlugin")
    await populate_memory(memory)
    # records = [
    #     TouristAttraction(text=tokyo_tour_guide),
    #     TouristAttraction(text=yokohama_tour_guide),
    #     TouristAttraction(text=fujisan_tour_guide),
    #     TouristAttraction(text=chiba_tour_guide),
    #     TouristAttraction(text=nijiironotani_tour_guide),
    # ]
    # await collection.upsert(records)
    # async with InMemoryCollection(record_type=TouristAttraction) as collection:
    #     await collection.ensure_collection_exists()
    #     records = [
    #         TouristAttraction(text=tokyo_tour_guide),
    #         TouristAttraction(text=yokohama_tour_guide),
    #         TouristAttraction(text=fujisan_tour_guide),
    #         TouristAttraction(text=chiba_tour_guide),
    #         TouristAttraction(text=nijiironotani_tour_guide),
    #     ]
    #     await collection.upsert(records)
    # kernel.add_function("memory", 
    #                 collection.create_search_function(
    #                 function_name="search_tourist_attractions",
    #                 description="Search for tourist attractions.",
    #                 )
    # )

    server = kernel.as_mcp_server(server_name="memory_sk")

    if transport == "sse" and port is not None:
        import uvicorn
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
                await server.run(read_stream, write_stream, server.create_initialization_options())

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)  # nosec
    elif transport == "stdio":
        import anyio
        from mcp.server.stdio import stdio_server

        async def handle_stdin(stdin: Any | None = None, stdout: Any | None = None) -> None:
            async with stdio_server() as (read_stream, write_stream):
                await server.run(read_stream, write_stream, server.create_initialization_options())

        await handle_stdin() 


if __name__ == "__main__":
    args = parse_arguments()
    anyio.run(run, args.transport, args.port)
