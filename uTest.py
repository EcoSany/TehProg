import unittest
from datetime import date
from pressure import Pressure, PressureParseError

class TestPressureModel(unittest.TestCase):
    def test_correct_line(self):
        line = "2026.02.13 1234.211 3212"
        res = Pressure.parse_line(line)
        self.assertEqual(res.date, date(2026, 2, 13))
        self.assertEqual(res.height, 1234.211)

    def test_source_tag_line(self):
        line = "2023.10.12 1500.5 755"
        res = Pressure.parse_line(line)
        self.assertIsNotNone(res)
        self.assertEqual(res.date, date(2023, 10, 12))

    def test_invalid_format(self):
        with self.assertRaises(PressureParseError):
            Pressure.parse_line("неправильная строка 123")

unittest.main()