from pressure import Pressure, PressureParseError
from logger import Logger

class PressureFacade:
    filename = "data.txt"

    def load_all(self):
        items = []
        try:
            with open(self.filename, encoding='utf-8') as f:
                for line in f:
                    try:
                        obj = Pressure.parse_line(line)
                        if obj:
                            items.append(obj)
                    except PressureParseError as e:
                        Logger.log(str(e))
        except FileNotFoundError:
            Logger.log(f"Файл {self.filename} не найден", level="WARN")
        return items

    def save_all(self, items):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(str(item))