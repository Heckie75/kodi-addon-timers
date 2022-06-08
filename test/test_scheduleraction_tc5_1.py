import unittest
from datetime import timedelta

from resources.lib.player.mediatype import AUDIO, PICTURE, VIDEO
from resources.lib.test.mockplayer import MockPlayer
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION, FADE_IN_FROM_MIN,
                                       FADE_OFF, FADE_OUT_FROM_CURRENT,
                                       FADE_OUT_FROM_MAX,
                                       MEDIA_ACTION_START_STOP,
                                       SYSTEM_ACTION_NONE, Period, Timer)


class TestSchedulerActions_5_1_1(unittest.TestCase):

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

    def test_tc_5_1_1(self):
        """
        TC 1.5.1 Single timer w/ resume and w/ former media

        Media 1 |---+---+---+---+---+---+---+---+---+---+---->      (Picture)
        Timer 1           |-----+----+------R                       (Audio)

        t       |----M1---|-------M1/T1-----|--------M1------>
                t0        t1       t2       t3       t4
        Player            play              resume

        Fader   100       T1(50)-----------T1(100)
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        playlist = player._buildPlaylist(["Pictures"], PICTURE)
        player.play(playlist)
        player.setVolume(100)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.s_label = "Timer 1"
        timer1.i_end_type = END_TYPE_DURATION
        timer1.td_duration = timedelta(minutes=self._t3 - self._t1)
        timer1.i_media_action = MEDIA_ACTION_START_STOP
        timer1.s_path = "Audio T1"
        timer1.s_mediatype = AUDIO
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
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(
        ).getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlayAV(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 50)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], timers[0].s_path)
        self.assertEqual(player.getVolume(), 50)
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(
        ).getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 75)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], timers[0].s_path)
        self.assertEqual(player.getVolume(), 75)
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 100)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].b_active, False)
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
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, False)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

class TestSchedulerActions_5_1_2(unittest.TestCase):

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

    def test_tc_5_1_2(self):
        """
        TC 1.5.2 Single timer w/ resume and w/ former media

        Media 1 |---+---+---+---+---+---+---+---+---+---+---->      (Audio)
        Timer 1           |-----+----+------R                       (Picture)

        t       |----M1---|-------M1/T1-----|--------M1------>
                t0        t1       t2       t3       t4
        Player            play              resume

        Fader   80        T1(80)-----------T1(50)
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        playlist = player._buildPlaylist(["Audio M1"], AUDIO)
        player.play(playlist)
        player.setVolume(80)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.s_label = "Timer 1"
        timer1.i_end_type = END_TYPE_DURATION
        timer1.td_duration = timedelta(minutes=self._t3 - self._t1)
        timer1.i_media_action = MEDIA_ACTION_START_STOP
        timer1.s_path = "Pictures T1"
        timer1.s_mediatype = PICTURE
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
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(
        ).getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 80)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].s_path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).getState(), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].b_active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(
        ).getTimer().s_label, timers[0].s_label)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 65)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].s_path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).getState(), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 65)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(
        ).getTimer().i_timer, timers[0].i_timer)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, 80)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, False)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.initFromTimers(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].b_active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        self.assertEqual(schedulderaction._volume, None)

        schedulderaction.perform()

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, False)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()
