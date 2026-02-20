import re
from datetime import datetime

class PressureParseError(Exception): pass

cdef class Pressure:
    cdef public object date
    cdef public double height
    cdef public int count

    def __init__(self, object date, double height, int count):
        self.date = date
        self.height = height
        self.count = count

    def to_list(self):
        return [self.date.strftime("%Y.%m.%d"), self.height, self.count]

    @staticmethod
    def parse_line(str line):
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