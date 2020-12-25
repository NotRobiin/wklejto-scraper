class Config:
    def __init__(self):
        self.URL = f"wklejto.pl/"

        self.RANGE = None

        self.THREAD_AMOUNT = None

        self.DB_HOST = "localhost"
        self.DB_PORT = 27017
        self.DB_NAME = "wklejto"
        self.DB_COL = "pastes"

        # Toggles prints and logs
        self.FRONT_END_ENABLED = True

        self.MAX_TRIES = 5
        self.TRY_DELAY = 0.2
