import unittest

from resources.lib.test.mockplayer import VIDEO, MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_TIME, FADE_OFF,
                                       MEDIA_ACTION_START_STOP)
from resources.lib.utils.datetime_utils import (DateTimeDelta,
                                                parse_datetime_str)
from datetime import timedelta


class TestSchedulerActions_9_1(unittest.TestCase):

    _t = [f"{i % 24}:00" for i in range(48)]
    _dtd = [DateTimeDelta(parse_datetime_str("2024-08-15 00:00") + timedelta(hours=h)) for h in range(48)]

    def test_tc_9_1_1(self):
        """
        Timer 1      S---------X              start-stop/video  (prio 0)

        t       |----|----|----|----|----|
                t0   t1   t2   t3   t4   t5
        """

        data= [
            {
                "date": "2024-08-15",
                "days": [
                    8
                ],
                "duration": "02:00",
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
                "path": "/music/song.mp3",
                "priority": 0,
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

        player= MockPlayer()
        player.setVolume(100)

        storage= MockStorage(data=data)
        timers= storage.load_timers_from_storage()

        schedulderaction= SchedulerAction(player, storage)

        # ------------ t0 ------------
        schedulderaction.calculate(timers, self._dtd[0])
        schedulderaction.perform(self._dtd[0])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(timers, self._dtd[1])
        schedulderaction.perform(self._dtd[1])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(timers, self._dtd[2])
        schedulderaction.perform(self._dtd[2])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(timers, self._dtd[3])
        schedulderaction.perform(self._dtd[3])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(timers, self._dtd[6])
        schedulderaction.perform(self._dtd[6])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()


    def test_tc_9_1_2(self):
        """
        Timer 1      S---------X              start-stop/video  (prio 0)

        t       |----|----|----|----|----|
                t0   t23  t24  t25  t26  t27
        """

        data= [
            {
                "date": "2024-08-15",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": self._t[25],
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
                "start": self._t[23],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        player= MockPlayer()
        player.setVolume(100)

        storage= MockStorage(data=data)
        timers= storage.load_timers_from_storage()

        schedulderaction= SchedulerAction(player, storage)

        # ------------ t0 ------------
        schedulderaction.calculate(timers, self._dtd[0])
        schedulderaction.perform(self._dtd[0])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t23 ------------
        schedulderaction.calculate(timers, self._dtd[23])
        schedulderaction.perform(self._dtd[23])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t24 ------------
        schedulderaction.calculate(timers, self._dtd[24])
        schedulderaction.perform(self._dtd[24])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t25 ------------
        schedulderaction.calculate(timers, self._dtd[25])
        schedulderaction.perform(self._dtd[25])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t26 ------------
        schedulderaction.calculate(timers, self._dtd[26])
        schedulderaction.perform(self._dtd[26])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()


    def test_tc_9_1_3(self):
        """
        Timer 1           S---------X        start-stop/video  (prio 0)

        t       |----|----|----|----|----|
                t0   t23  t24  t25  t26  t27
        """

        data= [
            {
                "date": "2024-08-16",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": self._t[26],
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
                "start": self._t[24],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        player= MockPlayer()
        player.setVolume(100)

        storage= MockStorage(data=data)
        timers= storage.load_timers_from_storage()

        schedulderaction= SchedulerAction(player, storage)

        # ------------ t23 ------------
        schedulderaction.calculate(timers, self._dtd[23])
        schedulderaction.perform(self._dtd[23])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t24 ------------
        schedulderaction.calculate(timers, self._dtd[24])
        schedulderaction.perform(self._dtd[24])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t25 ------------
        schedulderaction.calculate(timers, self._dtd[25])
        schedulderaction.perform(self._dtd[25])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)


        # ------------ t26 ------------
        schedulderaction.calculate(timers, self._dtd[26])
        schedulderaction.perform(self._dtd[26])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()
        
        
    def test_tc_9_1_4(self):
        """
        Timer 1           S---------X        start-stop/video  (prio 0)

        t       |----|----|----|----|----|
                t23  t24  t25  t26  t27  t28
        """

        data= [
            {
                "date": "2024-08-16",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": self._t[27],
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
                "start": self._t[25],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        player= MockPlayer()
        player.setVolume(100)

        storage= MockStorage(data=data)
        timers= storage.load_timers_from_storage()

        schedulderaction= SchedulerAction(player, storage)

        # ------------ t24 ------------
        schedulderaction.calculate(timers, self._dtd[24])
        schedulderaction.perform(self._dtd[24])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t25 ------------
        schedulderaction.calculate(timers, self._dtd[25])
        schedulderaction.perform(self._dtd[25])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t26 ------------
        schedulderaction.calculate(timers, self._dtd[26])
        schedulderaction.perform(self._dtd[26])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)


        # ------------ t27 ------------
        schedulderaction.calculate(timers, self._dtd[27])
        schedulderaction.perform(self._dtd[27])

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()



    def test_tc_9_1_5(self):
        """
        Timer 1           S---------X        start-stop/video  (prio 0)

        t       |----|----|----|----|----|
                               t26  t27  t28
        """

        data= [
            {
                "date": "2024-08-16",
                "days": [
                    8
                ],
                "duration": "02:00",
                "duration_offset": 0,
                "end": self._t[27],
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
                "start": self._t[25],
                "start_offset": 0,
                "system_action": 0,
                "vol_max": 100,
                "vol_min": 75
            }
        ]

        player= MockPlayer()
        player.setVolume(100)

        storage= MockStorage(data=data)
        timers= storage.load_timers_from_storage()

        schedulderaction= SchedulerAction(player, storage)

        # ------------ t26 ------------
        schedulderaction.calculate(timers, self._dtd[26])
        self.assertEqual(timers[0].state, 1)
        schedulderaction.perform(self._dtd[26])
        self.assertEqual(timers[0].state, 2)

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], data[0]["path"])
        self.assertEqual(player.getVolume(), 100)


        # ------------ t27 ------------
        schedulderaction.calculate(timers, self._dtd[27])
        self.assertEqual(timers[0].state, 3)
        schedulderaction.perform(self._dtd[27])
        self.assertEqual(timers[0].state, 0)

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()
        
        # ------------ t28 ------------
        schedulderaction.calculate(timers, self._dtd[28])
        self.assertEqual(timers[0].state, 0)
        schedulderaction.perform(self._dtd[28])
        self.assertEqual(timers[0].state, 0)

        apwpl= player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(VIDEO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()        