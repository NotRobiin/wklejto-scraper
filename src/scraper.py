import requests
import time
import datetime as dt
from bs4 import BeautifulSoup as bs
import helper_functions as helper
from document import Document
from website import Website
from typing import Union


class Scraper:
    def __init__(self, config, database):
        self.cfg = config
        self.db = database
        self.ids = self.cfg.RANGE
        self.failed = []
        self.protected = []
        self.progress = 0
        self.goal = len(self.ids)
        self.start_time = None
        self.current_url = ""

    def start(self) -> None:
        self.start_time = dt.datetime.now()

        for site_id in self.ids:
            self.progress += 1
            self.current_url = self.get_url(site_id)

            self.log_progress()

            soup = self.download(site_id)

            if soup is None:
                self.add_fail(site_id, reason="Failed to download data")
                continue

            site = Website(soup, index=site_id)
            site.password = site.is_password_protected()
            site.valid = site.is_valid()

            if site.password:
                self.add_protected(site.index)

            if not site.valid:
                self.add_fail(site.index, reason="Invalid website content")
                continue

            if site.password:
                doc = Document(protected=site.password, site_id=site.index)
            else:
                doc = Document(
                    protected=site.password,
                    author=site.get_author(),
                    date=site.get_date(),
                    content=site.get_content(),
                    site_id=site.index,
                )

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
                self.log_progress()
                self.log_fail(tries, self.cfg.MAX_TRIES)

                time.sleep(self.cfg.TRY_DELAY)

        if code == 200:
            soup = bs(request.content, "html.parser")

        return soup

    def log_progress(self) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        data = {
            "progress": self.progress,
            "goal": self.goal,
            "start": self.start_time,
            "url": self.current_url,
            "failed": self.failed,
            "protected": self.protected,
            "pushes": self.db.pushes,
            "duplicates": self.db.duplicates,
        }

        helper.log_progress(data)

    def log_fail(self, tries, max_tries) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        data = {
            "url": self.current_url,
            "tries": tries,
            "max_tries": max_tries,
            "delay": self.cfg.TRY_DELAY,
        }

        helper.log_fail(data)

    def add_protected(self, site_id) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        self.protected.append({"id": "site_id", "reason": "Password protected"})

    def add_fail(self, site_id, reason="") -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        self.failed.append({"id": site_id, "reason": reason})

    def get_url(self, i) -> str:
        return f"http://{self.cfg.URL}{i}"
