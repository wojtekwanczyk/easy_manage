from unittest import TestCase
from easy_manage.tools.ipmi.reducers.ipmi_reducer import IpmiReducer


class IpmiReducerTestCase(TestCase):
    def setUp(self):
        chass_buffer = {}  # Implement further parsing tests if needed
        sys_buffer = {
            'hardware': {
                'system_components': [
                    {
                        'Board Extra': 'psu',
                        'properties': {
                            'Board Mfg Date': 'Mon Jul 23 14:00:00 2018',
                        }
                    }
                ]
            }
        }

        self.reducer = IpmiReducer(sys_buffer, chass_buffer)

    def test_reduce_chassis_static(self):
        reduced = self.reducer.reduce_chassis_static()
        self.assertEqual(reduced['power_supplies'], {'psu': {'Mfg Date': 'Mon Jul 23 14:00:00 2018'}})
