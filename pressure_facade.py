class PressureFacade:
    filename = "data.txt"

    def load_all(self, Pressure):
        items = []
        
        with open(PressureFacade.filename, 'r', encoding='utf-8') as f:
            for line in f:
                obj = Pressure.parse_line(line)
                if obj: 
                    items.append(obj)
       
        return items

    def save_all(self, items):
        with open(PressureFacade.filename, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(item)