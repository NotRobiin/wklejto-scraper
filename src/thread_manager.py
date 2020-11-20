import threading
from scraper import Scraper


class NewThread(threading.Thread):
    def __init__(self, ids, config, database, helper, logger):
        threading.Thread.__init__(self)
        self.ids = ids
        self.cfg = config
        self.db = database
        self.helper = helper
        self.logger = logger

    def run(self):
        for site in self.ids:
            sc = Scraper(
                site_id=site,
                config=self.cfg,
                database=self.db,
                helper=self.helper,
                logger=self.logger,
            )
            sc.scrape()
