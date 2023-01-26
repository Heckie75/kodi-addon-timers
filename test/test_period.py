import unittest
from datetime import timedelta

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
        self.assertEquals(td_start, timedelta(hours=-3))
        self.assertEquals(td_end, timedelta(hours=-4))
        self.assertIsNone(td_length)

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEquals(td_start, timedelta(hours=3))
        self.assertEquals(td_end, timedelta(hours=4))
        self.assertIsNone(td_length)

    def test_compare_2(self):
        """
        Period 1         |---------|
        Period 2                   |--------------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
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
        self.assertEquals(td_start, timedelta(hours=-2))
        self.assertEquals(td_end, timedelta(hours=-3))
        self.assertEquals(td_length, timedelta())

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEquals(td_start, timedelta(hours=2))
        self.assertEquals(td_end, timedelta(hours=3))
        self.assertEquals(td_length, timedelta())

    def test_compare_3(self):
        """
        Period 1         |---------|
        Period 2              |--------------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
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
        self.assertEquals(td_start, timedelta(hours=-1))
        self.assertEquals(td_end, timedelta(hours=-2))
        self.assertEquals(td_length, timedelta(hours=1))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEquals(td_start, timedelta(hours=1))
        self.assertEquals(td_end, timedelta(hours=2))
        self.assertEquals(td_length, timedelta(hours=1))

    def test_compare_4(self):
        """
        Period 1         |---------|
        Period 2         |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
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
        self.assertEquals(td_start, timedelta())
        self.assertEquals(td_end, timedelta())
        self.assertEquals(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEquals(td_start, timedelta())
        self.assertEquals(td_end, timedelta())
        self.assertEquals(td_length, timedelta(hours=2))

    def test_compare_5(self):
        """
        Period 1         |--------------|
        Period 2              |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
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
        self.assertEquals(td_start, timedelta(hours=-1))
        self.assertEquals(td_end, timedelta())
        self.assertEquals(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEquals(td_start, timedelta(hours=1))
        self.assertEquals(td_end, timedelta())
        self.assertEquals(td_length, timedelta(hours=2))

    def test_compare_6(self):
        """
        Period 1         |--------------|
        Period 2         |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
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
        self.assertEquals(td_start, timedelta())
        self.assertEquals(td_end, timedelta(hours=1))
        self.assertEquals(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEquals(td_start, timedelta())
        self.assertEquals(td_end, timedelta(hours=-1))
        self.assertEquals(td_length, timedelta(hours=2))

    def test_compare_7(self):
        """
        Period 1         |-------------------|
        Period 2              |---------|

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        data = [
            {
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
        self.assertEquals(td_start, timedelta(hours=-1))
        self.assertEquals(td_end, timedelta(hours=1))
        self.assertEquals(td_length, timedelta(hours=2))

        td_start, td_end, td_length = timers[1].periods[0].compare(
            timers[0].periods[0])
        self.assertEquals(td_start, timedelta(hours=1))
        self.assertEquals(td_end, timedelta(hours=-1))
        self.assertEquals(td_length, timedelta(hours=2))

    def test_hit_1(self):
        """
        Period 1         |---------|
        Timestamp   x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=1)

        s, e, b = period1.hit(timestamp)
        self.assertEquals(s, timedelta(hours=1))
        self.assertEquals(e, timedelta(hours=3))
        self.assertEquals(b, False)

    def test_hit_2(self):
        """
        Period 1         |---------|
        Timestamp        x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=2)

        s, e, b = period1.hit(timestamp)
        self.assertEquals(s, timedelta(hours=0))
        self.assertEquals(e, timedelta(hours=2))
        self.assertEquals(b, True)

    def test_hit_3(self):
        """
        Period 1         |---------|
        Timestamp             x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=3)

        s, e, b = period1.hit(timestamp)
        self.assertEquals(s, timedelta(hours=-1))
        self.assertEquals(e, timedelta(hours=1))
        self.assertEquals(b, True)

    def test_hit_4(self):
        """
        Period 1         |---------|
        Timestamp                  x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=4)

        s, e, b = period1.hit(timestamp)
        self.assertEquals(s, timedelta(hours=-2))
        self.assertEquals(e, timedelta(hours=0))
        self.assertEquals(b, True)

    def test_hit_5(self):
        """
        Period 1         |---------|
        Timestamp                       x

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
        """

        period1 = Period(timedelta(hours=2), timedelta(hours=4))
        timestamp = timedelta(hours=5)

        s, e, b = period1.hit(timestamp)
        self.assertEquals(s, timedelta(hours=-3))
        self.assertEquals(e, timedelta(hours=-1))
        self.assertEquals(b, False)
