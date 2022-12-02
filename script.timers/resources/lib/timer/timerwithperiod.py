from resources.lib.timer.period import Period
from resources.lib.timer.timer import Timer


class TimerWithPeriod:

    def __init__(self, timer: Timer, period: Period) -> None:
        self.timer: Timer = timer
        self.period: Period = period

    def __str__(self) -> str:
        return "TimerWithPeriod[timer=%s, period=%s]" % (self.timer, self.period)
