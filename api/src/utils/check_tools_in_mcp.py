from semantic_kernel.connectors.mcp import MCPStdioPlugin

async def check_tools_in_mcp(plugin: MCPStdioPlugin):
    """
    MCPStdioPlugin を用いて、MCPクライアントに接続後
    利用可能なツールの一覧を取得。
    """

    # 3. MCPサーバが提供するツール一覧を取得
    tools_response = await plugin.session.list_tools()
    tools = tools_response.tools if tools_response else []
    print("取得したツール一覧:")
    for t in tools:
        print(f" - {t.name}: {t.description}")

    return tools