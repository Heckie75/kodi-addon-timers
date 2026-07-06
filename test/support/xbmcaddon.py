import os


class Addon:
    def __init__(self, id=None):
        self.id = id

    def getSettingInt(self, key):
        return 0

    def getSettingString(self, key):
        return ''

    def getSettingBool(self, key):
        return False

    def getSetting(self, key):
        return ''

    def setSetting(self, key, value):
        return None

    def getLocalizedString(self, id):
        return str(id)

    def getAddonInfo(self, key):
        if key == 'path':
            return os.getcwd()
        return ''
