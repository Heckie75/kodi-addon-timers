import unittest

from resources.lib.utils.datetime_utils import DateTimeDelta
from datetime import datetime, timedelta

from resources.lib.player.mediatype import VIDEO
from resources.lib.player.player_utils import REPEAT_ALL, REPEAT_OFF
from resources.lib.test.mockplayer import MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION, FADE_OFF,
                                       FADE_OUT_FROM_CURRENT,
                                       MEDIA_ACTION_START_STOP,
                                       MEDIA_ACTION_STOP_AT_END, STATE_ENDING,
                                       STATE_RUNNING, STATE_STARTING,
                                       STATE_WAITING, SYSTEM_ACTION_NONE,
                                       Period, Timer)


class TestSchedulerActions_4_3(unittest.TestCase):

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

    def test_tc_4_3_1(self):
        """
        Media 1 |---------|
        Timer 1           |-------------------------X
        Timer 2                  |------X

        t       |----M1---|--T1--|--T2--|-----------|---------------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play   play   stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)
        player.setDefaultVolume(100)
        player.setVolume(80)

        schedulderaction = SchedulerAction(player, MockStorage())

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.resume = False
        timer1.fade = FADE_OUT_FROM_CURRENT
        timer1.vol_min = 20
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t7))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t5 - self._t3)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Media T2"
        timer2.media_type = VIDEO
        timer2.repeat = False
        timer2.resume = False
        timer2.fade = FADE_OFF
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t5))]

        timers = [timer1, timer2]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertNotEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertNotEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 70)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertNotEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 60)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertNotEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 50)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertNotEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 40)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertNotEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 30)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 80)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 80)

        schedulderaction.reset()

    def test_tc_4_3_2(self):
        """
        Media 1 |---------|
        Timer 1           |-------------------------X
        Timer 2                  |------R

        t       |----M1---|--T1--|--T2--|---T1------|---------------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play   play   resume      stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        player.setSeekDelayedTimer(True)
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)
        player.setDefaultVolume(100)
        player.setShuffled(True)
        player.setRepeat(REPEAT_ALL)

        schedulderaction = SchedulerAction(player, MockStorage())

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1.1 (0:39)|Media T1.2 (0:37)|Media T1.3 (0:27)"
        timer1.media_type = VIDEO
        timer1.repeat = True
        timer1.shuffle = False
        timer1.resume = False
        timer1.fade = FADE_OFF
        timer1.vol_min = 0
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t7))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t5 - self._t3)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Media T2"
        timer2.media_type = VIDEO
        timer2.repeat = False
        timer2.shuffle = False
        timer2.resume = True
        timer2.fade = FADE_OFF
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t5))]

        timers = [timer1, timer2]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))
        player._td_now = timedelta(minutes=self._t1)

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path.split("|")[0])
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))
        player._td_now = timedelta(minutes=self._t2)

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path.split("|")[0])
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))
        player._td_now = timedelta(minutes=self._t3)

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[1].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], timers[0].path.split("|")[0])
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))
        player._td_now = timedelta(minutes=self._t4)

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[1].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], timers[0].path.split("|")[0])
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))
        player._td_now = timedelta(minutes=self._t5)

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].position, 1)
        self.assertEqual(apwpl[VIDEO].time, 1320)
        self.assertEqual(apwpl[VIDEO].playlist[1]
                         ["file"], timers[0].path.split("|")[1])
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))
        player._td_now = timedelta(minutes=self._t6)

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[1]
                         ["file"], timers[0].path.split("|")[1])
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))
        player._td_now = timedelta(minutes=self._t7)

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))
        player._td_now = timedelta(minutes=self._t8)

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        player.play(playlist)
        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

    def test_tc_4_3_3(self):
        """
        Media 1 |---------|
        Timer 1           |-------------------------R
        Timer 2                  |------X

        t       |----M1---|--T1--|--T2--|-----------|---------------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play   play   stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)
        player.setDefaultVolume(100)

        schedulderaction = SchedulerAction(player, MockStorage())

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.resume = True
        timer1.fade = FADE_OFF
        timer1.vol_min = 0
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t7))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t5 - self._t3)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Media T2"
        timer2.media_type = VIDEO
        timer2.repeat = False
        timer2.resume = False
        timer2.fade = FADE_OFF
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t5))]

        timers = [timer1, timer2]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

    def test_tc_4_3_4(self):
        """
        Timer 1           |-------------------------R
        Timer 2                  |------X

        t       |----M1---|--T1--|--T2--|-----------|---------------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play   play   stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player, MockStorage())
        player.setVolume(100)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.resume = True
        timer1.fade = FADE_OFF
        timer1.vol_min = 0
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t7))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t5 - self._t3)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Media T2"
        timer2.media_type = VIDEO
        timer2.repeat = False
        timer2.resume = False
        timer2.fade = FADE_OFF
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t5))]

        timers = [timer1, timer2]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

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
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

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
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

    def test_tc_4_3_5(self):
        """
        Timer 1           |-------------------------X
        Timer 2                  |------R

        t       |----M1---|--T1--|--T2--|---T1------|---------------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play   play   resume      stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player, MockStorage())
        player.setVolume(100)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.resume = False
        timer1.fade = FADE_OFF
        timer1.vol_min = 0
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t7))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t5 - self._t3)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Media T2"
        timer2.media_type = VIDEO
        timer2.repeat = False
        timer2.resume = True
        timer2.fade = FADE_OFF
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t5))]

        timers = [timer1, timer2]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[1].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], timers[0].path)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[1].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], timers[0].path)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

    def test_tc_4_3_6(self):
        """
        Media 1 |---------|
        Timer 1           |-------------R
        Timer 2                  |------------------X      (Fader, no media)
        Timer 3                         |-----------R

        t       |----M1---|----T1-------|-----T3----|---------------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play          play        stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)
        player.setDefaultVolume(100)

        schedulderaction = SchedulerAction(player, MockStorage())

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t5 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.resume = True
        timer1.fade = FADE_OFF
        timer1.vol_min = 0
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t5))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t7 - self._t3)
        timer2.media_action = MEDIA_ACTION_STOP_AT_END
        timer2.path = ""
        timer2.media_type = VIDEO
        timer2.repeat = False
        timer2.resume = False
        timer2.fade = FADE_OUT_FROM_CURRENT
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t7))]

        # Timer 3 (T3)
        timer3 = Timer(3)
        timer3.label = "Timer 3"
        timer3.end_type = END_TYPE_DURATION
        timer3.duration_timedelta = timedelta(minutes=self._t7 - self._t5)
        timer3.media_action = MEDIA_ACTION_START_STOP
        timer3.path = "Media T3"
        timer3.media_type = VIDEO
        timer3.repeat = False
        timer3.resume = True
        timer3.fade = FADE_OFF
        timer3.vol_min = 0
        timer3.vol_max = 100
        timer3.system_action = SYSTEM_ACTION_NONE
        timer3.active = False
        timer3.notify = False
        timer3.periods = [
            Period(timedelta(days=3, minutes=self._t5), timedelta(days=3, minutes=self._t7))]

        timers = [timer1, timer2, timer3]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV.id, timer1.id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T1")
        self.assertEqual(player.getVolume(), 75)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(timers[2].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV.id, timer3.id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T3")
        self.assertEqual(player.getVolume(), 50)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(timers[2].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T3")
        self.assertEqual(player.getVolume(), 25)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(timers[2].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 2)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV.id, timer2.id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

    def test_tc_4_3_7(self):
        """
        Media 1 |---------|                         |---------------->
        Timer 1           |-------------R
        Timer 2                  |------------------R               (Fader with media)
        Timer 3                         |-----------R

        t       |----M1---|--T1--|--T2--|------T3---|------M1-------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play          play        play
        """

        # ------------ setup player ------------
        player = MockPlayer()
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)
        player.setDefaultVolume(100)

        schedulderaction = SchedulerAction(player, MockStorage())

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t5 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.resume = True
        timer1.fade = FADE_OFF
        timer1.vol_min = 0
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t5))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t7 - self._t3)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Media T2"
        timer2.media_type = VIDEO
        timer2.repeat = False
        timer2.resume = True
        timer2.fade = FADE_OUT_FROM_CURRENT
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t7))]

        # Timer 3 (T3)
        timer3 = Timer(3)
        timer3.label = "Timer 3"
        timer3.end_type = END_TYPE_DURATION
        timer3.duration_timedelta = timedelta(minutes=self._t7 - self._t5)
        timer3.media_action = MEDIA_ACTION_START_STOP
        timer3.path = "Media T3"
        timer3.media_type = VIDEO
        timer3.repeat = False
        timer3.resume = True
        timer3.fade = FADE_OFF
        timer3.vol_min = 0
        timer3.vol_max = 100
        timer3.system_action = SYSTEM_ACTION_NONE
        timer3.active = False
        timer3.notify = False
        timer3.periods = [
            Period(timedelta(days=3, minutes=self._t5), timedelta(days=3, minutes=self._t7))]

        timers = [timer1, timer2, timer3]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV.id, timer1.id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV.id, timer2.id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T2")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T2")
        self.assertEqual(player.getVolume(), 75)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(timers[2].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV.id, timer3.id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T3")
        self.assertEqual(player.getVolume(), 50)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(timers[2].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.id, timer2.id)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media T3")
        self.assertEqual(player.getVolume(), 25)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(timers[2].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 2)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV.id, timer3.id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(timers[2].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()
