import unittest

from resources.lib.utils import datetime_utils
from datetime import datetime, timedelta


class TestDateTimeUtils(unittest.TestCase):

    def test_abs_time_diff(self):

        td1 = timedelta(seconds=60)
        td2 = timedelta(seconds=120)
        delta = datetime_utils.abs_time_diff(td1, td2)
        self.assertEqual(delta, 60)

        delta = datetime_utils.abs_time_diff(td2, td1)
        self.assertEqual(delta, 60)

    def test_format_from_seconds(self):

        s = datetime_utils.format_from_seconds(49)
        self.assertEqual(s, "00:00")

        s = datetime_utils.format_from_seconds(60)
        self.assertEqual(s, "00:01")

        s = datetime_utils.format_from_seconds(3599)
        self.assertEqual(s, "00:59")

        s = datetime_utils.format_from_seconds(7260)
        self.assertEqual(s, "02:01")

    def test_parse_time(self):

        _time = datetime_utils.parse_time(s_time="")
        self.assertEqual(_time.seconds, 0)

        _time = datetime_utils.parse_time(s_time="12:10 pm")
        self.assertEqual(_time.seconds, 43800)

        _time = datetime_utils.parse_time(s_time="12:10")
        self.assertEqual(_time.seconds, 43800)

        _time = datetime_utils.parse_time(s_time="12:10 am")
        self.assertEqual(_time.seconds, 600)

        _time = datetime_utils.parse_time(s_time="00:10")
        self.assertEqual(_time.seconds, 600)

        _time = datetime_utils.parse_time(s_time="00:10", i_day=2)
        self.assertEqual(_time.days, 2)

    def test_time_diff(self):

        td1 = timedelta(seconds=60)
        td2 = timedelta(seconds=120)
        delta = datetime_utils.time_diff(td1, td2)
        self.assertEqual(delta, 60)

        delta = datetime_utils.time_diff(td2, td1)
        self.assertEqual(delta, -60)

    def test_time_duration_str(self):

        s = datetime_utils.time_duration_str("23:30", "02:30")
        self.assertEqual(s, "03:00")
