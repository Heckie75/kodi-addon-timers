import os
import time
import xbmc
import xbmcaddon
import xbmcplugin
import sys

import json

from datetime import datetime
from datetime import timedelta

# prevent Error: Failed to import _strptime because the import lockis held by another thread.
# see https://www.raspberrypi.org/forums/viewtopic.php?t=166912
import _strptime


__PLUGIN_ID__ = "script.service.heckies.timers"
settings = xbmcaddon.Addon(id=__PLUGIN_ID__)
addon_dir = xbmc.translatePath(settings.getAddonInfo('path'))

CHECK_INTERVAL = 10

SLEEP_TIMER = 0
SNOOZE_TIMER = 1

TIMERS = [
    "Sleep timer",
    "Snooze timer",
    "Timer 1",
    "Timer 2",
    "Timer 3",
    "Timer 4",
    "Timer 5",
    "Timer 6",
    "Timer 7",
    "Timer 8",
    "Timer 9",
    "Timer 10",
    "Timer 11",
    "Timer 12",
    "Timer 13",
    "Timer 14",
    "Timer 15"
]

TIMER_OFF = 0
TIMER_ONCE = 1

END_TYPE_NO = "0"
END_TYPE_DURATION = "1"
END_TYPE_TIME = "2"

ACTION_NO = "0"
ACTION_PLAY = "1"
ACTION_START = "2"
ACTION_STOP = "3"
ACTION_STOP_AT_END = "4"
ACTION_SUSPEND_AT_END = "5"
ACTION_HIBERNATE_AT_END = "6"
ACTION_POWERDOWN_AT_END = "7"
ACTION_QUIT_AT_END = "8"
ACTION_SCR_SAVE_AT_END = "9"

FADE_OFF = "0"
FADE_IN_FROM_MIN = "1"
FADE_OUT_FROM_MAX = "2"
FADE_OUT_FROM_CURRENT = "3"

TIMER_DAYS_PRESETS = [
    [],                    # off
    [0, 1, 2, 3, 4, 5, 6],  # once
    [0],                   # mon
    [1],                   # tue
    [2],                   # wed
    [3],                   # thu
    [4],                   # fri
    [5],                   # sat
    [6],                   # sun
    [0, 1, 2, 3],          # mon-thu
    [0, 1, 2, 3, 4],       # mon-fri
    [1, 2, 3, 4],          # tue-fri
    [3, 4, 5],             # thu-sat
    [4, 5],                # fri-sat
    [4, 5, 6],             # fri-sun
    [5, 6],                # sat-sun
    [5, 6, 0],             # sat-mon
    [6, 0, 1, 2],          # sun-wed
    [6, 0, 1, 2, 3],       # sun-thu
    [0, 1, 2, 3, 4, 5, 6]  # everyday
]


def set_filename_for_timer(listitem, timer):

    if settings.getSetting("timer_%i" % timer) == TIMER_OFF:
        settings.setSetting("timer_%i" % timer, str(TIMER_ONCE))

    settings.setSetting("timer_%i_label" % timer,
                        listitem.getLabel())

    _uri = listitem.getfilename()
    settings.setSetting("timer_%i_filename" % timer, _uri)

    xbmc.executebuiltin("Notification(\"%s\", \"%s\")"
                        % (TIMERS[timer], listitem.getLabel()))

    _navigate_to_settings(['Down'] * timer
                          + ['Right'] * 2)


def activate_sleep(listitem):

    settings.setSetting("timer_%i" % SLEEP_TIMER, str(TIMER_ONCE))

    settings.setSetting("timer_%i_label" % SLEEP_TIMER,
                        TIMERS[SLEEP_TIMER])

    settings.setSetting("timer_%i_end_type" % SLEEP_TIMER,
                        END_TYPE_DURATION)

    settings.setSetting("timer_%i_action" % SLEEP_TIMER,
                        ACTION_STOP_AT_END)

    dur = settings.getSetting("timer_%i_duration" % SLEEP_TIMER)

    if dur == "00:00":
        settings.setSetting("timer_%i_duration" % SLEEP_TIMER,
                            "00:10")

    settings.setSetting("timer_%i_start" % SLEEP_TIMER,
                        time.strftime("%H:%M", time.localtime()))

    _navigate_to_settings(['Down'] * SLEEP_TIMER
                          + ['Right'] + 4 * ['Down'] + ['Select'])


