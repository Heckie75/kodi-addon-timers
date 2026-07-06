INPUT_DATE = 0


class Dialog:
    def notification(self, *args, **kwargs):
        return None

    def yesno(self, *args, **kwargs):
        return False

    def yesnocustom(self, *args, **kwargs):
        return False

    def numeric(self, *args, **kwargs):
        return None

    def multiselect(self, *args, **kwargs):
        return []

    def select(self, *args, **kwargs):
        return -1

    def input(self, *args, **kwargs):
        return ''


class ListItem:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
