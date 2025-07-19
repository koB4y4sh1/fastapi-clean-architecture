
from pydantic import BaseModel
import yaml
from pathlib import Path

from src.schema.value_object.agent import AgentObject

def get_agent(response_format: BaseModel|None = None) -> AgentObject:
    """
    YAMLファイルからエージェントの設定値を取得し、AgentRepoを返します。
    dataフォルダの中にあるagent.yamlファイルを読み込みます。
    
    Returns:
        AgentRepo: エージェントの設定値情報。
    """
    agent_yaml_path = Path(__file__).parent.parent.parent / "data" / "agent.yaml"
    with open(agent_yaml_path, "r", encoding="utf-8") as f:
        agent_yaml_str = f.read()
    agent_data = yaml.safe_load(agent_yaml_str)  # YAMLをパースしてエージェントの設定値を取得

    # AgentRepoモデルに変換
    return AgentObject(**agent_data) if agent_data else None
