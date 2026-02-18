import re
from datetime import datetime
from dataclasses import dataclass

class PressureParseError(Exception): pass

@dataclass
class Pressure:
    date: datetime.date
    height: float
    count: int

    def to_list(self):
        return [self.date.strftime("%Y.%m.%d"), self.height, self.count]

    @staticmethod
    def parse_line(line):
        match = re.search(r'(\d{4}\.\d{2}\.\d{2})\s+([\d.]+)\s+(\d+)', line)
        if not match:
            raise PressureParseError(f"Строка не соответствует формату: {line.strip()}")
        
        date_str, h_str, c_str = match.groups()
        return Pressure(
            date=datetime.strptime(date_str, "%Y.%m.%d").date(),
            height=float(h_str),
            count=int(c_str)
        )

    def __str__(self):
        return f"{self.date.strftime('%Y.%m.%d')} {self.height} {self.count}\n"