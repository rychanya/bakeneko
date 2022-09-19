from bakeneko.store import store


class AppContext:
    def __init__(self) -> None:
        self.store = store
