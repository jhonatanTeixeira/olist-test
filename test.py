from unittest import TestCase
from domain.model import PhoneCallStart
from datetime import datetime as DateTime


class TestPhoneCallStart(TestCase):
    def test_should_calculate_cost_with_an_hour_out_of_range(self):
        phone_call_start = PhoneCallStart(DateTime.now().replace(hour=21), 1, 1112345678, 1123456789)
        phone_call_start.end_timestamp = DateTime.now().replace(hour=23)

        shouldCost = 0.36 + (60 * 0.09)

        self.assertEqual(shouldCost, phone_call_start.cost)

    def test_should_calculate_cost_with_hours_within_range(self):
        phone_call_start = PhoneCallStart(DateTime.now().replace(hour=20), 1, 1112345678, 1123456789)
        phone_call_start.end_timestamp = DateTime.now().replace(hour=22)

        shouldCost = 0.36 + ((2 * 60) * 0.09)

        self.assertEqual(shouldCost, phone_call_start.cost)

    def test_should_calculate_minimun_cost_hours_outside_range(self):
        phone_call_start = PhoneCallStart(DateTime.now().replace(hour=1), 1, 1112345678, 1123456789)
        phone_call_start.end_timestamp = DateTime.now().replace(hour=5)

        shouldCost = 0.36

        self.assertEqual(shouldCost, phone_call_start.cost)

    def test_should_raise_when_call_not_ended(self):
        phoneCallStart = PhoneCallStart(DateTime.now().replace(hour=21), 1, 1112345678, 1123456789)

        self.assertFalse(phoneCallStart.is_call_ended())

        with self.assertRaises(RuntimeError):
            phoneCallStart.cost

    def test_should_raise_when_invalid(self):
        with self.assertRaises(AssertionError):
            PhoneCallStart(DateTime.now(), 1, 111234567822, '1123456dddd78912343')

        # with self.assertRaises(AssertionError):
        #     pcs = PhoneCallStart(DateTime.now(), 1, 1112345678, 1123456789)
        #     PhoneCallEnd(DateTime.now(), 2, pcs)

