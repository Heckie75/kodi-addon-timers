import unittest
from datetime import datetime, timedelta

from resources.lib.player.mediatype import AUDIO, PICTURE, VIDEO
from resources.lib.test.mockplayer import MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION,
                                       FADE_OUT_FROM_CURRENT,
                                       MEDIA_ACTION_START_STOP, STATE_ENDING,
                                       STATE_RUNNING, STATE_STARTING,
                                       STATE_WAITING, SYSTEM_ACTION_NONE,
                                       Period, Timer)
from resources.lib.utils.datetime_utils import DateTimeDelta


class TestSchedulerActions_1_3(unittest.TestCase):

    _t0 = 0
    _t1 = 60
    _t2 = 120
    _t3 = 180
    _t4 = 240
    _t5 = 300
    _t6 = 360
    _t7 = 420
    _t8 = 480
    _t9 = 520
    _t10 = 600

    def test_tc_1_3(self):
        """
        TC 1.3. Single timer w/o resume and w/ former media

        Media 1 |---------|                                         (tested w/ PVR and Playlist)
        Timer 1           |-----------------X                       (tested w/ PVR and Playlist)

        t       |----M1---|-------T1--------|---------------->
                t0        t1       t2       t3       t4
        Player            play              stop

        Fader   80        T1(=)-----------T1(40)
        """

        # ------------ setup player ------------
        player = MockPlayer()
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)
        player.setVolume(80)

        schedulderaction = SchedulerAction(player, MockStorage())

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t3 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.resume = False
        timer1.fade = FADE_OUT_FROM_CURRENT
        timer1.vol_min = 40
        timer1.vol_max = None
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t3))]

        timers = [timer1]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.label, timers[0].label)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.label, timers[0].label)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)
        self.assertEqual(player.getVolume(), 80)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 60)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(
            len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(
            schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()
