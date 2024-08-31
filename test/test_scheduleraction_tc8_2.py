import unittest

from resources.lib.test.mockplayer import AUDIO, PICTURE, VIDEO, MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START_STOP)
from resources.lib.utils.datetime_utils import (DateTimeDelta,
                                                parse_datetime_str)


class TestSchedulerActions_8_2(unittest.TestCase):

    _t = ["%i:00" % i for i in range(10)]
    _dtd = [DateTimeDelta(parse_datetime_str("2023-01-02 %s" % s)) for s in _t]

    def test_tc_8_2_1(self):
        """
        Timer 1           S----R            start-stop/video   (prio 0)
        Timer 2           S---------R       start-stop/audio   (prio -1)
        Timer 3      S--------------R       start-stop/picture (prio -1)

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
                "end": self._t[3],
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
                "id": 2,
                "label": "Timer 2",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": AUDIO,
                "notify": True,
                "path": "/music/song.mp3",
                "priority": -1,
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
                "fade": FADE_OFF,
                "id": 3,
                "label": "Timer 3",
                "media_action": MEDIA_ACTION_START_STOP,
                "media_type": PICTURE,
                "notify": True,
                "path": "/pictures/",
                "priority": -1,
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
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)

        storage = MockStorage(data=data)
        timers = storage.load_timers_from_storage()

        schedulderaction = SchedulerAction(player, storage)

        # ------------ t0 ------------
        schedulderaction.calculate(timers, self._dtd[0])
        schedulderaction.perform(self._dtd[0])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], data[2]["path"])
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(PICTURE in apwpl, False)
        self.assertEqual(AUDIO in apwpl, False)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 2)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]["file"], data[1]["path"])
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], data[2]["path"])
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(timers, self._dtd[0])
        schedulderaction.perform(self._dtd[0])

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
