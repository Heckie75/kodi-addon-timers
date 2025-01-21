import unittest

from datetime import datetime

from resources.lib.test.mockplayer import VIDEO
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START_STOP)
from resources.lib.utils import housekeeper


class TestHousekeeper(unittest.TestCase):

    def test_cleaner_by_date_outdated(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-17 15:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_DELETE)

    def test_cleaner_by_date_outdated_today(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 11:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_DELETE)

    def test_cleaner_by_date_running(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 09:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)
        self.assertEqual(timers[0].date, "2024-08-15")

        self.assertEqual(action, housekeeper.ACTION_NOTHING)

    def test_cleaner_upcoming_today(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 03:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_NOTHING)
        self.assertEqual(timers[0].date, "2024-08-15")

    def test_cleaner_upcoming_next_week(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-05 03:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_NOTHING)
        self.assertEqual(timers[0].date, "2024-08-15")

    def test_cleaner_weekly_timer(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    0, 1, 2, 3, 4, 5, 6, 7
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-09-30 03:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_NOTHING)
        self.assertEqual(timers[0].date, "")

    def test_cleaner_timer_by_weekdays_all_outdated(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-09-30 03:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_DELETE)

    def test_cleaner_timer_by_weekdays_keep_all(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 09:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_NOTHING)
        self.assertEqual(timers[0].date, "2024-08-15")

    def test_cleaner_timer_by_weekdays_keep_all_same_day(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 05:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_NOTHING)
        self.assertEqual(timers[0].date, "2024-08-15")

    def test_cleaner_timer_by_weekdays_keep_all_threshold_except_same_day(self):
        data = [
            {
                "date": "2024-08-15",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 11:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_UPDATE)
        self.assertEqual(timers[0].days, [0, 1, 2, 4, 5, 6])
        self.assertEqual(timers[0].date, "2024-08-16")

    def test_cleaner_timer_by_weekdays_keep_some(self):
        data = [
            {
                "date": "2024-08-12",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 11:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_UPDATE)
        self.assertEqual(timers[0].date, "2024-08-16")
        self.assertEqual(timers[0].days, [4, 5, 6])

    def test_cleaner_timer_by_weekdays_keep_some_w_one_running(self):
        data = [
            {
                "date": "2024-08-14",
                "days": [
                    2, 3, 4, 5, 6
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 09:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_UPDATE)
        self.assertEqual(timers[0].date, "2024-08-15")
        self.assertEqual(timers[0].days, [3, 4, 5, 6])

    def test_cleaner_timer_by_weekdays_keep_by_date_2(self):
        data = [
            {
                "date": "2024-08-18",
                "days": [8],
                "duration": "02:00",
                "duration_offset": 0,
                "end": "10:00",
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": "08:00",
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()
        threshold = datetime.strptime("2024-08-15 11:00", "%Y-%m-%d %H:%M")

        action = housekeeper.check_timer(timers[0], threshold=threshold)

        self.assertEqual(action, housekeeper.ACTION_NOTHING)
        self.assertEqual(timers[0].date, "2024-08-18")
