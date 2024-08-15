import unittest
from datetime import datetime, timedelta

from resources.lib.utils import datetime_utils


class TestDateTimeUtils(unittest.TestCase):

    def test_tc1_apply_for_now(self):

        now = datetime(year=2024, month=8, day=15, hour=15, minute=0)
        td = timedelta(days=2, hours=14, minutes=0)
        date = datetime_utils.apply_for_now(now, td, force_future=True)
        self.assertEquals(date, datetime(
            year=2024, month=8, day=21, hour=14, minute=0))

    def test_tc2_apply_for_now(self):

        now = datetime(year=2024, month=8, day=15, hour=15, minute=0)
        td = timedelta(days=3, hours=14, minutes=0)
        date = datetime_utils.apply_for_now(now, td, force_future=True)
        self.assertEquals(date, datetime(
            year=2024, month=8, day=22, hour=14, minute=0))

    def test_tc3_apply_for_now(self):

        now = datetime(year=2024, month=8, day=15, hour=15, minute=0)
        td = timedelta(days=3, hours=15, minutes=5)
        date = datetime_utils.apply_for_now(now, td, force_future=True)
        self.assertEquals(date, datetime(
            year=2024, month=8, day=15, hour=15, minute=5))

    def test_tc1_time_diff(self):

        td1 = timedelta(seconds=60)
        td2 = timedelta(seconds=120)
        delta = datetime_utils.time_diff(td1, td2)
        self.assertEqual(delta, 60)

        delta = datetime_utils.time_diff(td2, td1)
        self.assertEqual(delta, -60)

    def test_tc2_time_diff(self):
        """
        Datetime                             x       Thursday, 2024-08-15 16:30
        Timedelta           x                |       Wednesday, 8:30 ---> 2024-08-14 8:30
                            |   now          |       now = 2024-08-14 15:30
                  |---------|---+------------|---->
                            |- -115200 secs- |
        """

        now = datetime(year=2024, month=8, day=14,
                       hour=15, minute=30, second=0)

        t1 = timedelta(days=2, hours=8, minutes=30, seconds=0)
        t2 = datetime(year=2024, month=8, day=15, hour=16, minute=30, second=0)
        delta = datetime_utils.time_diff(t1, t2, now)
        self.assertEqual(delta, -115200)

        delta = datetime_utils.time_diff(t2, t1, now)
        self.assertEqual(delta, -115200)

    def test_tce_time_diff(self):
        """
        Datetime                                     x        Monday, 2024-08-12 00:02
        Timedelta    x ---> x                        |        Monday, 0:01 ==> 2024-08-12 00:01
                     :      |                        |        now = Monday, 2024-08-12 00:01
                  |--:---+--|------------------------|---->
                        now |                        |
                            |-      60 secs         -|
        """

        now = datetime(year=2024, month=8, day=12, hour=0, minute=1, second=0)

        t1 = timedelta(days=0, hours=0, minutes=1, seconds=0)
        t2 = datetime(year=2024, month=8, day=12, hour=0, minute=2, second=0)
        delta = datetime_utils.time_diff(t1, t2, now)
        self.assertEqual(delta, -60)

        delta = datetime_utils.time_diff(t2, t1, now)
        self.assertEqual(delta, -60)

    def test_tc6_datetime_diff(self):
        """
        Datetime                                     x        Monday, 2024-08-12 00:02
        Datetime            x                        |        Monday, 2024-08-12 00:01
                            |                        |        now = Monday, 2024-08-12 00:01
                  |------+--|------------------------|---->
                        now |                        |
                            |-      60 secs         -|
        """

        now = datetime(year=2024, month=8, day=12, hour=0, minute=1, second=0)

        t1 = datetime(year=2024, month=8, day=12, hour=0, minute=1, second=0)
        t2 = datetime(year=2024, month=8, day=12, hour=0, minute=2, second=0)
        delta = datetime_utils.time_diff(t1, t2)
        self.assertEqual(delta, 60)

        delta = datetime_utils.time_diff(t2, t1)
        self.assertEqual(delta, -60)

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

    def test_get_now(self):

        dt_now = datetime.today()
        td_now = timedelta(hours=dt_now.hour, minutes=dt_now.minute,
                           seconds=dt_now.second, days=dt_now.weekday())

        now = datetime_utils.DateTimeDelta.now()
        self.assertAlmostEqual(dt_now.second, now.dt.second, delta=1)
        self.assertAlmostEqual(td_now.seconds, now.td.seconds, delta=1)

        now = datetime_utils.DateTimeDelta.now(offset=5)
        self.assertAlmostEqual(td_now.seconds + 5, now.td.seconds, delta=1)
        self.assertAlmostEqual(dt_now.second + 5, now.dt.second, delta=1)

        now = datetime_utils.DateTimeDelta.now(offset=-5)
        self.assertAlmostEqual(td_now.seconds - 5, now.td.seconds, delta=1)
        self.assertAlmostEqual(dt_now.second - 5, now.dt.second, delta=1)

    def test_parse_date_from_xbmcdialog(self):

        dt = datetime_utils.parse_date_from_xbmcdialog("1/1/1970")
        self.assertEqual(dt, datetime(year=1970, month=1, day=1))

        dt = datetime_utils.parse_date_from_xbmcdialog("31/1/1970")
        self.assertEqual(dt, datetime(year=1970, month=1, day=31))

        dt = datetime_utils.parse_date_from_xbmcdialog("1/12/1970")
        self.assertEqual(dt, datetime(year=1970, month=12, day=1))

        dt = datetime_utils.parse_date_from_xbmcdialog("31/12/1970")
        self.assertEqual(dt, datetime(year=1970, month=12, day=31))

    def test_convert_for_xbmcdialog(self):

        s = datetime_utils.convert_for_xbmcdialog("1970-01-01")
        self.assertEqual(s, " 1/ 1/1970")

        s = datetime_utils.convert_for_xbmcdialog("1970-01-31")
        self.assertEqual(s, "31/ 1/1970")

        s = datetime_utils.convert_for_xbmcdialog("1970-12-01")
        self.assertEqual(s, " 1/12/1970")

        s = datetime_utils.convert_for_xbmcdialog("1970-12-31")
        self.assertEqual(s, "31/12/1970")
