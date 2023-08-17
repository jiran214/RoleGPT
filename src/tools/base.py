from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool


class CurrentStockPriceInput(BaseModel):
    """Inputs for get_current_stock_price"""

    ticker: str = Field(description="Ticker symbol of the stock")
    num: int = 123


class CurrentStockPriceTool(BaseTool):
    name = "get_current_stock_price"
    description = """
        Useful when you want to get current stock price.
        You should enter the stock ticker symbol recognized by the yahoo finance
        """
    args_schema: Type[BaseModel] = CurrentStockPriceInput

    def _run(self, ticker: str):
        price_response = 15
        return price_response

    def _arun(self, ticker: str):
        raise NotImplementedError("get_current_stock_price does not support async")