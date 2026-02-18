import re
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Pressure:
    date: datetime.date
    height: float
    count: int

def parse_input(input_str):
    res = re.search(r'(\d{4}\.\d{2}\.\d{2})\s+(\d+.\d+)\s+(\d+)', input_str)

    if res:
        date_str, height_str, count_str = res.groups()
        date_obj = datetime.strptime(date_str, "%Y.%m.%d").date()

        return Pressure(
            date=date_obj,
            height=float(height_str),
            count=int(count_str)
        )
    return None

raw_string = "Измерения_давления 2023.10.12    1500.5   755"
result = parse_input(raw_string)

print(result)