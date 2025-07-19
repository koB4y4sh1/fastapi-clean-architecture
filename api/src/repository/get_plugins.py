
import yaml
from pathlib import Path

from src.schema.value_object.plugin import PluginObject

def get_plugins() -> list[PluginObject]:
    """
    YAMLファイルからプラグインの設定値を取得し、プラグインのリストを返します。
    dataフォルダの中にあるplugin.yamlファイルを読み込みます。
    Args:
        plugin_yaml_str (str): YAML形式のプラグイン定義文字列。
    Returns:
        list[PluginRepo]: プラグインの設定値情報のリスト。
    """
    plugin_file_path = Path(__file__).parent.parent.parent.joinpath('data', 'plugins.yaml')
    
    with open(plugin_file_path, 'r', encoding='utf-8') as file:
        plugin_yaml_str = file.read()
    
    plugin_data = yaml.safe_load(plugin_yaml_str)  # YAMLをパースしてプラグインの設定値を取得
    plugins = plugin_data.get("plugins", [])        # プラグインの設定値情報
    
    return [PluginObject(**plugin) for plugin in plugins]