from semantic_kernel.connectors.mcp import MCPSsePlugin

def create_mcp_time_plugin() -> MCPSsePlugin:
    return MCPSsePlugin(
        name="GitHub",
        url="https://gitmcp.io/langchain-ai/langgraph",
    )