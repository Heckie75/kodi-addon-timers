import unittest

from resources.lib.utils.datetime_utils import DateTimeDelta
from datetime import datetime, timedelta

from resources.lib.player.mediatype import AUDIO, PICTURE, VIDEO
from resources.lib.test.mockplayer import MockPlayer
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION, FADE_OFF,
                                       MEDIA_ACTION_START_STOP, STATE_ENDING,
                                       STATE_RUNNING, STATE_STARTING,
                                       STATE_WAITING, SYSTEM_ACTION_NONE,
                                       Period, Timer)


class TestSchedulerActions_5_3(unittest.TestCase):

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

    def test_tc_5_3_1(self):
        """
        Slide T1           |------------------R
        Slide T2                      |-----------------R

        t        |---------|----T1----|-------T2--------|------->
                 t0        t1    t2   t3  t4  t5   t6   t7   t8
        Player             play       play              stop
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        player.setVolume(100)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t5 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Pictures T1"
        timer1.media_type = PICTURE
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
        timer2.path = "Pictures T2"
        timer2.media_type = PICTURE
        timer2.repeat = False
        timer2.resume = True
        timer2.fade = FADE_OFF
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t7))]

        timers = [timer1, timer2]

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

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(
            schedulderaction.timerToStopSlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

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
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

    def test_tc_5_3_2(self):
        """
        Video M1   |---------|                            |---------------->
        Picture T1           |----------R
        Picture T2                      |-----------------R

        t          |----M1---|----T1----|-------T2--------|-------M1-------->
                   t0        t1   t2    t3      t4        t5      t6
        Player               play       play              resume
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        player.setVolume(100)
        playlist = player._buildPlaylist(["Video M1"], VIDEO)
        player.play(playlist)

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
        timer1.fade = FADE_OFF
        timer1.vol_min = 0
        timer1.vol_max = 100
        timer1.system_action = SYSTEM_ACTION_NONE
        timer1.active = False
        timer1.notify = False
        timer1.periods = [
            Period(timedelta(days=3, minutes=self._t1), timedelta(days=3, minutes=self._t3))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t5 - self._t3)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Pictures T2"
        timer2.media_type = PICTURE
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
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Video M1")
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(
            schedulderaction.timerToStopSlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], "Video M1")
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_WAITING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], "Video M1")
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

    def test_tc_5_3_3(self):
        """
         Slide T1           |-------------------------R
         Slide T2                  |------R

         t        |---------|--T1--|--T2--|---T1------|---------------->
                  t0        t1 t2  t3 t4  t5   t6     t7   t8
         Player             play   play   resume      stop
         """

        # ------------ setup player ------------
        player = MockPlayer()
        player.setSeekDelayedTimer(True)
        player._slideShowStaytime = 60
        schedulderaction = SchedulerAction(player)
        player.setVolume(100)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Pictures T1.1|Pictures T1.2|Pictures T1.3|Pictures T1.4|Pictures T1.5|Pictures T1.6|Pictures T1.7"
        timer1.media_type = PICTURE
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
        timer2.path = "Pictures T2"
        timer2.media_type = PICTURE
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
        player._td_now = timedelta(minutes=self._t0)

        self.assertEqual(timers[0].state, STATE_WAITING)
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
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))
        player._td_now = timedelta(minutes=self._t1)

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path.split("|")[0])
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))
        player._td_now = timedelta(minutes=self._t2)

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path.split("|")[0])
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

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
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

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
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

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
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].position, 2)
        self.assertEqual(apwpl[PICTURE].playlist[2]
                         ["file"], timers[0].path.split("|")[2])
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))
        player._td_now = timedelta(minutes=self._t6)

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[2]
                         ["file"], timers[0].path.split("|")[2])
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(PICTURE).state, None)

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
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(
            schedulderaction.timerToStopSlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

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
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 0)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

    def test_tc_5_3_4(self):
        """
         Video M1 |---------|                         |---------------->
         Slide T1           |-------------------------R
         Slide T2                  |------R

         t        |----M1---|--T1--|--T2--|---T1------|------M1-------->
                  t0        t1 t2  t3 t4  t5   t6     t7   t8
         Player             play   play   resume      resume
         """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        player.setVolume(100)
        playlist = player._buildPlaylist(["Video M1"], VIDEO)
        player.play(playlist)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Pictures T1"
        timer1.media_type = PICTURE
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
        timer2.path = "Pictures T2"
        timer2.media_type = PICTURE
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
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Video M1")
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

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
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(
            schedulderaction.timerToStopSlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Video M1")
        self.assertEqual(player.getVolume(), 100)

        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

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
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Video M1")
        self.assertEqual(player.getVolume(), 100)

        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()

    def test_tc_5_3_5(self):
        """
        Video M1 |---------|                            |---------------->
        Slide T1           |------------------R
        Slide T2                      |-----------------R

        t       |----M1---|----T1----|-------T2--------|-------M1-------->
                t0        t1    t2   t3  t4  t5   t6   t7   t8
        Player            play       play              resume
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        player.setVolume(100)
        playlist = player._buildPlaylist(["Video M1"], VIDEO)
        player.play(playlist)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t5 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Pictures T1"
        timer1.media_type = PICTURE
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
        timer2.path = "Pictures T2"
        timer2.media_type = PICTURE
        timer2.repeat = False
        timer2.resume = True
        timer2.fade = FADE_OFF
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(days=3, minutes=self._t3), timedelta(days=3, minutes=self._t7))]

        timers = [timer1, timer2]

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

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Video M1")
        self.assertEqual(player.getVolume(), 100)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        self.assertEqual(timers[0].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[0].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_STARTING)
        self.assertEqual(len(schedulderaction._beginningTimers), 1)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(
            schedulderaction.timerToPlaySlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        self.assertEqual(timers[0].state, STATE_RUNNING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 2)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t5 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        self.assertEqual(timers[0].state, STATE_ENDING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t6 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_RUNNING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 1)
        self.assertEqual(len(schedulderaction._endingTimers), 0)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[1].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Video M1")

        schedulderaction.reset()

        # ------------ t7 ------------
        schedulderaction.calculate(
            timers, DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        self.assertEqual(timers[0].state, STATE_WAITING)
        self.assertEqual(timers[1].state, STATE_ENDING)
        self.assertEqual(len(schedulderaction._beginningTimers), 0)
        self.assertEqual(len(schedulderaction._runningTimers), 0)
        self.assertEqual(len(schedulderaction._endingTimers), 1)
        self.assertEqual(schedulderaction.fader, None)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(
            schedulderaction.timerToStopSlideshow.id, timers[1].id)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], "Video M1")
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

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
        self.assertEqual(schedulderaction.timerToPlaySlideshow, None)
        self.assertEqual(schedulderaction.timerToStopSlideshow, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(len(apwpl), 1)
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], "Video M1")
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()
