import unittest
from datetime import datetime

from resources.lib.test.mockplayer import AUDIO, PICTURE, VIDEO, MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.concurrency import determine_overlappings
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START,
                                       MEDIA_ACTION_START_AT_END,
                                       MEDIA_ACTION_START_STOP,
                                       MEDIA_ACTION_STOP,
                                       MEDIA_ACTION_STOP_AT_END,
                                       MEDIA_ACTION_STOP_START)
from resources.lib.utils.datetime_utils import (DateTimeDelta,
                                                parse_datetime_str)


class TestSchedulerActions_8_4(unittest.TestCase):

    _t = ["%i:00" % i for i in range(10)]
    _dtd = [DateTimeDelta(parse_datetime_str("2024-08-15 %s" % s)) for s in _t]
    _now = datetime(year=2024, month=8, day=15, hour=0, minute=0, second=0)

    def test_tc_8_4_1_1(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                S---------X                      start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_1_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                S--------->                      start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_1_3(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                |---------S                      start-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_1_4(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                X---------S                      stop-start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_1_5(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                |---------X                      stop-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_1_6(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                X---------|                      stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_2_1(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      S---------X                                start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_2_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      S--------->                                start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_2_3(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      |---------S                                start-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_2_4(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      X---------S                                stop-start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_2_5(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      |---------X                                stop-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        player = MockPlayer()
        player.setVolume(100)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # test overlapping
        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

    def test_tc_8_4_2_6(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      X---------|                                stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_3_1(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               S---------X       start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_3_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               S--------->       start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_3_3(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               |---------S       start-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_3_4(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               X---------S       stop-start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_3_5(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               |---------X       stop-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_3_6(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                               X---------|       stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_4_1(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                S---------X                      start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_4_2(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                S--------->                      start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_4_3(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                |---------S                      start-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_4_4(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                X---------S                      stop-start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_4_5(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                |---------X                      stop-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_4_6(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                X---------|                      stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_5_1(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      S---------X                                start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_5_2(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      S--------->                                start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_5_3(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      |---------S                                start-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_5_4(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      X---------S                                stop-start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_5_5(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      |---------X                                stop-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_5_6(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2      X---------|                                stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_6_1(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               S---------X       start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_6_2(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               S--------->       start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_6_3(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               |---------S       start-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_6_4(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               X---------S       stop-start/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_6_5(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               |---------X       stop-at-end/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_6_6(self):
        """
        Timer 1           X------------------------S            stop-start/video
        Timer 2                               X---------|       stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_7_1(self):
        """
        Timer 1           S------------------------X            start-stop/audio
        Timer 2                S---------X                      start-stop/picture by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

    def test_tc_8_4_7_2(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2                S---------X                      start-stop/picture by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_7_3(self):
        """
        Timer 1           S------------------------R            start-stop/video
        Timer 2           S------------------------R            start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertTrue(b)

    def test_tc_8_4_7_4(self):
        """
        Timer 1           S--------------R                      start-stop/video
        Timer 2                          S---------R            start-stop/video by date

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
        """

        data = [
            {
                "date": "",
                "days": [
                    3
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
                "date": "2024-08-15",
                "days": [
                    8
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

        b = determine_overlappings(
            timers[0], timers[1:], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_4._now)
        self.assertFalse(b)
