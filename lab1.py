import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from dataclasses import dataclass
import re
from pressure_facade import PressureFacade

@dataclass
class Pressure:
    date: datetime.date
    height: float
    count: int

    def to_list(self):
        return [self.date.strftime("%Y.%m.%d"), self.height, self.count]

    def parse_line(line):
        match = re.search(r'(\d{4}\.\d{2}\.\d{2})\s+(\d.+)\s+(\d+)', line)
        if not match:
            return None
        date_str, h_str, c_str = match.groups()
        return Pressure(
            date=datetime.strptime(date_str, "%Y.%m.%d").date(),
            height=float(h_str),
            count=int(c_str)
        )
    
    def __str__(self):
        return f"{self.date.strftime('%Y.%m.%d')} {self.height} {self.count}\n"


class PressureApp:
    def __init__(self, root, repo):
        self.root = root
        self.repo = repo
        self.items = self.repo.load_all(Pressure)

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        input_frame = ttk.LabelFrame(self.root, text="Добавить новую запись")
        input_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(input_frame, text="Дата (гггг.мм.дд):").grid(row=0, column=0, padx=5, pady=5)
        self.ent_date = ttk.Entry(input_frame)
        self.ent_date.insert(0, datetime.now().strftime("%Y.%m.%d"))
        self.ent_date.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Высота:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_height = ttk.Entry(input_frame)
        self.ent_height.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Кол-во:").grid(row=0, column=4, padx=5, pady=5)
        self.ent_count = ttk.Entry(input_frame)
        self.ent_count.grid(row=0, column=5, padx=5, pady=5)

        btn_add = ttk.Button(input_frame, text="Добавить", command=self.add_item)
        btn_add.grid(row=0, column=6, padx=10, pady=5)

        self.table = ttk.Treeview(self.root, columns=("date", "height", "count"), show="headings")
        self.table.heading("date", text="Дата")
        self.table.heading("height", text="Высота")
        self.table.heading("count", text="Количество")
        self.table.pack(padx=10, pady=5, fill="both")

        btn_del = ttk.Button(self.root, text="Удалить выбранное", command=self.delete_item)
        btn_del.pack(pady=10)

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for item in self.items:
            self.table.insert("", "end", values=item.to_list())

    def add_item(self):
        try:
            new_obj = Pressure(
                date=datetime.strptime(self.ent_date.get(), "%Y.%m.%d").date(),
                height=float(self.ent_height.get()),
                count=int(self.ent_count.get())
            )
            self.items.append(new_obj)
            self.repo.save_all(self.items)
            self.refresh_table()
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность ввода данных")

    def delete_item(self):
        selected = self.table.selection()
        if not selected:
            return

        for item_id in selected:
            index = self.table.index(item_id)
            del self.items[index]
        
        self.repo.save_all(self.items)
        self.refresh_table()

root = tk.Tk()
repository = PressureFacade()
app = PressureApp(root, repository)
root.mainloop()