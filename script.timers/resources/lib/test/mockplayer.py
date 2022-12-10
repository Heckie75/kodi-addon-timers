import re

from resources.lib.player import player_utils
from resources.lib.player.mediatype import AUDIO, PICTURE, TYPES, VIDEO
from resources.lib.player.player import Player
from resources.lib.player.playerstatus import PlayerStatus
from resources.lib.utils.vfs_utils import get_file_name


class PlayList():

    def __init__(self) -> None:
        self.playListId: int = -1
        self.paths: 'list[str]' = None
        self.position: int = 0
        self.directUrl: str = None

    def getPlayListId(self) -> int:

        return self.playListId

    def shuffle(self) -> None:

        if self.paths:
            self.paths.reverse()

    def getposition(self) -> int:

        return self.position

    def size(self) -> int:

        return len(self.paths) if self.paths else 0


class MockPlayer(Player):

    def __init__(self) -> None:
        super().__init__()
        self._player_status: 'dict[PlayerStatus]' = dict()
        self._volume: int = 100
        self._slideShowStaytime: int = 5

    def _playSlideShow(self, path: str, beginSlide=None, shuffle=False) -> None:

        files, type = self._getFilesAndType(path=path, type=PICTURE)
        playlist = self._buildPlaylist(files, type=PICTURE)
        startpos = files.index(beginSlide) if beginSlide else 0
        self.play(playlist, startpos=startpos)
        self.setShuffled(shuffle)

    def play(self, playlist: PlayList, startpos=0) -> None:

        playlist.position = startpos

        state = self._player_status[TYPES[playlist.playListId]
                                    ] if TYPES[playlist.playListId] in self._player_status else player_utils.State()
        state.playerId = playlist.playListId
        state.playlistId = playlist.playListId
        state.playlist = playlist.paths
        state.position = startpos
        state.time = 0
        state.type = TYPES[playlist.playListId]

        for r in player_utils.get_types_replaced_by_type(state.type):
            self.stopPlayer(r)

        self._player_status[state.type] = state

        if TYPES[state.playerId] in [AUDIO, VIDEO]:
            self.onAVStarted()

    def stop(self) -> None:

        self.stopPlayer(type=AUDIO)
        self.stopPlayer(type=VIDEO)

    def stopPlayer(self, type: str) -> 'player_utils.State':

        if type in self._player_status:
            return self._player_status.pop(type)

        return None

    def isPlaying(self) -> bool:

        return self.isPlayingAudio() or self.isPlayingVideo()

    def isPlayingAudio(self) -> bool:

        return AUDIO in self._player_status

    def isPlayingVideo(self) -> bool:

        return VIDEO in self._player_status

    def getTotalTime(self) -> float:

        if self.isPlaying():
            f = self._playlist.paths[self._playlist.position]["file"]
            m = re.match(".*\(([0-9]+:[0-9]{2})\)$", f)
            if m:
                s = m.groups()[0].split(":")
                return float(s[0]) * 3600 + float(s[1]) * 60

            else:
                return 0.0
        else:
            return 0.0

    def playnext(self) -> None:

        if self.isPlayingVideo():
            self.play(playlist=self._playlist,
                      startpos=self._playlist.position + 1)

        elif self.isPlayingAudio():
            self.play(playlist=self._playlist,
                      startpos=self._playlist.position + 1)

    def getTime(self) -> float:

        if self.isPlayingVideo():
            return self._player_status[VIDEO].time

        elif self.isPlayingAudio():
            return self._player_status[AUDIO].time

        else:
            return 0

    def seekTime(self, seekTime: float) -> None:

        for type in self._player_status:
            if type in [AUDIO, VIDEO]:
                self._player_status[type].time = seekTime

    def _getFilesAndType(self, path: str, type=None) -> 'tuple[list[str],str]':

        return path.split("|"), type

    def _buildPlaylist(self, paths: 'list[str]', type: str, label="") -> 'PlayList':

        playlist = PlayList()
        playlist.paths = [
            {"file": file, "label": get_file_name(file)} for file in paths]
        playlist.type = type
        playlist.playListId = TYPES.index(type)

        return playlist

    def getActivePlayersWithPlaylist(self, type=None) -> 'dict[str, player_utils.State]':

        newState = dict()

        for _type in self._player_status:

            if not type or _type == type:
                newState[_type] = player_utils.State()
                newState[_type].playerId = self._player_status[_type].playerId
                newState[_type].type = self._player_status[_type].type
                newState[_type].position = self._player_status[_type].position
                newState[_type].time = self._player_status[_type].time
                newState[_type].playlistId = self._player_status[_type].playlistId
                newState[_type].playlist = self._player_status[_type].playlist
                newState[_type].repeat = self._player_status[_type].repeat
                newState[_type].shuffled = self._player_status[_type].shuffled
                newState[_type].speed = self._player_status[_type].speed

        return newState

    def getVolume(self) -> int:

        return self._volume

    def setVolume(self, volume: int) -> None:

        self._volume = volume

    def setRepeat(self, mode: str) -> None:

        for type in self._player_status:
            self._player_status[type].repeat = mode

    def setShuffled(self, value: bool) -> None:

        for type in self._player_status:
            self._player_status[type].shuffled = value

    def setSpeed(self, speed: float) -> None:

        for type in self._player_status:
            self._player_status[type].speed = speed

    def _getSlideshowStaytime(self) -> int:

        return self._slideShowStaytime