def activate_snooze(listitem):

    settings.setSetting("timer_%i" % SNOOZE_TIMER, str(TIMER_ONCE))

    settings.setSetting("timer_%i_label" % SNOOZE_TIMER,
                        "%s - %s" % (TIMERS[SNOOZE_TIMER],
                                     listitem.getLabel()))

    if settings.getSetting("timer_%i_action" % SNOOZE_TIMER) \
            not in [ACTION_PLAY, ACTION_START]:
        settings.setSetting("timer_%i_action" % SNOOZE_TIMER,
                            ACTION_START)

    t_now = time.localtime()
    td_start = timedelta(
        hours=t_now.tm_hour,
        minutes=t_now.tm_min) + timedelta(minutes=15)

    settings.setSetting("timer_%i_start" % SNOOZE_TIMER,
                        str(td_start)[0:5])

    filename = listitem.getfilename()
    settings.setSetting("timer_%i_filename" % SNOOZE_TIMER,
                        filename)

    _navigate_to_settings(['Down'] * SNOOZE_TIMER
                          + ['Right'] + 2 * ['Down'] + ['Select'])


def _navigate_to_settings(path=[]):

    xbmc.executebuiltin('Addon.OpenSettings(%s)' % __PLUGIN_ID__)

    if len(path) == 0:
        return

    time.sleep(.3)
    for key in path:
        xbmc.executebuiltin('Action(%s)' % key)


def _json_rpc(jsonmethod, params=None):

    kodi_json = {}
    kodi_json["jsonrpc"] = "2.0"
    kodi_json["method"] = jsonmethod

    if not params:
        params = {}

    kodi_json["params"] = params
    kodi_json["id"] = 1

    json_response = xbmc.executeJSONRPC(json.dumps(kodi_json).encode("utf-8"))
    json_object = json.loads(json_response.decode('utf-8', 'replace'))

    result = None
    if 'result' in json_object:
        if isinstance(json_object['result'], dict):
            for key, value in json_object['result'].iteritems():
                if not key == "limits":
                    result = value
                    break
        else:
            return json_object['result']

    return result


