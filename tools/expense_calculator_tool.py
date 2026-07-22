from utils.expense_calculator import Calculator
from typing import List, Union
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night: Union[str, float], total_days: Union[str, float]) -> float:
            """Calculate total hotel cost."""
            price = self.calculator.parse_float(price_per_night)
            nights = self.calculator.parse_float(total_days)
            return self.calculator.multiply(price, nights)
        
        @tool
        def calculate_total_expense(costs: list[float]) -> float:
            """Calculate total expense of the trip."""
            return self.calculator.calculate_total(*costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense."""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]