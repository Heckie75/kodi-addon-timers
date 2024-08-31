import unittest
from datetime import datetime, timedelta

from resources.lib.test.mockplayer import VIDEO
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.period import Period
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START_STOP)


class TestPeriod(unittest.TestCase):

    _t = ["%i:00" % i for i in range(10)]

    def test_compare_1(self):
        """
        Period 1         |---------|
        Period 2                        |--------------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[5],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        td_start, td_end, td_length = timers[0].periods[0].compare(
            timers[1].periods[0])
        self.assertEqual(td_start, timedelta(hours=-3))
        self.assertEqual(td_end, timedelta(hours=-4))
        self.assertIsNone(td_length)

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEqual(td_start, timedelta(hours=3))
        self.assertEqual(td_end, timedelta(hours=4))
        self.assertIsNone(td_length)

    def test_compare_2(self):
        """
        Period 1         |---------|
        Period 2                   |--------------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[4],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        td_start, td_end, td_length = timers[0].periods[0].compare(
            timers[1].periods[0])
        self.assertEqual(td_start, timedelta(hours=-2))
        self.assertEqual(td_end, timedelta(hours=-3))
        self.assertEqual(td_length, timedelta())

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEqual(td_start, timedelta(hours=2))
        self.assertEqual(td_end, timedelta(hours=3))
        self.assertEqual(td_length, timedelta())

    def test_compare_3(self):
        """
        Period 1         |---------|
        Period 2              |--------------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[6],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        td_start, td_end, td_length = timers[0].periods[0].compare(
            timers[1].periods[0])
        self.assertEqual(td_start, timedelta(hours=-1))
        self.assertEqual(td_end, timedelta(hours=-2))
        self.assertEqual(td_length, timedelta(hours=1))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEqual(td_start, timedelta(hours=1))
        self.assertEqual(td_end, timedelta(hours=2))
        self.assertEqual(td_length, timedelta(hours=1))

    def test_compare_4(self):
        """
        Period 1         |---------|
        Period 2         |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        td_start, td_end, td_length = timers[0].periods[0].compare(
            timers[1].periods[0])
        self.assertEqual(td_start, timedelta())
        self.assertEqual(td_end, timedelta())
        self.assertEqual(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEqual(td_start, timedelta())
        self.assertEqual(td_end, timedelta())
        self.assertEqual(td_length, timedelta(hours=2))

    def test_compare_5(self):
        """
        Period 1         |--------------|
        Period 2              |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        td_start, td_end, td_length = timers[0].periods[0].compare(
            timers[1].periods[0])
        self.assertEqual(td_start, timedelta(hours=-1))
        self.assertEqual(td_end, timedelta())
        self.assertEqual(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEqual(td_start, timedelta(hours=1))
        self.assertEqual(td_end, timedelta())
        self.assertEqual(td_length, timedelta(hours=2))

    def test_compare_6(self):
        """
        Period 1         |--------------|
        Period 2         |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        td_start, td_end, td_length = timers[0].periods[0].compare(
            timers[1].periods[0])
        self.assertEqual(td_start, timedelta())
        self.assertEqual(td_end, timedelta(hours=1))
        self.assertEqual(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEqual(td_start, timedelta())
        self.assertEqual(td_end, timedelta(hours=-1))
        self.assertEqual(td_length, timedelta(hours=2))

    def test_compare_7(self):
        """
        Period 1         |-------------------|
        Period 2              |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[6],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        td_start, td_end, td_length = timers[0].periods[0].compare(
            timers[1].periods[0])
        self.assertEqual(td_start, timedelta(hours=-1))
        self.assertEqual(td_end, timedelta(hours=1))
        self.assertEqual(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEqual(td_start, timedelta(hours=1))
        self.assertEqual(td_end, timedelta(hours=-1))
        self.assertEqual(td_length, timedelta(hours=2))

    def test_compare_exception(self):
        """
        Period 1         |-------------------|
        PeriodByDate 2        |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[6],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        try:
            timers[0].periods[0].compare(timers[1].periods[0])
            self.assertEquals(True, False)
        except Exception as e:
            self.assertEquals(str(
                e), "can't compare Period[start=2:00:00, end=6:00:00] with Period[start=2024-08-15 03:00:00, end=2024-08-15 05:00:00] caused by different types")
            self.assertEquals(True, True)

    def test_hit_1(self):
        """
        Period 1         |---------|
        Timestamp   x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=1)

        s, e, b = period1.hit(timestamp)
        self.assertEqual(s, timedelta(hours=1))
        self.assertEqual(e, timedelta(hours=3))
        self.assertEqual(b, False)

    def test_hit_2(self):
        """
        Period 1         |---------|
        Timestamp        x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=2)

        s, e, b = period1.hit(timestamp)
        self.assertEqual(s, timedelta(hours=0))
        self.assertEqual(e, timedelta(hours=2))
        self.assertEqual(b, True)

    def test_hit_3(self):
        """
        Period 1         |---------|
        Timestamp             x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=3)

        s, e, b = period1.hit(timestamp)
        self.assertEqual(s, timedelta(hours=-1))
        self.assertEqual(e, timedelta(hours=1))
        self.assertEqual(b, True)

    def test_hit_4(self):
        """
        Period 1         |---------|
        Timestamp                  x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=4)

        s, e, b = period1.hit(timestamp)
        self.assertEqual(s, timedelta(hours=-2))
        self.assertEqual(e, timedelta(hours=0))
        self.assertEqual(b, True)

    def test_hit_5(self):
        """
        Period 1         |---------|
        Timestamp                       x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=5)

        s, e, b = period1.hit(timestamp)
        self.assertEqual(s, timedelta(hours=-3))
        self.assertEqual(e, timedelta(hours=-1))
        self.assertEqual(b, False)

    def test_hit_6(self):
        """
        Timer 1         |-------------------|
        Timer 2               |---------|                                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[6],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        # Monday
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, True)

        # Friday
        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Timer 2 hits timer 1?
        # Monday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].end, base)
        self.assertEqual(b, False)

        # Friday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].end, base)
        self.assertEqual(b, False)

    def test_hit_7(self):
        """
        Timer 1                    |-------------------|
        Timer 2              |---------|                                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[4],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        # Monday
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, True)

        # Friday
        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Timer 2 hits timer 1?
        # Monday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].end, base)
        self.assertEqual(b, False)

        # Friday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].end, base)
        self.assertEqual(b, False)

    def test_hit_8(self):
        """
        Timer 1     |--------------|
        Timer 2              |---------|                                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        # Monday
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Friday
        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Timer 2 hits timer 1?
        # Monday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].end, base)
        self.assertEqual(b, True)

        # Friday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].end, base)
        self.assertEqual(b, False)

    def test_hit_9(self):
        """
        Timer 1                    |-------------------|
        Timer 2              |---------|                                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[4],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        # Monday
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, True)

        # Friday
        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Timer 2 hits timer 1?
        # Monday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].end, base)
        self.assertEqual(b, False)

        # Friday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].end, base)
        self.assertEqual(b, False)

    def test_hit_10(self):
        """
        Timer 1     |--------------|
        Timer 2                              |---------|                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        # Monday
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[1].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[2].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Friday
        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[4].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[5].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[6].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Timer 2 hits timer 1?
        # Monday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, False)

        # Tuesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[1].end, base)
        self.assertEqual(b, False)

        # Wednesday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[2].end, base)
        self.assertEqual(b, False)

        # Thursday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].end, base)
        self.assertEqual(b, False)

        # Friday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[4].end, base)
        self.assertEqual(b, False)

        # Saturday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[5].end, base)
        self.assertEqual(b, False)

        # Sunday
        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[6].end, base)
        self.assertEqual(b, False)

    def test_hit_11(self):
        """
        Timer 1     |--------------|                                     (by date)
        Timer 2                              |---------|                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Timer 2 hits timer 1?
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, False)

    def test_hit_12(self):
        """
        Timer 1                    |--------------|                      (by date)
        Timer 2                              |---------|                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[4],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, False)

        # Timer 2 hits timer 1?
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, True)

    def test_hit_13(self):
        """
        Timer 1                    |--------------|                      (by date)
        Timer 2               |---------|                                (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[4],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, False)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, True)

        # Timer 2 hits timer 1?
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, False)

    def test_hit_14(self):
        """
        Timer 1               |---------|                                (by date)
        Timer 2               |---------|                                (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, True)

        # Timer 2 hits timer 1?
        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start)
        self.assertEqual(b, True)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, base)
        self.assertEqual(b, True)

    def test_hit_15(self):
        """
        Timer 1               |---------|
        Timer 2               |---------|                                (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
                "date": "",
                "days": [0, 1, 2, 3, 4, 5, 6, 7],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://1/1/1.mp3",
                "priority": 1,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-15",
                "days": [8],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        base = datetime(year=2024, month=8, day=15, hour=1, minute=0)

        # Timer 1 hits timer 2?
        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[3].hit(timers[1].periods[0].end, base)
        self.assertEqual(b, True)

        # Timer 2 hits timer 1?
        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].start, base)
        self.assertEqual(b, True)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[3].end, base)
        self.assertEqual(b, True)
