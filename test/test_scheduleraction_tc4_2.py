import unittest
from datetime import timedelta

from resources.lib.player.player_utils import REPEAT_ALL, REPEAT_OFF
from resources.lib.player.mediatype import VIDEO
from resources.lib.test.mockplayer import MockPlayer
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION, FADE_IN_FROM_MIN, FADE_OFF, FADE_OUT_FROM_MAX,
                                       MEDIA_ACTION_START_STOP,
                                       SYSTEM_ACTION_NONE, Period, Timer)


class TestSchedulerActions_4_2(unittest.TestCase):

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

    def test_tc_4_2(self):
        """
        Media 1 |---------|                         |---------------->
        Timer 1           |-------------------------R
        Timer 2                  |------R

        t       |----M1---|--T1--|--T2--|---T1------|------M1-------->
                t0        t1 t2  t3 t4  t5   t6     t7   t8
        Player            play   play   resume      resume
        """

        # ------------ setup player ------------
        player = MockPlayer()
        player.setSeekDelayedTimer(True)
        playlist = player._buildPlaylist(["Media M1"], VIDEO)
        player.play(playlist)
        player.setDefaultVolume(100)
        player.setShuffled(True)
        player.setRepeat(REPEAT_ALL)
        player.setVolume(80)

        schedulderaction = SchedulerAction(player)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.s_label = "Timer 1"
        timer1.i_end_type = END_TYPE_DURATION
        timer1.td_duration = timedelta(minutes=self._t7 - self._t1)
        timer1.i_media_action = MEDIA_ACTION_START_STOP
        timer1.s_path = "Media T1.1 (0:45)|Media T1.2 (1:55)|Media T1.3 (0:55)|Media T1.4 (1:13)|Media T1.5 (2:39)"
        timer1.s_mediatype = VIDEO
        timer1.b_repeat = False
        timer1.b_shuffle = False
        timer1.b_resume = True
        timer1.i_fade = FADE_IN_FROM_MIN
        timer1.i_vol_min = 30
        timer1.i_vol_max = 100
        timer1.i_system_action = SYSTEM_ACTION_NONE
        timer1.b_active = False
        timer1.b_notify = False
        timer1.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t7))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.s_label = "Timer 2"
        timer2.i_end_type = END_TYPE_DURATION
        timer2.td_duration = timedelta(minutes=self._t5 - self._t3)
        timer2.i_media_action = MEDIA_ACTION_START_STOP
        timer2.s_path = "Media T2"
        timer2.s_mediatype = VIDEO
        timer2.b_repeat = True
        timer2.b_shuffle = True
        timer2.b_resume = True
        timer2.i_fade = FADE_OUT_FROM_MAX
        timer2.i_vol_min = 0
        timer2.i_vol_max = 100
        timer2.i_system_action = SYSTEM_ACTION_NONE
        timer2.b_active = False
        timer2.b_notify = False
        timer2.periods = [
            Period(timedelta(minutes=self._t3), timedelta(minutes=self._t5))]

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
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t1))
        player._td_now = timedelta(minutes=self._t1)

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer(), timer1)
        self.assertEqual(schedulderaction._getTimerToPlayAV(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 30)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].s_path.split("|")[0])
        self.assertEqual(player.getVolume(), 30)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[0].i_timer)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t2))
        player._td_now = timedelta(minutes=self._t2)
        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer(), timer1)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 41)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].s_path.split("|")[0])
        self.assertEqual(player.getVolume(), 41)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[0].i_timer)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))
        player._td_now = timedelta(minutes=self._t3)

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer(), timer1)
        self.assertEqual(schedulderaction._getTimerToPlayAV(
        ).getTimer().i_timer, timers[1].i_timer)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 53)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].s_path)
        self.assertEqual(player.getVolume(), 53)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[1].i_timer)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t4))
        player._td_now = timedelta(minutes=self._t4)

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 2)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer(), timer1)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 65)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].s_path)
        self.assertEqual(player.getVolume(), 65)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[1].i_timer)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t5))
        player._td_now = timedelta(minutes=self._t5)

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader().getTimer(), timer1)
        self.assertEqual(schedulderaction._getTimerToPlayAV(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 76)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].position, 3)
        self.assertEqual(apwpl[VIDEO].time, 1500)                         
        self.assertEqual(apwpl[VIDEO].playlist[3]
                         ["file"], timers[0].s_path.split("|")[3])
        self.assertEqual(player.getVolume(), 76)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[0].i_timer)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t6))
        player._td_now = timedelta(minutes=self._t6)

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader().getTimer(), timer1)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 88)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[3]
                         ["file"], timers[0].s_path.split("|")[3])
        self.assertEqual(player.getVolume(), 88)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._timer.i_timer, timers[0].i_timer)
        self.assertEqual(player._getResumeStatus(
            VIDEO)._state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t7))
        player._td_now = timedelta(minutes=self._t7)

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(timers[1].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 80)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()

        # ------------ t8 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t8))
        player._td_now = timedelta(minutes=self._t8)

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
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()
