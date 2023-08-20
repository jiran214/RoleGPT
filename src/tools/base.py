from abc import ABC
from typing import Type, Any
from langchain.tools import BaseTool

from pydantic import BaseModel


class ToolModel(BaseModel, ABC):

    def use(self, *args, **kwargs):
        raise NotImplementedError


    class Meta:
        name = ""  # 工具名称
        description = ""  # 工具描述


class LangchainToolAdapter(BaseTool):
    @classmethod
    def from_tool_model(cls, tool_model: Type[ToolModel]):
        instance = cls(
            name = tool_model.Meta.name,
            description = tool_model.Meta.description,
            args_schema = tool_model
        )
        return instance

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        assert self.args_schema
        tool_model = self.args_schema(*args, **kwargs)
        return tool_model.use()

