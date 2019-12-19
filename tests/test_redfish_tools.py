import unittest
from unittest.mock import Mock

from easy_manage.tools import RedfishTools


class TestRedfishTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {
            'System': {
                'SerialNumber': 'S4ATJ171',
            },
            'Very': {
                'NestedWrong': {
                    'specialKey': 'looseVal'
                },
                'Nested': {
                    'specialKey': 'strictVal'
                },
            },
            'CPUs': [
                {
                    'Name': 'CPU1',
                    'Temp': '100',
                },
                {
                    'Name': 'CPU2',
                    'Temp': '30',
                },
            ],
        }
        cls.rf_tools = RedfishTools()

    def test_find(self):
        found_val = self.rf_tools.find(
            ['SerialNumber'],
            data=self.data)
        self.assertEqual('S4ATJ171', found_val)

    def test_find_not_strict(self):
        found_val = self.rf_tools.find(
            ['Very', 'Nested', 'specialKey'],
            strict=False,
            data=self.data)
        self.assertEqual('looseVal', found_val)

    def test_find_strict(self):
        found_val = self.rf_tools.find(
            ['Very', 'Nested', 'specialKey'],
            strict=True,
            data=self.data)
        self.assertEqual('strictVal', found_val)

    def test_get_dict_containing(self):
        found_dict = self.rf_tools._get_dict_containing(
            'CPU1',
            self.data)
        self.assertEqual(self.data['CPUs'][0], found_dict)
    
    def test_snake_case_dict(self):
        snake_cased = self.rf_tools.snake_case_dict(self.data)
        self.assertTrue('serial_number' in snake_cased['system'].keys())


if __name__ == '__main__':
    unittest.main()
