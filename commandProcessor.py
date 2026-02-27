from pressure import Pressure
import re

class CommandProcessor:
    def __init__(self, app_instance):
        self.app = app_instance

    def read_command(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.execute(line.strip())

    def execute(self, command_line):
        if not command_line: return
        
        cmd, _, args = command_line.partition(' ')
        cmd = cmd.upper()

        if cmd == "ADD":
            obj = Pressure.from_csv(args)
            self.app.items.append(obj)
        
        elif cmd == "REM":
            match = re.match(r"(\w+)\s*([<>=!]+)\s*([\d.]+)", args)
            if match:
                field, op, value = match.groups()
                value = float(value)
                
                self.app.items = [
                    item for item in self.app.items 
                    if self.check_condition(item, field, op, value)
                ]

        elif cmd == "SAVE":
            filename = args if args else "result.txt"
            self.app.repo.filename = filename
            self.app.repo.save_all(self.app.items)
        
        elif cmd == "PRINT":
            print(args)

    def check_condition(self, item, field, op, value):
        attr_val = getattr(item, field, None)
        if attr_val is None: return False
        
        if op == "<": return attr_val < value
        if op == ">": return attr_val > value
        if op == "==": return attr_val == value
        if op == "!=": return attr_val != value
        if op == ">=": return attr_val >= value
        if op == "<=": return attr_val <= value
        return False