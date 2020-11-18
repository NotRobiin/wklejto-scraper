class Config:
    def __init__(self):
        # wklejto.pl/{ID} - Front-end finished paste
        # wklejto.pl/txt{ID} - Raw text. Password front-end still occurs
        self.URL = f"wklejto.pl/"

        self.RANGE = range(120, 50_000)

        self.DB_HOST = "localhost"
        self.DB_PORT = 27017
        self.DB_NAME = "wklejto"
        self.DB_COL = "pastes"

        # Toggles prints and logs
        self.FRONT_END_ENABLED = True

        self.LOAD_DELAY = 0.2

        self.CONTENT_LOAD_DELAY = 1.0

        self.MAX_TRIES = 5
        self.TRY_DELAY = 0.6