class Scheduler(xbmc.Monitor):

    _timer_state = {
        "t_now": None,
        "td_now": None,
        "i_default_vol": 100,
        "timers": [
            {
                "i_timer": 0,
                "i_schedule": 0,
                "days": [],
                "s_label": "",
                "s_start": "00:00",
                "s_end_type": "0",
                "s_end": "00:00",
                "s_duration": "00:00",
                "td_duration": None,
                "s_action": "0",
                "s_filename": "",
                "s_fade": "0",
                "i_vol_min": 0,
                "i_vol_max": 100,
                "i_return_vol": 100,
                "periods": [],
                "b_in_period": False,
                "b_active": False,
                "b_notify": True,
                "b_silent": False
            }] * len(TIMERS)
    }

    def __init__(self):

        xbmc.Monitor.__init__(self)
        self._timer_state["i_default_vol"] = int(
            settings.getSetting("vol_default"))
        xbmc.executebuiltin("SetVolume(%i)" %
                            self._timer_state["i_default_vol"])
        self._update()

    def onSettingsChanged(self):

        self._update()

        xbmc.executebuiltin(
            "Notification(Heckies timers, update succeeded)")

    def _update(self):

        self._set_now()
        timers = self._timer_state["timers"]
        for i in range(0, len(timers)):

            s_label = settings.getSetting("timer_%i_label" % i)

            s_action = settings.getSetting("timer_%i_action" % i)

            s_fade = settings.getSetting("timer_%i_fade" % i)

            i_vol_min = int(settings.getSetting("timer_%i_vol_min" % i))

            i_vol_max = int(settings.getSetting("timer_%i_vol_max" % i))

            s_filename = settings.getSetting("timer_%i_filename" % i)

            i_schedule = int(settings.getSetting("timer_%i" % i))

            s_start = settings.getSetting("timer_%i_start" % i)

            s_end_type = settings.getSetting("timer_%i_end_type" % i)

            s_end = settings.getSetting("timer_%i_end" % i)

            s_duration = settings.getSetting("timer_%i_duration" % i)

            td_duration = self._parse_time(s_duration)

            b_notify = ("true" == settings.getSetting("timer_%i_notify" % i))

            b_silent = ("true" == settings.getSetting("timer_%i_silent" % i))

            if b_silent and s_filename.startswith("plugin://"):
                s_filename += ("&" if "?" in s_filename else "?") + "silent=1"

            if len(TIMER_DAYS_PRESETS[i_schedule]) > 0:
                xbmc.log("""
                Init timer:
                    timer      : %i
                    label      : %s
                    days       : %s
                    start      : %s
                    end_type   : %s
                    end        : %s
                    duration   : %s
                """ % (i,
                       s_label,
                       ",".join(str(day)
                                for day in TIMER_DAYS_PRESETS[i_schedule]),
                       s_start,
                       s_end_type,
                       s_end,
                       s_duration),
                    xbmc.LOGNOTICE)

            periods = []
            for i_day in TIMER_DAYS_PRESETS[i_schedule]:
                td_start = self._parse_time(s_start, i_day)
                td_end = self._build_end_time(td_start,
                                              s_end_type,
                                              td_duration,
                                              s_end)

                xbmc.log("""
                        day         : %i
                        start       : %s
                        end         : %s
                        duration    : %s
                    """ % (i_day, str(td_start), str(td_end), s_duration),
                         xbmc.LOGNOTICE)

                periods += [{
                    "td_start": td_start,
                    "td_end": td_end
                }]

            timers[i] = {
                "i_timer": i,
                "i_schedule": i_schedule,
                "days": TIMER_DAYS_PRESETS[i_schedule],
                "s_label": s_label,
                "s_start": s_start,
                "s_end_type": s_end_type,
                "s_end": s_end,
                "s_duration": s_duration,
                "td_duration": td_duration,
                "s_action": s_action,
                "s_filename": s_filename,
                "s_fade": s_fade,
                "i_vol_min": i_vol_min,
                "i_vol_max": i_vol_max,
                "periods": periods,
                "b_in_period": False,
                "b_active": False,
                "b_notify": b_notify,
                "b_silent": b_silent
            }

    def _set_now(self, t_now=None):

        if t_now == None:
            t_now = time.localtime()

        td_now = timedelta(hours=t_now.tm_hour,
                           minutes=t_now.tm_min,
                           seconds=t_now.tm_sec,
                           days=t_now.tm_wday)

        self._timer_state["t_now"] = t_now
        self._timer_state["td_now"] = td_now

        return t_now, td_now

    def _abs_time_diff(self, td1, td2):

        s1 = td1.days * 86400 + td1.seconds
        s2 = td2.days * 86400 + td2.seconds

        return abs(s2 - s1)

    def _parse_time(self, s_time, i_day=0):

        if s_time == "":
            s_time = "00:00"

        t_time = time.strptime(s_time, "%H:%M")
        return timedelta(
            days=i_day,
            hours=t_time.tm_hour,
            minutes=t_time.tm_min)

    def _build_end_time(self, td_start, s_end_type, td_duration, s_end):

        if s_end_type == END_TYPE_DURATION:
            td_end = td_start + td_duration

        elif s_end_type == END_TYPE_TIME:
            td_end = self._parse_time(s_end, td_start.days)

            if td_end < td_start:
                td_end += timedelta(days=1)

        else:  # END_TYPE_NO
            td_end = td_start + timedelta(seconds=CHECK_INTERVAL)

        return td_end

    def _start_action(self, timer):

        xbmc.log("timer start action for timer %i" %
                 timer["i_timer"], xbmc.LOGNOTICE)

        try:
            timer["i_return_vol"] = int(
                _json_rpc("Application.GetProperties", {"properties": ["volume"]}))
        except:
            timer["i_return_vol"] = int(settings.getSetting("vol_default"))

        if timer["s_fade"] == FADE_OUT_FROM_CURRENT \
                and timer["s_end_type"] != END_TYPE_NO:
            xbmc.log("timer start fading out from current volume %i for timer %i" % (
                timer["i_return_vol"], timer["i_timer"]), xbmc.LOGNOTICE)

        elif timer["s_fade"] == FADE_OUT_FROM_MAX \
                and timer["s_end_type"] != END_TYPE_NO:
            xbmc.log("timer start fading out from max %i for timer %i" %
                     (timer["i_vol_max"], timer["i_timer"]), xbmc.LOGNOTICE)
            xbmc.executebuiltin("SetVolume("
                                + str(timer["i_vol_max"]) + ")")

        elif timer["s_fade"] == FADE_IN_FROM_MIN \
                and timer["s_end_type"] != END_TYPE_NO:
            xbmc.log("timer start fading in from min %i for timer %i" %
                     (timer["i_vol_min"], timer["i_timer"]), xbmc.LOGNOTICE)
            xbmc.executebuiltin("SetVolume("
                                + str(timer["i_vol_min"]) + ")")

        if timer["s_action"] in [ACTION_PLAY, ACTION_START]:
            xbmc.log("timer start play media for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("PlayMedia(" + timer["s_filename"] + ")")

        elif timer["s_action"] in [ACTION_STOP]:
            xbmc.log("timer stop media for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("PlayerControl(Stop)")

        if timer["b_notify"] \
                and timer["s_end_type"] == END_TYPE_NO:
            icon_file = os.path.join(addon_dir,
                                     "resources",
                                     "assets", "icon_alarm.png")
            xbmc.executebuiltin(
                "Notification("
                + " Timer triggered,"
                + timer["s_label"]
                + ", 5000, "
                + icon_file + ")")

        elif timer["b_notify"]:
            icon_file = os.path.join(addon_dir,
                                     "resources",
                                     "assets", "icon_sleep.png")
            xbmc.executebuiltin(
                "Notification("
                + " Timer starts,"
                + timer["s_label"]
                + ", 5000, "
                + icon_file + ")")

        timer["b_active"] = True

    def _stop_action(self, timer):

        xbmc.log("timer stop for timer %i" % timer["i_timer"], xbmc.LOGNOTICE)

        if timer["s_action"] in [ACTION_PLAY, ACTION_STOP_AT_END]:
            xbmc.log("timer stop player for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("PlayerControl(Stop)")
            time.sleep(2)

        if timer["b_notify"] and timer["s_end_type"] != END_TYPE_NO:
            xbmc.executebuiltin(
                "Notification("
                + "Timer ended,"
                + timer["s_label"]
                + ", 5000)")

        if timer["i_schedule"] == TIMER_ONCE:
            timer["i_schedule"] == TIMER_OFF
            settings.setSetting("timer_%i" % timer["i_timer"],
                                str(TIMER_OFF))

        if timer["s_fade"] != FADE_OFF \
                and timer["s_end_type"] != END_TYPE_NO:
            reset_vol = timer["i_return_vol"]
            xbmc.log("reset volume to %i" % reset_vol, xbmc.LOGNOTICE)
            xbmc.executebuiltin("SetVolume(%s)" % reset_vol)

        timer["b_active"] = False

        if timer["s_action"] in [ACTION_SUSPEND_AT_END]:
            time.sleep(5)
            xbmc.log("timer suspend system for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("Suspend")

        if timer["s_action"] in [ACTION_HIBERNATE_AT_END]:
            time.sleep(5)
            xbmc.log("timer hibernate system for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("Hibernate")

        if timer["s_action"] in [ACTION_POWERDOWN_AT_END]:
            time.sleep(5)
            xbmc.log("timer poweroff system for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("Powerdown")

        if timer["s_action"] in [ACTION_QUIT_AT_END]:
            time.sleep(5)
            xbmc.log("timer quit kodi for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("Quit")

        if timer["s_action"] in [ACTION_SCR_SAVE_AT_END]:
            time.sleep(5)
            xbmc.log("timer starts screensaver for timer %i" %
                     timer["i_timer"], xbmc.LOGNOTICE)
            xbmc.executebuiltin("PlayerControl(Stop)")
            xbmc.executebuiltin("ActivateScreensaver")

    def _fade(self, timer, td_now, td_start, td_end):

        if timer["s_fade"] == FADE_OFF \
                or timer["s_end_type"] == END_TYPE_NO:
            return

        delta_now_start = self._abs_time_diff(td_now, td_start)
        delta_end_start = self._abs_time_diff(td_end, td_start)
        delta_percent = delta_now_start / float(delta_end_start)

        vol_min = timer["i_vol_min"]
        vol_max = timer["i_return_vol"] if timer["s_fade"] == FADE_OUT_FROM_CURRENT else timer["i_vol_max"]
        vol_diff = vol_max - vol_min

        if timer["s_fade"] == FADE_IN_FROM_MIN:
            new_vol = int(vol_min + vol_diff * delta_percent)
        else:
            new_vol = int(vol_max - vol_diff * delta_percent)

        current_vol = int(
            _json_rpc("Application.GetProperties", {"properties": ["volume"]}))
        if current_vol != new_vol:
            xbmc.log("timer fade to new volume %i for timer %i" %
                     (new_vol, timer["i_timer"]), xbmc.LOGNOTICE)
            xbmc.executebuiltin("SetVolume(%i)" % new_vol)

    def _check_period(self, timer, td_now):

        for period in timer["periods"]:

            in_period = period["td_start"] <= td_now < period["td_end"]
            if in_period:
                xbmc.log("timer " + str(timer["i_timer"]) + " is in period: " + str(
                    period["td_start"]) + " <= " + str(td_now) + " < " + str(period["td_end"]), xbmc.LOGDEBUG)
                timer["b_in_period"] = True
                return in_period, period["td_start"], period["td_end"]

        timer["b_in_period"] = False
        return False, None, None

    def check_timers(self, t_now=None):

        t_now, td_now = self._set_now(t_now)

        starters, stoppers = [], []

        timers = self._timer_state["timers"]
        for timer in timers:
            in_period, td_start, td_end = self._check_period(timer, td_now)

            if in_period and not timer["b_active"]:
                starters.append(timer)

            elif not in_period and timer["b_active"]:
                stoppers.append(timer)

            elif in_period:  # fade
                self._fade(timer, td_now, td_start, td_end)

        map(self._stop_action, stoppers)
        map(self._start_action, starters)


if __name__ == "__main__":

    xbmc.log('[Heckies Timers] Service started', xbmc.LOGNOTICE)

    scheduler = Scheduler()

    if xbmc.getCondVisibility("system.platform.windows") and "true" == settings.getSetting("windows_unlock"):
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

    while not scheduler.abortRequested():

        t_now = time.localtime()
        xbmc.log("timer is waiting in intervals of %i secs ..." %
                 (CHECK_INTERVAL - t_now.tm_sec % CHECK_INTERVAL), xbmc.LOGDEBUG)

        if scheduler.waitForAbort(
                CHECK_INTERVAL - t_now.tm_sec % CHECK_INTERVAL):
            break

        scheduler.check_timers()

    if xbmc.getCondVisibility("system.platform.windows") and "true" == settings.getSetting("windows_unlock"):
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
