import os
import time
import xbmc
import xbmcaddon
import xbmcplugin

from datetime import datetime
from datetime import timedelta

__PLUGIN_ID__ = "script.service.heckies.timers"
settings = xbmcaddon.Addon(id=__PLUGIN_ID__);
addon_dir = xbmc.translatePath( settings.getAddonInfo('path') )

SLEEP_TIMER = 0
SNOOZE_TIMER = 1

TIMERS = [
    "Sleep timer",
    "Snooze timer",
    "Timer 1",
    "Timer 2",
    "Timer 3",
    "Timer 4",
    "Timer 5"
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

FADE_OFF = "0"
FADE_IN = "1"
FADE_OUT = "2"

TIMER_DAYS_PRESETS = [
    [],                    # off
    [0, 1, 2, 3, 4, 5, 6], # once
    [0, 1, 2, 3, 4, 5, 6], # everyday
    [0, 1, 2, 3, 4],       # mon-fri
    [4, 5],                # fri-sat
    [5, 6],                # sat-sun
    [6, 0, 1, 2, 3],       # sun-thu
    [0],                   # mon
    [1],                   # tue
    [2],                   # wed
    [3],                   # thu
    [4],                   # fri
    [5],                   # sat
    [6]                    # sun
]




def set_filename_for_timer(listitem, timer):

    filename = listitem.getfilename()

    if settings.getSetting("timer_%i" % timer) == TIMER_OFF:
        settings.setSetting("timer_%i" % timer, str(TIMER_ONCE))

    settings.setSetting("timer_%i_label" % timer,
                        listitem.getLabel())

    settings.setSetting("timer_%i_filename" % timer, filename)

    xbmc.executebuiltin("Notification(\"%s\", \"%s\")"
                        % (TIMERS[timer], listitem.getLabel()))

    __navigate_to_settings(['Down'] * timer
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

    __navigate_to_settings(['Down'] * SLEEP_TIMER
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
        hours = t_now.tm_hour,
        minutes = t_now.tm_min) + timedelta(minutes = 15)

    settings.setSetting("timer_%i_start" % SNOOZE_TIMER,
                        str(td_start)[0:5])

    filename = listitem.getfilename()
    settings.setSetting("timer_%i_filename" % SNOOZE_TIMER,
                        filename)

    __navigate_to_settings(['Down'] * SNOOZE_TIMER
                         + ['Right'] + 2 * ['Down'] + ['Select'])




def __navigate_to_settings(path = []):

    xbmc.executebuiltin('Addon.OpenSettings(%s)' % __PLUGIN_ID__)

    if len(path) == 0:
        return

    time.sleep(.3)
    for key in path:
        xbmc.executebuiltin('Action(%s)' % key)




class Scheduler(xbmc.Monitor):

    __timer_state = {
        "t_now" : None,
        "td_now" : None,
        "timers" : [
            {
                "i_timer"     : 0,
                "i_schedule"  : 0,
                "days"        : [],
                "s_label"     : "",
                "s_start"     : "00:00",
                "s_end_type"  : "0",
                "s_end"       : "00:00",
                "s_duration"  : "00:00",
                "td_duration" : None,
                "s_action"    : "0",
                "s_filename"  : "",
                "s_fade"      : "0",
                "i_vol_min"   : 0,
                "i_vol_max"   : 100,
                "periods"     : [],
                "b_in_period" : False,
                "b_active"    : False
            }] * len(TIMERS)
    }




    def __init__(self):

        xbmc.Monitor.__init__(self)
        self.__update()




    def onSettingsChanged(self):

        self.__update()

        xbmc.executebuiltin(
            "Notification(Heckies timers, update succeeded)")




    def __update(self):

        self.__set_now()

        timers = self.__timer_state["timers"]
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

            td_duration = self.__parse_time(s_duration)

            periods = []
            for i_day in TIMER_DAYS_PRESETS[i_schedule]:
                td_start = self.__parse_time(s_start, i_day)
                periods += [{
                    "td_start" : td_start,
                    "td_end" : self.__build_end_time(td_start,
                                                     s_end_type,
                                                     td_duration,
                                                     s_end)
                }]

            timers[i] = {
                "i_timer"     : i,
                "i_schedule"  : i_schedule,
                "days"        : TIMER_DAYS_PRESETS[i_schedule],
                "s_label"     : s_label,
                "s_start"     : s_start,
                "s_end_type"  : s_end_type,
                "s_end"       : s_end,
                "s_duration"  : s_duration,
                "td_duration" : td_duration,
                "s_action"    : s_action,
                "s_filename"  : s_filename,
                "s_fade"      : s_fade,
                "i_vol_min"   : i_vol_min,
                "i_vol_max"   : i_vol_max,
                "periods"     : periods,
                "b_in_period" : False,
                "b_active"    : False
            }




    def __set_now(self, t_now = None):

        if t_now == None:
            t_now  = time.localtime()

        td_now = timedelta(hours = t_now.tm_hour,
                             minutes = t_now.tm_min,
                             seconds = t_now.tm_sec,
                             days=t_now.tm_wday)

        self.__timer_state["t_now"] = t_now
        self.__timer_state["td_now"] = td_now

        return t_now, td_now




    def __abs_time_diff(self, td1, td2):

        s1 = td1.days * 86400 + td1.seconds
        s2 = td2.days * 86400 + td2.seconds

        return abs(s2 - s1)




    def __parse_time(self,s_time, i_day = 0):
        try:
            t_time = time.strptime(s_time, "%H:%M")
            return timedelta(
                days = i_day,
                hours = t_time.tm_hour,
                minutes = t_time.tm_min)
        except:
            return timedelta(days = i_day, seconds = 0)




    def __build_end_time(self, td_start, s_end_type, td_duration, s_end):

        if s_end_type == END_TYPE_DURATION:
            td_end = td_start + td_duration

        elif s_end_type == END_TYPE_TIME:
            td_end = self.__parse_time(s_end, td_start.days)

            if td_end < td_start:
                td_end += timedelta(1)

        else: # END_TYPE_NO
            td_end = td_start + timedelta(seconds = 59)

        return td_end




    def __start_action(self, timer):

        if timer["s_fade"] == FADE_OUT \
                and timer["s_end_type"] != END_TYPE_NO:
            xbmc.executebuiltin("SetVolume("
                                + str(timer["i_vol_max"]) + ")")

        elif timer["s_fade"] == FADE_IN \
                and timer["s_end_type"] != END_TYPE_NO:
            xbmc.executebuiltin("SetVolume("
                                + str(timer["i_vol_min"]) + ")")


        if timer["s_action"] in [ACTION_PLAY, ACTION_START]:
            xbmc.executebuiltin("PlayMedia("
                                + timer["s_filename"] + ")")

        elif timer["s_action"] in [ACTION_STOP]:
            xbmc.executebuiltin("PlayerControl(Stop)")


        if timer["s_end_type"] == END_TYPE_NO:
            icon_file = os.path.join(addon_dir,
                                 "resources",
                                 "assets", "icon_alarm.png")
            xbmc.executebuiltin(
                "Notification("
                    + " Timer triggered,"
                    + timer["s_label"]
                    + ", 5000, "
                    + icon_file + ")")
        else:
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




    def __stop_action(self, timer):

        if timer["s_action"] in [ACTION_PLAY, ACTION_STOP_AT_END]:
            xbmc.executebuiltin("PlayerControl(Stop)")
            time.sleep(2)

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
            xbmc.executebuiltin("SetVolume(100)")

        timer["b_active"] = False




    def __fade(self, timer, td_now, td_start, td_end):

        if timer["s_fade"] == FADE_OFF \
                or timer["s_end_type"] ==END_TYPE_NO:
            return

        delta_now_start = self.__abs_time_diff(td_now, td_start)
        delta_end_start = self.__abs_time_diff(td_end, td_start)
        delta_percent = delta_now_start / float(delta_end_start)

        vol_min = timer["i_vol_min"]
        vol_max = timer["i_vol_max"]
        vol_diff = vol_max - vol_min

        if timer["s_fade"] == FADE_IN:
            new_vol = int(vol_min + vol_diff * delta_percent)
        else:
            new_vol = int(vol_max - vol_diff * delta_percent)

        xbmc.executebuiltin("SetVolume(%i)" % new_vol)


    def __check_period(self, timer, td_now):

        for period in timer["periods"]:

            in_period = period["td_start"] <= td_now <= period["td_end"]
            if in_period:
                timer["b_in_period"] = True
                return in_period, period["td_start"], period["td_end"]

        timer["b_in_period"] = False
        return False, None, None




    def __check_timer(self, timer, td_now):

        in_period, td_start, td_end = self.__check_period(timer, td_now)

        if in_period and not timer["b_active"]:
            self.__start_action(timer)

        elif not in_period and timer["b_active"]:
            self.__stop_action(timer)

        elif in_period: # fade
            self.__fade(timer, td_now, td_start, td_end)

        return in_period




    def check_timers(self, t_now = None):

        t_now, td_now = self.__set_now(t_now)

        timers = self.__timer_state["timers"]
        for timer in timers:
            in_period = self.__check_timer(timer, td_now)




if __name__ == "__main__":

    xbmc.log('[Heckies Timers] Service started', xbmc.LOGNOTICE)

    scheduler = Scheduler()
    while not scheduler.abortRequested():

        t_now = time.localtime()
        if scheduler.waitForAbort(
                10 - t_now.tm_sec % 10):
            break

        scheduler.check_timers()
