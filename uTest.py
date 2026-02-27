import unittest
from datetime import date
from pressure import Pressure, PressureParseError
from commandProcessor import CommandProcessor

class TestPressureModel(unittest.TestCase):
    def test_correct_line_1(self):
        line = "2026.02.13 1234.211 3212"
        res = Pressure.parse_line(line)
        self.assertEqual(res.date, date(2026, 2, 13))
        self.assertEqual(res.height, 1234.211)
        self.assertEqual(res.count, 3212)

    def test_correct_line_2(self):
        line = "2023.10.12 1500.5 755"
        res = Pressure.parse_line(line)
        self.assertEqual(res.date, date(2023, 10, 12))
        self.assertEqual(res.height, 1500.5)
        self.assertEqual(res.count, 755)

    def test_invalid_format(self):
        with self.assertRaises(PressureParseError):
            Pressure.parse_line("неправильная строка 123")

class PreApp:
    def __init__(self):
        self.items = []
        self.repo = self
    def save_all(self, items): pass

class TestPressureExtended(unittest.TestCase):

    def setUp(self):
        self.app = PreApp()
        self.processor = CommandProcessor(self.app)

    def test_command_add(self):
        self.processor.execute("ADD 2026.10.10; 100; 50")
        self.assertEqual(len(self.app.items), 1)
        self.assertEqual(self.app.items[0].count, 50)

    def test_command_rem_1(self):
        self.app.items = [
            Pressure(date(2026, 1, 1), 10, 500),
            Pressure(date(2026, 1, 1), 10, 1000),
            Pressure(date(2026, 1, 1), 20, 1500)
        ]
        self.processor.execute("REM count < 1000")
        self.assertEqual(len(self.app.items), 1)
        self.assertEqual(self.app.items[0].count, 500)

    def test_command_rem_2(self):
        self.app.items = [
            Pressure(date(2026, 1, 1), 100, 10),
            Pressure(date(2026, 1, 1), 300, 10),
            Pressure(date(2026, 1, 1), 500, 10)
        ]
        self.processor.execute("REM height >= 300")
        self.assertEqual(len(self.app.items), 2)
        self.assertEqual(self.app.items[0].height, 300)
        self.assertEqual(self.app.items[1].height, 500)

unittest.main()