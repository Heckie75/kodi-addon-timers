import unittest

from resources.lib.test.mockplayer import AUDIO, PICTURE, VIDEO
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.concurrency import determine_overlappings
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START,
                                       MEDIA_ACTION_START_AT_END,
                                       MEDIA_ACTION_START_STOP,
                                       MEDIA_ACTION_STOP,
                                       MEDIA_ACTION_STOP_AT_END,
                                       MEDIA_ACTION_STOP_START)
from resources.lib.utils.datetime_utils import (DateTimeDelta,
                                                parse_datetime_str)


class TestSchedulerActions_8_1(unittest.TestCase):

    _t = ["%i:00" % i for i in range(10)]
    _dtd = [DateTimeDelta(parse_datetime_str("2023-01-02 %s" % s)) for s in _t]

    def test_tc_8_1_1(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                S---------X                      start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_1_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                S--------->                      start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_1_3(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                |---------S                      start-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_1_4(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                X---------S                      stop-start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_1_5(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                |---------X                      stop-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_1_6(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                X---------|                      stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_2_1(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      S---------X                                start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_2_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      S--------->                                start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_2_3(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      |---------S                                start-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_2_4(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      X---------S                                stop-start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_2_5(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      |---------X                                stop-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_2_6(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      X---------|                                stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_3_1(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               S---------X       start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_3_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               S--------->       start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_3_3(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               |---------S       start-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_3_4(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               X---------S       stop-start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_3_5(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               |---------X       stop-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_3_6(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               X---------|       stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_4_1(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                S---------X                      start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_4_2(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                S--------->                      start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_4_3(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                |---------S                      start-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_4_4(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                X---------S                      stop-start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_4_5(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                |---------X                      stop-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_4_6(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                X---------|                      stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_5_1(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      S---------X                                start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_5_2(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      S--------->                                start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_5_3(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      |---------S                                start-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_5_4(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      X---------S                                stop-start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_5_5(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      |---------X                                stop-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_5_6(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      X---------|                                stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[3],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[1],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_6_1(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               S---------X       start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_6_2(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               S--------->       start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_6_3(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               |---------S       start-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_6_4(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               X---------S       stop-start/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_6_5(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               |---------X       stop-at-end/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_6_6(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               X---------|       stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_STOP_START,
                "media_type": VIDEO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[8],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP,
                "media_type": VIDEO,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[6],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_7_1(self):
        """
        Timer 1           S------------------------X            start-stop/audio
        Timer 2                S---------X                      start-stop/picture

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[7],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OFF,
                "id": 1,
                "label": "Timer 1",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": AUDIO,
                "notify": True,
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "media_type": PICTURE,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)

    def test_tc_8_7_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                S---------X                      start-stop/picture

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "media_type": PICTURE,
                "notify": True,
                "path": "/home/heckie/pictures/",
                "priority": 0,
                "repeat": False,
                "resume": False,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_7_3(self):
        """
        Timer 1           S------------------------R            start-stop/video
        Timer 2           S------------------------R            start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
                ],
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertTrue(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertTrue(b)

    def test_tc_8_7_4(self):
        """
        Timer 1           S--------------R                      start-stop/video
        Timer 2                          S---------R            start-stop/video

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "days": [
                    1
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": self._t[2],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            },
            {
                "days": [
                    1
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
                "path": "pvr://channels/radio/Alle%20Kan%C3%A4le/pvr.hts_976717008.pvr",
                "priority": 0,
                "repeat": False,
                "resume": True,
                "shuffle": False,
                "start": self._t[5],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        b = determine_overlappings(timers[0], timers[1:])
        self.assertFalse(b)

        b = determine_overlappings(timers[1], timers[:1])
        self.assertFalse(b)