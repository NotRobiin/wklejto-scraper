import requests
import time
import datetime as dt
from bs4 import BeautifulSoup as bs
from document import Document
from website import Website
from typing import Union
from helper import Helper


class Scraper:
    def __init__(self, config, database):
        self.cfg = config
        self.db = database
        self.helper = Helper(self.cfg)
        self.ids = self.cfg.RANGE
        self.progress = 0
        self.goal = len(self.ids)
        self.start_time = None
        self.current_url = ""

    def start(self) -> None:
        self.start_time = dt.datetime.now()

        for site_id in self.ids:
            self.progress += 1
            self.current_url = self.get_url(site_id)

            self.helper.log_progress(self)

            soup = self.download(site_id)

            if soup is None:
                self.helper.add_fail(site_id, reason="Failed to download data")
                continue

            site = Website(soup, index=site_id)

            if site.has_password():
                self.helper.add_protected(site.index)

            if not site.is_valid():
                self.helper.add_fail(site.index, reason="Invalid website content")
                continue

            doc = site.to_doc()
            self.db.insert(doc)

    def make_request(self) -> set:
        req = requests.get(self.current_url)
        code = req.status_code

        return (req, code)

    def download(self, site_id) -> Union[None, bs]:
        tries = 0
        request = None
        code = 0
        soup = None

        while code != 200 and tries < self.cfg.MAX_TRIES:
            tries += 1

            try:
                request, code = self.make_request()
            except:
                self.helper.log_progress(self)
                self.helper.log_fail(self, tries, self.cfg.MAX_TRIES)

                time.sleep(self.cfg.TRY_DELAY)

        if code == 200:
            soup = bs(request.content, "html.parser")

        return soup

    def get_url(self, i) -> str:
        return f"http://{self.cfg.URL}{i}"
