import datetime

# prevent Error: Failed to import _strptime because the import lockis held by another thread.
# see https://www.raspberrypi.org/forums/viewtopic.php?t=166912
import _strptime
import xbmc
import xbmcaddon

from resources.lib.timer.scheduler import Scheduler
from resources.lib.timer import migration
from resources.lib.timer import util

addon = xbmcaddon.Addon()


if __name__ == "__main__":

    # prevent Error: Failed to import _strptime because the import locks held by another thread.
    # see https://www.raspberrypi.org/forums/viewtopic.php?t=166912
    try:
        datetime.datetime.strptime("2016", "%Y")
    except:
        pass

    migration.migrate()

    scheduler = Scheduler(addon)

    try:
        scheduler.start()

    finally:
        scheduler.reset_powermanagement_displaysoff()
        util.set_windows_unlock(False)
