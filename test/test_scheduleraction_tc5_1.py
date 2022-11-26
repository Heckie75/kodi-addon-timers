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
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t3 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Audio T1"
        timer1.media_type = AUDIO
        timer1.repeat = False
        timer1.resume = True
        timer1.fade = FADE_IN_FROM_MIN
        timer1.vol_min = 50
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        timers = [timer1]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t0))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.timer.label, timers[0].label)
        self.assertEqual(
            schedulderaction.timerToPlayAV.timer.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t1))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 50)
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.timer.label, timers[0].label)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t2))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures")
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], timers[0].path)
        self.assertEqual(player.getVolume(), 75)
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopAV.timer.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t3))

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
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t4))

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
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t3 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Pictures T1"
        timer1.media_type = PICTURE
        timer1.repeat = False
        timer1.resume = True
        timer1.fade = FADE_OUT_FROM_CURRENT
        timer1.vol_min = 50
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        timers = [timer1]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t0))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.timer.label, timers[0].label)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.timer.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t1))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader.timer.label, timers[0].label)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t2))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio M1")
        self.assertEqual(player.getVolume(), 65)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(
            schedulderaction.timerToStopSlideshow.timer.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t3))

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
        schedulderaction.calculate(
            timers, None, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(timedelta(minutes=self._t4))

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
