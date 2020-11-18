import requests
import time
import datetime as dt
from bs4 import BeautifulSoup as bs
import helper_functions as helper
from document import Document


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

            password = helper.is_password_protected(soup)
            valid = helper.is_valid_page(soup)

            if password:
                self.add_protected(site_id)

            if not valid:
                self.add_fail(site_id, reason="Invalid website content")
                continue

            if password:
                doc = Document(protected=password, site_id=site_id)
            else:
                doc = Document(
                    protected=password,
                    author=helper.get_author(soup),
                    date=helper.get_date(soup),
                    content=helper.get_content(soup),
                    site_id=site_id,
                )

            self.db.insert(doc)

    def make_request(self):
        req = requests.get(self.current_url)
        code = req.status_code

        return (req, code)

    def download(self, site_id):
        tries = 0
        request = None
        code = 0
        soup = None

        while code != 200 and tries < self.cfg.MAX_TRIES:
            try:
                request, code = self.make_request()
            except:
                self.log_progress()
                self.log_fail(tries, self.cfg.MAX_TRIES)

                time.sleep(self.cfg.TRY_DELAY)

            tries += 1

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
