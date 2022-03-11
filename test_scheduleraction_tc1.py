import unittest
from datetime import timedelta

from resources.lib.player import player_utils
from resources.lib.test.testplayer import TestPlayer
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION, FADE_IN_FROM_MIN, FADE_OFF, FADE_OUT_FROM_CURRENT,
                                       MEDIA_ACTION_START_STOP,
                                       SYSTEM_ACTION_NONE, Period, Timer)


class TestSchedulerActions(unittest.TestCase):

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

    def test_tc_1_1(self):
        """
        TC 1.1. Single timer w/ resume but w/o former media

        Timer 1           |-----------------R

        t       |---------|-------T1--------|---------------->
                t0        t1       t2       t3       t4
        Player            play              stop
        
        Fader   100       T1(100)-----------T1(50)
        """

        # ------------ setup player ------------d
        player = TestPlayer()
        schedulderaction = SchedulerAction(player)
        player.set_volume(100)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.s_label = "Timer 1"
        timer1.i_end_type = END_TYPE_DURATION
        timer1.td_duration = timedelta(minutes=self._t3 - self._t1)
        timer1.i_media_action = MEDIA_ACTION_START_STOP
        timer1.s_filename = "Media T1"
        timer1.b_repeat = False
        timer1.b_resume = True
        timer1.i_fade = FADE_OUT_FROM_CURRENT
        timer1.i_vol_min = 50
        timer1.i_vol_max = 100
        timer1.i_system_action = SYSTEM_ACTION_NONE
        timer1.b_active = False
        timer1.b_notify = False
        timer1.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        timers = [timer1]

        # ------------ t0 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        self.assertEqual(player._player_status, None)
        self.assertEqual(player._resume_status, None)
        self.assertEqual(player.get_volume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlay(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 100)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, timers[0].s_filename)
        self.assertEqual(player.get_volume(), 100)
        self.assertNotEqual(player._resume_status, None)
        self.assertEqual(player._resume_status._i_timer, timers[0].i_timer)
        self.assertEqual(player._resume_status._state, None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 75)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, timers[0].s_filename)
        self.assertNotEqual(player._resume_status, None)
        self.assertEqual(player._resume_status._i_timer, timers[0].i_timer)
        self.assertEqual(player._resume_status._state, None)
        self.assertEqual(player.get_volume(), 75)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 100)

        schedulderaction.perform()

        self.assertEqual(player._player_status, None)
        self.assertEqual(player.get_volume(), 100)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(
            len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(
            schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        self.assertEqual(player._player_status, None)
        self.assertEqual(player._resume_status, None)
        self.assertEqual(player.get_volume(), 100)

        schedulderaction.reset()

    def test_tc_1_2(self):
        """
        TC 1.2. Single timer w/ resume and w/ former media

        Media 1 |---+---+-|                 |----+---+---+---->     (tested w/ PVR and Playlist)
        Timer 1           |-----+----+------R

        t       |----M1---|-------T1--------|--------M1------->     (tested w/ PVR and Playlist)
                t0        t1       t2       t3       t4
        Player            play              resume

        Fader   100       T1(50)-----------T1(100)
        """

        # ------------ setup player ------------
        player = TestPlayer()
        player._player_status = player_utils.State()
        player._player_status.playlist = "Media M1"
        player.set_default_volume(100)

        schedulderaction = SchedulerAction(player)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.s_label = "Timer 1"
        timer1.i_end_type = END_TYPE_DURATION
        timer1.td_duration = timedelta(minutes=self._t3 - self._t1)
        timer1.i_media_action = MEDIA_ACTION_START_STOP
        timer1.s_filename = "Media T1"
        timer1.b_repeat = False
        timer1.b_resume = True
        timer1.i_fade = FADE_IN_FROM_MIN
        timer1.i_vol_min = 50
        timer1.i_vol_max = 100
        timer1.i_system_action = SYSTEM_ACTION_NONE
        timer1.b_active = False
        timer1.b_notify = False
        timer1.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        timers = [timer1]

        # ------------ t0 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, "Media M1")
        self.assertEqual(player.get_volume(), 100)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer().s_label timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlay(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 50)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, timers[0].s_filename)
        self.assertEqual(player.get_volume(), 100)
        self.assertNotEqual(player._resume_status, None)
        self.assertEqual(player._resume_status._i_timer, timers[0].i_timer)
        self.assertEqual(player._resume_status._state.playlist, "Media M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 75)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, timers[0].s_filename)
        self.assertEqual(player.get_volume(), 75)
        self.assertNotEqual(player._resume_status, None)
        self.assertEqual(player._resume_status._i_timer, timers[0].i_timer)
        self.assertEqual(player._resume_status._state.playlist, "Media M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 100)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, "Media M1")
        self.assertEqual(player.get_volume(), 100)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(
            len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(
            schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, "Media M1")
        self.assertEqual(player.get_volume(), 100)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

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
        player = TestPlayer()
        player._player_status = player_utils.State()
        player._player_status.playlist = "Media M1"
        player.set_volume(80)

        schedulderaction = SchedulerAction(player)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.s_label = "Timer 1"
        timer1.i_end_type = END_TYPE_DURATION
        timer1.td_duration = timedelta(minutes=self._t3 - self._t1)
        timer1.i_media_action = MEDIA_ACTION_START_STOP
        timer1.s_filename = "Media T1"
        timer1.b_repeat = False
        timer1.b_resume = False
        timer1.i_fade = FADE_OUT_FROM_CURRENT
        timer1.i_vol_min = 40
        timer1.i_vol_max = None
        timer1.i_system_action = SYSTEM_ACTION_NONE
        timer1.b_active = False
        timer1.b_notify = False
        timer1.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        timers = [timer1]

        # ------------ t0 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, "Media M1")
        self.assertEqual(player.get_volume(), 80)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlay(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 80)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, timers[0].s_filename)
        self.assertEqual(player.get_volume(), 80)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(player.get_volume(), 60)

        schedulderaction.perform()

        self.assertEqual(player._player_status.playlist, timers[0].s_filename)
        self.assertEqual(player.get_volume(), 60)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 80)

        schedulderaction.perform()

        self.assertEqual(player._player_status, None)
        self.assertEqual(player.get_volume(), 80)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(
            len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlay(), None)
        self.assertEqual(schedulderaction._getTimerToStop(), None)
        self.assertEqual(
            schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        self.assertEqual(player._player_status, None)
        self.assertEqual(player.get_volume(), 80)
        self.assertEqual(player._resume_status, None)

        schedulderaction.reset()
