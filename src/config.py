class Config:
    def __init__(self):
        self.URL = f"wklejto.pl/"

        self.RANGE = None

        self.THREAD_AMOUNT = None

        self.DB_HOST = "localhost"
        self.DB_PORT = 27017
        self.DB_NAME = "wklejto"
        self.DB_COL = "pastes"

        # Front-end switch.
        # Options: "enabled", "disabled", "min"
        self.FRONT_END_TYPE = "min"

        self.MAX_TRIES = 5
        self.TRY_DELAY = 0.2
