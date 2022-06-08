from datetime import datetime

import xbmcaddon
import xbmcgui
from resources.lib.utils import datetime_utils
from resources.lib.utils.settings_utils import (
    activateOnSettingsChangedEvents, deactivateOnSettingsChangedEvents)


def set_pause() -> None:

    addon = xbmcaddon.Addon()
    duration = xbmcgui.Dialog().numeric(
        2, addon.getLocalizedString(32106), "01:00")
    if duration == "":
        return
    else:
        duration = ("0%s" % duration.strip())[-5:]
        end = datetime.today() + datetime_utils.parse_time(duration)
        _set(until=end)


def reset_pause() -> None:

    _set(until=None)


def _set(until: datetime) -> None:

    if not until:
        date = "2000-01-01"
        time = "00:01"
    else:
        date = until.strftime("%Y-%m-%d")
        time = until.strftime("%H:%M")

    addon = xbmcaddon.Addon()
    deactivateOnSettingsChangedEvents()
    addon.setSetting("pause_date", date)
    addon.setSetting("pause_time", time)
    activateOnSettingsChangedEvents()

    xbmcgui.Dialog().notification(addon.getLocalizedString(32027), addon.getLocalizedString(32166)
                                  if not until or until < datetime.today() else addon.getLocalizedString(32165) % until.strftime("%Y-%m-%d %H:%M"))
