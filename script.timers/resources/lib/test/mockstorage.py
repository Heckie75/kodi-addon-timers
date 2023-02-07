from resources.lib.timer.storage import Storage


class MockStorage(Storage):

    def __init__(self, data: 'list[dict]' = list()) -> None:
        super().__init__()

        self._data = data

    def release_lock(self) -> None:

        self.lock = None

    def _load_from_storage(self) -> 'list[dict]':

        return self._data

    def _save_to_storage(self, storage: 'list[dict]') -> None:

        storage.sort(key=lambda item: item["id"])
        self._data = storage
