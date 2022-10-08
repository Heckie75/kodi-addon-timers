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


class TestSchedulerActions_5_2(unittest.TestCase):

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

    def test_tc_5_1_3(self):
        """
        TC 1.5.3 Single timer w/ resume and w/ former media

        Media 1 |---+---+-|                 |----+---+---+---->     (Video)
        Timer 1           |-----+----+------R                       (Picture)
        Timer 2           |-----+----+------R                       (Audio)

        t       |----M1---|-------T1--------|--------M1------->
                t0        t1       t2       t3       t4
        Player            play              resume

        Fader   100       T1(0)-----------T1(100)
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        playlist = player._buildPlaylist(["Video M1"], VIDEO)
        player.play(playlist)
        player.setVolume(100)

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
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        # Timer 2 (T2)
        timer2 = Timer(2)
        timer2.label = "Timer 2"
        timer2.end_type = END_TYPE_DURATION
        timer2.duration_timedelta = timedelta(minutes=self._t3 - self._t1)
        timer2.media_action = MEDIA_ACTION_START_STOP
        timer2.path = "Audio T2"
        timer2.media_type = AUDIO
        timer2.repeat = False
        timer2.resume = True
        timer2.fade = FADE_IN_FROM_MIN
        timer2.vol_min = 0
        timer2.vol_max = 100
        timer2.system_action = SYSTEM_ACTION_NONE
        timer2.active = False
        timer2.notify = False
        timer2.periods = [
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        timers = [timer1, timer2]

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t0))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Video M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(timers[1].active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 2)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(
        ).getTimer().id, timers[0].id)
        self.assertEqual(schedulderaction._getFader(
        ).getTimer().label, timers[1].label)
        self.assertEqual(schedulderaction._getTimerToPlayAV(
        ).getTimer().id, timers[1].id)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t1))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).getState().playlist[0]["file"], "Video M1")

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio T2")
        self.assertEqual(player.getVolume(), 0)
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(AUDIO).getState(), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(timers[1].active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 2)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getFader(
        ).getTimer().label, timers[1].label)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t2))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).getState().playlist[0]["file"], "Video M1")

        # Audio
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]
                         ["file"], "Audio T2")
        self.assertEqual(player.getVolume(), 50)
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(AUDIO).getState(), None)

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(timers[1].active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 2)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(
        ).getTimer().id, timers[0].id)
        self.assertEqual(schedulderaction._getTimerToStopAV(
        ).getTimer().id, timers[1].id)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t3))

        apwpl = player.getActivePlayersWithPlaylist()
        # Picture / Audio
        self.assertEqual(PICTURE in apwpl, False)
        self.assertEqual(AUDIO in apwpl, False)

        # Video
        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Video M1")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)
        
        schedulderaction.reset()

    def test_tc_5_1_4(self):
        """
        TC 1.5.3 Single timer w/ resume and w/ former media

        Media 1 |---+---+-|                 |----+---+---+---->     (Picture)
        Media 2 |---+---+-|                 |----+---+---+---->     (Audio)        
        Timer 1           |-----+----+------R                       (Video)

        t       |----M1---|-------T1--------|--------M1------->
                t0        t1       t2       t3       t4
        Player            play              resume
        """

        # ------------ setup player ------------
        player = MockPlayer()
        schedulderaction = SchedulerAction(player)
        playlist = player._buildPlaylist(["Pictures M1"], PICTURE)
        player.play(playlist)

        playlist = player._buildPlaylist(["Audio M2"], AUDIO)
        player.play(playlist)
        player.setVolume(100)

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t3 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Video T1"
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
            Period(timedelta(minutes=self._t1), timedelta(minutes=self._t3))]

        timers = [timer1]     

        # ------------ t0 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t0))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t0))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures M1")
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]["file"], "Audio M2")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()

        # ------------ t1 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t1))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 1)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToPlayAV().getTimer().id, timers[0].id)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t1))

        apwpl = player.getActivePlayersWithPlaylist()
        # Video
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(
            PICTURE).getState().playlist[0]["file"], "Pictures M1")
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(AUDIO).getState().playlist[0]["file"], "Audio M2")
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(VIDEO).getState(), None)

        schedulderaction.reset()

        # ------------ t2 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t2))

        self.assertEqual(timers[0].active, True)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 1)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getRunningTimers()[0].getTimer().id, timers[0].id)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t2))

        apwpl = player.getActivePlayersWithPlaylist()
        # Video
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path)
        self.assertNotEqual(player._getResumeStatus(PICTURE), None)
        self.assertEqual(player._getResumeStatus(
            PICTURE).getState().playlist[0]["file"], "Pictures M1")
        self.assertNotEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(AUDIO).getState().playlist[0]["file"], "Audio M2")
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(VIDEO).getState(), None)        

        schedulderaction.reset()

        # ------------ t3 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t3))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 1)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV().getTimer().id, timers[0].id)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t3))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures M1")
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]["file"], "Audio M2")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(AUDIO), None)

        schedulderaction.reset()                            

        # ------------ t4 ------------
        schedulderaction.calculate(
            timers, timedelta(minutes=self._t4))

        self.assertEqual(timers[0].active, False)
        self.assertEqual(len(schedulderaction._getBeginningTimers()), 0)
        self.assertEqual(len(schedulderaction._getRunningTimers()), 0)
        self.assertEqual(len(schedulderaction._getEndingTimers()), 0)
        self.assertEqual(schedulderaction._getTimerToPlaySlideshow(), None)
        self.assertEqual(schedulderaction._getFader(), None)
        self.assertEqual(schedulderaction._getTimerToStopAV(), None)
        self.assertEqual(schedulderaction._getTimerToStopSlideshow(), None)
        self.assertEqual(schedulderaction._getTimerWithSystemAction(), None)
        

        schedulderaction.perform(timedelta(minutes=self._t4))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(PICTURE in apwpl, True)
        self.assertEqual(apwpl[PICTURE].playlist[0]["file"], "Pictures M1")
        self.assertEqual(AUDIO in apwpl, True)
        self.assertEqual(apwpl[AUDIO].playlist[0]["file"], "Audio M2")
        self.assertEqual(player.getVolume(), 100)
        self.assertEqual(player._getResumeStatus(AUDIO), None)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(PICTURE), None)

        schedulderaction.reset()                                    
