import os

LOGDEBUG = 0
LOGINFO = 1
LOGNOTICE = 2
LOGWARNING = 3
LOGERROR = 4
ISO_639_1 = 'en'


class PlayList:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.items = []

    def clear(self):
        self.items = []

    def add(self, *args, **kwargs):
        self.items.append((args, kwargs))


class Player:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def play(self, *args, **kwargs):
        return None

    def stop(self):
        return None

    def pause(self):
        return None

    def seekTime(self, *args, **kwargs):
        return None

    def setSubtitles(self, *args, **kwargs):
        return None

    def setAudioStream(self, *args, **kwargs):
        return None


class Monitor:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def waitForAbort(self, timeout=None):
        return False

    def onSettingsChanged(self):
        return None


def sleep(ms):
    return None


def executebuiltin(function, wait=False):
    return None


def executeJSONRPC(jsonrpc):
    return '{}'


def getInfoLabel(label):
    return ''


def getCondVisibility(condition):
    return False


def getRegion(key):
    if key == 'dateshort':
        return '%d/%m/%Y'
    if key == 'datelong':
        return '%d %B %Y'
    return ''


def getLanguage(format=None):
    return 'en'


def translatePath(path):
    return path


def playSFX(filename):
    return None


def shutdown():
    return None


def log(msg, level=LOGNOTICE):
    return None
