class Config:
    def __init__(self):
        # wklejto.pl/{ID} - Front-end finished paste
        # wklejto.pl/txt{ID} - Raw text. Password front-end still occurs
        self.URL = f"wklejto.pl/"

        self.RANGE = range(1, 10_000)

        self.THREAD_AMOUNT = 30

        self.DB_HOST = "localhost"
        self.DB_PORT = 27017
        self.DB_NAME = "wklejto"
        self.DB_COL = "pastes"

        # Toggles prints and logs
        self.FRONT_END_ENABLED = True

        self.MAX_TRIES = 5
        self.TRY_DELAY = 0.6

    def set_range(self, r) -> bool:
        if r[0] <= 0 or r[1] <= 0:
            return False

        if r[0] > r[1]:
            return False

        self.RANGE = range(r[0], r[1])
