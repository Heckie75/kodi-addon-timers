import unittest
from datetime import timedelta

from resources.lib.player.mediatype import AUDIO, VIDEO, PICTURE
from resources.lib.test.mockplayer import MockPlayer
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION, FADE_OFF,
                                       MEDIA_ACTION_START_STOP,
                                       SYSTEM_ACTION_NONE, Period, Timer)


class TestSchedulerActions_2_1(unittest.TestCase):

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

    def test_tc_2_1(self):
        """
        TC 2.1. Overlapping timers w/ resume but w/o former media

        Timer 1           |------------------R
        Timer 2                      |-----------------R

        t       |---------|----T1----|-------T2--------|------->
                t0        t1    t2   t3  t4  t5   t6   t7   t8
        Player            play       play              stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.s_label = "Timer 1"
        timer1.i_end_type = END_TYPE_DURATION
        timer1.td_duration = timedelta(minutes=self._t5 - self._t1)
        timer1.i_media_action = MEDIA_ACTION_START_STOP
        timer1.s_path = "Media T1"
        timer1.s_mediatype = VIDEO
        timer1.b_repeat = False
        timer1.b_resume = True
        timer1.i_fade = FADE_OFF
        timer1.i_vol_min = 0
        timer1.i_vol_max = 100
        timer1.i_system_action = SYSTEM_ACTION_NONE
        timer1.b_active = False
        timer1.b_notify = False
        timer1.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t5))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.s_label = "Timer 2"
        timer2.i_end_type = END_TYPE_DURATION
        timer2.td_duration = timedelta(minutes=self._t7 - self._t3)
        timer2.i_media_action = MEDIA_ACTION_START_STOP
        timer2.s_path = "Media T2"
        timer2.s_mediatype = VIDEO
        timer2.b_repeat = False
        timer2.b_resume = True
        timer2.i_fade = FADE_OFF
        timer2.i_vol_min = 0
        timer2.i_vol_max = 100
        timer2.i_system_action = SYSTEM_ACTION_NONE
        timer2.b_active = False
        timer2.b_notify = False
        timer2.periods = [
            Period(timedelta(minutes=self._t3), timedelta(minutes=self._t7))]

        timers = [timer1, timer2]

        # ------------ t0 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].s_path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[0].i_timer)
        self.assertEqual(player._getResumeStatus(VIDEO)._state, None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].s_path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[0].i_timer)
        self.assertEqual(player._getResumeStatus(VIDEO)._state, None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(
        ).getTimer().i_timer, timers[1].i_timer)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].s_path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[1].i_timer)
        self.assertEqual(player._getResumeStatus(VIDEO)._state, None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 2)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].s_path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[1].i_timer)
        self.assertEqual(player._getResumeStatus(VIDEO)._state, None)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t5))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(timers[1].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].s_path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[1].i_timer)
        self.assertEqual(player._getResumeStatus(VIDEO)._state, None)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t6))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(timers[1].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].s_path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[1].i_timer)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t7))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(
        ).getTimer().i_timer, timers[1].i_timer)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t8))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(VIDEO), None)

        schedulderaction.reset()
