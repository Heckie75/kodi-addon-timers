import unittest
from datetime import datetime, timedelta

from resources.lib.player.mediatype import VIDEO
from resources.lib.player.player_utils import REPEAT_ALL, REPEAT_OFF
from resources.lib.test.mockplayer import MockPlayer
from resources.lib.test.mockstorage import MockStorage
from resources.lib.timer.scheduleraction import SchedulerAction
from resources.lib.timer.timer import (END_TYPE_DURATION, FADE_IN_FROM_MIN,
                                       FADE_OUT_FROM_MAX,
                                       MEDIA_ACTION_START_STOP, STATE_ENDING,
                                       STATE_RUNNING, STATE_STARTING,
                                       STATE_WAITING, SYSTEM_ACTION_NONE,
                                       Period, Timer)
from resources.lib.utils.datetime_utils import DateTimeDelta


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

        schedulderaction = SchedulerAction(player, MockStorage())

        # ------------ setup timers ------------
        # Timer 1 (T1)
        timer1 = Timer(1)
        timer1.label = "Timer 1"
        timer1.end_type = END_TYPE_DURATION
        timer1.duration_timedelta = timedelta(minutes=self._t7 - self._t1)
        timer1.media_action = MEDIA_ACTION_START_STOP
        timer1.path = "Media T1.1 (0:45)|Media T1.2 (1:55)|Media T1.3 (0:55)|Media T1.4 (1:13)|Media T1.5 (2:39)"
        timer1.media_type = VIDEO
        timer1.repeat = False
        timer1.shuffle = False
        timer1.resume = True
        timer1.fade = FADE_IN_FROM_MIN
        timer1.vol_min = 30
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
        timer2.repeat = True
        timer2.shuffle = True
        timer2.resume = True
        timer2.fade = FADE_OUT_FROM_MAX
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

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t0)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
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
        self.assertEqual(schedulderaction.fader, timer1)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t1)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path.split("|")[0])
        self.assertEqual(player.getVolume(), 30)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

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
        self.assertEqual(schedulderaction.fader, timer1)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t2)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[0].path.split("|")[0])
        self.assertEqual(player.getVolume(), 42)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

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
        self.assertEqual(schedulderaction.fader, timer1)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[1].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t3)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 53)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[1].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

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
        self.assertEqual(schedulderaction.fader, timer1)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t4)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]
                         ["file"], timers[1].path)
        self.assertEqual(player.getVolume(), 65)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[1].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

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
        self.assertEqual(schedulderaction.fader, timer1)
        self.assertEqual(
            schedulderaction.timerToPlayAV.id, timers[0].id)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t5)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].position, 3)
        self.assertEqual(apwpl[VIDEO].time, 1500)
        self.assertEqual(apwpl[VIDEO].playlist[3]
                         ["file"], timers[0].path.split("|")[3])
        self.assertEqual(player.getVolume(), 80)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

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
        self.assertEqual(schedulderaction.fader, timer1)
        self.assertEqual(schedulderaction.timerToPlayAV, None)
        self.assertEqual(schedulderaction.timerToStopAV, None)
        self.assertEqual(schedulderaction.timerWithSystemAction, None)

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t6)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[3]
                         ["file"], timers[0].path.split("|")[3])
        self.assertEqual(player.getVolume(), 88)
        self.assertNotEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(player._getResumeStatus(
            VIDEO).timer.id, timers[0].id)
        self.assertEqual(player._getResumeStatus(
            VIDEO).state.playlist[0]["file"], "Media M1")
        self.assertEqual(apwpl[VIDEO].shuffled, False)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_OFF)

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

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t7)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

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

        schedulderaction.perform(DateTimeDelta(
            datetime.utcfromtimestamp(60 * self._t8)))

        apwpl = player.getActivePlayersWithPlaylist()
        self.assertEqual(VIDEO in apwpl, True)
        self.assertEqual(apwpl[VIDEO].playlist[0]["file"], "Media M1")
        self.assertEqual(player.getVolume(), 80)
        self.assertEqual(player._getResumeStatus(VIDEO), None)
        self.assertEqual(apwpl[VIDEO].shuffled, True)
        self.assertEqual(apwpl[VIDEO].repeat, REPEAT_ALL)

        schedulderaction.reset()
