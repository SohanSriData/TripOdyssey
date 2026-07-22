import re

class Calculator:
    @staticmethod
    def parse_float(value) -> float:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            cleaned = re.sub(r"[^0-9.\-,]", "", value.strip())
            cleaned = cleaned.replace(",", "")
            if cleaned == "" or cleaned == "." or cleaned == "-" or cleaned == "-.":
                raise ValueError(f"Unable to parse numeric value from '{value}'")
            return float(cleaned)
        raise TypeError(f"Unsupported type for numeric conversion: {type(value).__name__}")

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return float(a) * float(b)
    
    @staticmethod
    def calculate_total(*x: float) -> float:
        return sum(x)
    
    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        return total / days if days > 0 else 0
    
    