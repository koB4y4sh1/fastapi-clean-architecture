
"""
agent.py

このモジュールは、エージェントの入出力やステータス、処理ステップ、タスクの構造化結果を表現するPydanticモデルを定義します。

クラス:
    Input: エージェントへの入力データの型と値を表現します。
    Output: エージェントからの出力データの型と値を表現します。
    Status: ステップやタスクの進行状況やエラー情報を表現します。
    Step: タスクを構成する各ステップの詳細情報を表現します。
    StructuredResult: タスク全体の構造化された実行結果を表現します。
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, Annotated


class Input(BaseModel):
    """
    エージェントへの入力データを表現するモデル。
    input_typeでデータ型（text, number, list, dict）を指定し、input_valueに値を格納します。
    """
    input_type: Annotated[Literal["text", "number", "list", "dict"], Field(description="Input data type")]
    input_value: Annotated[str | int | float | list[int|float|str] | dict[int|float|str, int|float|str], Field(description="Input data")]


class Output(BaseModel):
    """
    エージェントからの出力データを表現するモデル。
    output_typeでデータ型（text, number, list, dict）を指定し、output_valueに値を格納します。
    """
    output_type: Annotated[Literal["text", "number", "list", "dict"], Field(description="Output data type")]
    output_value: Annotated[str | int | float | list[int|float|str] | dict[int|float|str, int|float|str], Field(description="Output data")]
    
class Status(BaseModel):
    """
    ステップやタスクの進行状況やエラー情報を表現するモデル。
    phaseで状態（success, failure, in_progress）を示し、messageやerror_codeで詳細を補足します。
    """
    phase: Annotated[Literal["success", "failure", "in_progress"], Field(description="Status phase")]
    message: Annotated[Optional[str], Field(description="Status message")] = None
    error_code: Annotated[Optional[str], Field(description="Error code")] = None

class Step(BaseModel):
    """
    タスクを構成する各ステップの詳細情報を表現するモデル。
    ステップID、名称、説明、状態、入出力、子ステップなどを持ちます。
    """
    step_id: Annotated[str, Field(description="UUID of the step")]
    step_name: Annotated[str, Field(description="name of the step")]
    explanation: Annotated[str, Field(description="explanation of the step")]
    status: Annotated[Status, Field(description="Step status")]
    function_name: Annotated[Optional[str], Field(description="Function called in this step")]
    input: Annotated[Optional[Input], Field(description="Step input")]
    output: Annotated[Output, Field(description="Step output")]
    steps: Annotated[Optional[list["Step"]], Field(description="Child steps")]

class StructuredResult(BaseModel):
    """
    タスク全体の構造化された実行結果を表現するモデル。
    タスクID、名称、説明、状態、各ステップ、カテゴリ、タグ、最終結果などを持ちます。
    """
    task_id: Annotated[str, Field(description="UUID of the task")]
    task_name: Annotated[str, Field(description="name of the task")]
    explanation: Annotated[str, Field(description="explanation of the task")]
    status: Annotated[Status, Field(description="Task status")]
    function_name: Annotated[Optional[str], Field(description="Function called in this step")]
    # input: Optional[Input]
    steps: Annotated[Optional[list["Step"]], Field(description="Each step to complete the task")]
    # output: Output
    categories: Annotated[Optional[list[Literal["restaurant", "menu", "calculation"]]], Field(description="categories of the task")]
    tags: Annotated[Optional[list[str]], Field(description="tags of the task")]
    result: Annotated[str, Field(description="final result of the task")]