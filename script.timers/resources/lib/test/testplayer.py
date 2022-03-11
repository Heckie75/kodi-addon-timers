from resources.lib.player import player_utils
from resources.lib.player.player import Player
from resources.lib.player.playerstatus import PlayerStatus
from resources.lib.timer.timer import Timer
from resources.lib.utils import datetime_utils


class TestPlayer(Player):

    _volume = 100
    _player_status = None

    def playTimer(self, timer: Timer) -> None:

        def _save_resume(_timer: Timer) -> None:

            if _timer.b_resume and _timer.is_play_at_start_timer() and _timer.is_stop_at_end_timer():
                if not self._resume_status:
                    self._resume_status = PlayerStatus(
                        _timer.i_timer, self._player_status)

                else:
                    self._getResumeStatus().setTimerId(_timer.i_timer)

            else:
                self._resume_status = None

        def _get_delay_for_seektime(_timer: Timer) -> None:

            if self._seek_delayed_timer and _timer.is_play_at_start_timer():
                t_now, td_now = datetime_utils.get_now()
                td_start = datetime_utils.parse_time(
                    _timer.s_start, t_now.tm_wday)
                seektime = datetime_utils.abs_time_diff(
                    td_now, td_start)
            else:
                seektime = None

            return seektime

        _save_resume(timer)

        playlist = timer.s_filename
        seektime = _get_delay_for_seektime(timer)
        self._playTest(playlist=playlist,
                       seektime=seektime,
                       repeat=player_utils.REPEAT_ALL if timer.b_repeat else player_utils.REPEAT_OFF)

    def _playTest(self, playlist, startpos=0, seektime=None, repeat=player_utils.REPEAT_OFF, shuffled=False, speed=1.0) -> None:

        self._player_status = player_utils.State()
        self._player_status.playlist = playlist
        self._player_status.position = startpos
        self._player_status.repeat = repeat
        self._player_status.speed = speed
        self._player_status.shuffled = shuffled
        self._player_status.time = seektime
        self._player_status.type = 0

    def resumeFormerOrStop(self) -> None:

        resumState = self._getResumeStatus()
        if resumState and resumState.getState():
            state = resumState.getState()
            self._resume_status = None

            self._playTest(
                state.playlist,
                startpos=state.position,
                seektime=state.time,
                repeat=state.repeat,
                shuffled=state.shuffled,
                speed=state.speed)

        else:
            self._player_status = None
            self._resume_status = None

    def set_volume(self, volume: int) -> None:

        self._volume = volume

    def get_volume(self) -> int:

        return self._volume
