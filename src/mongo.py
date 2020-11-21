import pymongo
from document import Document


class Database:
    def __init__(self, config):
        self.cfg = config
        self.pushes = 0
        self.duplicates = 0

    def __del__(self):
        print(f"Closing database connection. Inserted documents: {self.pushes}")

    def start(self, confirm):
        self.host = self.cfg.DB_HOST
        self.port = self.cfg.DB_PORT
        self.db_name = self.cfg.DB_NAME
        self.col_name = self.cfg.DB_COL

        self.client = pymongo.MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        self.col = self.db[self.col_name]

        confirm = False or confirm

        if confirm and self.db_name in self.client.list_database_names():
            print(f'Database "{self.db_name}" already exists.')

    def insert(self, doc: Document) -> int:
        if self.col.find_one({"site_id": doc.site_id}):
            self.duplicates += 1

            return -1

        data = doc.get()
        ret = self.col.insert_one(data)

        self.pushes += 1

        return ret