import unittest

from resources.lib.test.mockplayer import VIDEO, MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START_STOP)
from resources.lib.utils.datetime_utils import (DateTimeDelta,
                                                parse_datetime_str)


class TestSchedulerActions_7_1(unittest.TestCase):

    _t = ["%i:00" % i for i in range(10)]
    _dtd = [DateTimeDelta(parse_datetime_str("2023-01-02 %s" % s)) for s in _t]

    def test_tc_7_1_1(self):
        """
        Timer 1           |-------------------------|  Prio 1
        Timer 2                  |------|              Prio 0

        t       |---------|--T1--|--T1--|---T1------|---------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play
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
                "resume": True,
                "shuffle": False,
                "start": self._t[1],
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
                "resume": True,
                "shuffle": False,
                "start": self._t[3],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 80
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
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(VIDEO).state, None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(VIDEO).state, None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(VIDEO).state, None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[4])
        schedulderaction.perform(self._dtd[4])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(VIDEO).state, None)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(timers, self._dtd[5])
        schedulderaction.perform(self._dtd[5])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(VIDEO).state, None)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(VIDEO).state, None)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(timers, self._dtd[7])
        schedulderaction.perform(self._dtd[7])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(timers, self._dtd[8])
        schedulderaction.perform(self._dtd[8])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()
