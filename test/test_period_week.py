import unittest
from datetime import datetime

from resources.lib.test.mockplayer import VIDEO
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START_STOP, Timer)
from resources.lib.utils.datetime_utils import DateTimeDelta


class TestPeriodWeek(unittest.TestCase):

    def test_hit_1(self):
        """
        Timer 1                    |--|
        Timer 2                     |--|                                 (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
                Mon Tue  Wed  Thu  Fri  Sat  Sun  Mon  Tue  Wed  Thu
                         Now
        """

        data = [
            {
                "date": "",
                "days": [
                    4,
                    5,
                    6
                ],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "07:00",
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
                "start": "01:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-23",
                "days": [8],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "08:00",
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
                "start": "02:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        now = datetime(year=2024, month=8, day=21, hour=0)
        dtd = DateTimeDelta(now)

        storage = MockStorage(data=data)
        timers: 'list[Timer]' = storage.load_timers_from_storage()

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, now)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, now)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, now)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, now)
        self.assertEqual(b, True)
        
    def test_hit_2(self):
        """
        Timer 1          |--|                               |--|
        Timer 2           |--|                                           (by date)
        Timer 3                                              |--|        (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
                Mon Tue  Wed  Thu  Fri  Sat  Sun  Mon  Tue  Wed  Thu
                    Now
        """

        data = [
            {
                "date": "",
                "days": [
                    2,
                    7
                ],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "07:00",
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
                "start": "01:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-14",
                "days": [8],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "08:00",
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
                "start": "02:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-21",
                "days": [8],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "08:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 3",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": "02:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        now = datetime(year=2024, month=8, day=13, hour=0)
        dtd = DateTimeDelta(now)

        storage = MockStorage(data=data)
        timers: 'list[Timer]' = storage.load_timers_from_storage()

        # ------------------ t2 ------------------
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, now)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, now)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, now)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, now)
        self.assertEqual(b, True)
        

        # ------------------ t9 ------------------
        s, e, b = timers[0].periods[0].hit(timers[2].periods[0].start, now)
        self.assertEqual(b, False) # known issue, no forecast

        s, e, b = timers[0].periods[0].hit(timers[2].periods[0].end, now)
        self.assertEqual(b, False)

        s, e, b = timers[2].periods[0].hit(timers[0].periods[0].start, now)
        self.assertEqual(b, False)

        s, e, b = timers[2].periods[0].hit(timers[0].periods[0].end, now)
        self.assertEqual(b, False) # known issue, no forecast
        
    def test_hit_3(self):
        """
        Timer 1          |--|                               |--|
        Timer 2           |--|                                           (by date)
        Timer 3                                              |--|        (by date)

        t       |---t1---t2---t3---t4---t5---t6---t7---t8---t9---t10--->
                Mon Tue  Wed  Thu  Fri  Sat  Sun  Mon  Tue  Wed  Thu
                              Now
        """

        data = [
            {
                "date": "",
                "days": [
                    2,
                    7
                ],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "07:00",
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
                "start": "01:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-14",
                "days": [8],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "08:00",
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
                "start": "02:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            },
            {
                "date": "2024-08-21",
                "days": [8],
                "duration": "06:00",
                "duration_offset": 0,
                "end": "08:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 3",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "videodb://2/2/2.mp3",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": "02:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
            }
        ]

        now = datetime(year=2024, month=8, day=15, hour=0)
        dtd = DateTimeDelta(now)

        storage = MockStorage(data=data)
        timers: 'list[Timer]' = storage.load_timers_from_storage()

        # ------------------ t2 ------------------
        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].start, now)
        self.assertEqual(b, False) # known issue, no 'forecast' in the past

        s, e, b = timers[0].periods[0].hit(timers[1].periods[0].end, now)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].start, now)
        self.assertEqual(b, False)

        s, e, b = timers[1].periods[0].hit(timers[0].periods[0].end, now)
        self.assertEqual(b, False) # known issue, no 'forecast' in the past
        

        # ------------------ t9 ------------------
        s, e, b = timers[0].periods[0].hit(timers[2].periods[0].start, now)
        self.assertEqual(b, True)

        s, e, b = timers[0].periods[0].hit(timers[2].periods[0].end, now)
        self.assertEqual(b, False)

        s, e, b = timers[2].periods[0].hit(timers[0].periods[0].start, now)
        self.assertEqual(b, False)

        s, e, b = timers[2].periods[0].hit(timers[0].periods[0].end, now)
        self.assertEqual(b, True)
        
