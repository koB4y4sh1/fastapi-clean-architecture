from pydantic import BaseModel
from semantic_kernel.connectors.mcp import MCPSsePlugin
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments

class AgentWithPlugin(BaseModel):
    settings:AzureChatPromptExecutionSettings
    name:str
    instructions:str
    plugins:list[MCPSsePlugin]

    def create_agent(self) -> ChatCompletionAgent:
        """
        直接 MCPStdioPlugin を組み込んだ ChatCompletionAgent を作成
        """
        arguments = KernelArguments(
            settings = self.settings
        )

        agent = ChatCompletionAgent(
            service=AzureChatCompletion(), 
            name=self.name,
            instructions=self.instructions,
            plugins=self.plugins,
            arguments=arguments,
        )
        return agent
    
    # pydanticでサポートされいなMCPSsePluginの型を使用するため追記
    model_config = {
        "arbitrary_types_allowed": True
    }