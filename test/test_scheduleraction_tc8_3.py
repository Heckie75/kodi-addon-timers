import unittest

from datetime import datetime

from resources.lib.test.mockplayer import VIDEO, MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.concurrency import determine_overlappings
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       FADE_OUT_FROM_CURRENT,
                                       MEDIA_ACTION_START_STOP,
                                       MEDIA_ACTION_STOP_AT_END)
from resources.lib.utils.datetime_utils import (DateTimeDelta,
                                                parse_datetime_str)


class TestSchedulerActions_8_3(unittest.TestCase):

    _t = ["%i:00" % i for i in range(10)]
    _dtd = [DateTimeDelta(parse_datetime_str("2024-08-15 %s" % s)) for s in _t]
    _now = datetime(year=2024, month=8, day=15, hour=0, minute=0, second=0)

    def test_tc_8_3_1(self):
        """
        Timer 1           S---------X       start-stop/video  (prio 0)
        Timer 2      F--------------X       fading-only-timer (prio 10)

        t       |----|----|----|----|----|
                t0   t1   t2   t3   t4   t5
        """

        data = [
            {
                "date": "",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
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
                "path": "/music/song.mp3",
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
                "date": "",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[4],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OUT_FROM_CURRENT,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "",
                "priority": 10,
                "repeat": False,
                "resume": True,
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

        # ------------ t0 ------------
        schedulderaction.calculate(timers, self._dtd[0])
        schedulderaction.perform(self._dtd[0])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 92)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 83)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 100)

    def test_tc_8_3_2(self):
        """
        Timer 1           S---------X       start-stop/video  (prio 0)
        Timer 2      F-------------------X  fading-only-timer (prio 10)

        t       |----|----|----|----|----|
                t0   t1   t2   t3   t4   t5
        """

        data = [
            {
                "date": "",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
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
                "path": "/music/song.mp3",
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
                "date": "",
                "days": [
                    0, 1, 2, 3, 4, 5, 6
                ],
                "duration": "01:00",
                "duration_offset": 0,
                "end": self._t[5],
                "end_offset": 0,
                "end_type": END_TYPE_TIME,
                "fade": FADE_OUT_FROM_CURRENT,
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_STOP_AT_END,
                "media_type": VIDEO,
                "notify": True,
                "path": "",
                "priority": 10,
                "repeat": False,
                "resume": True,
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

        # ------------ t0 ------------
        schedulderaction.calculate(timers, self._dtd[0])
        schedulderaction.perform(self._dtd[0])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 94)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 88)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 81)

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 100)


    def test_tc_8_3_3(self):
        """
        Timer 1           S------------------------X            start-stop/video
        Timer 2      S---------X                                start-stop/video by date (Prio 10)

        t       |----|----|----|----|----|----|----|----|----|
                t0   t1   t2   t3   t4   t5   t6   t7   t8   t9
                     play play stop
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
                "priority": 10,
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
            timers[0], timers[1:], base=TestSchedulerActions_8_3._now)
        self.assertTrue(b)

        b = determine_overlappings(
            timers[1], timers[:1], base=TestSchedulerActions_8_3._now)
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
                         ["file"], timers[1].path)
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