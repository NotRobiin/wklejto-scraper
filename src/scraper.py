import requests
import time
from bs4 import BeautifulSoup as bs
from document import Document
from website import Website
from typing import Union


class Scraper:
    def __init__(self, site_id, config, helper, database, logger):
        self.cfg = config
        self.db = database
        self.helper = helper
        self.logger = logger
        self.site_id = site_id
        self.current_url = self.get_url(self.site_id)

    def scrape(self) -> int:
        self.logger.progress += 1
        self.logger.log_progress(self)

        soup = self.download(self.site_id)

        if soup is None:
            self.helper.add_fail(self.site_id, reason="Failed to download data")
            return 0

        site = Website(soup, index=self.site_id)

        if site.has_password():
            self.helper.add_protected(site.index)

        if not site.is_valid():
            self.helper.add_fail(site.index, reason="Invalid website content")
            return 0

        doc = site.to_doc()
        self.db.insert(doc)

        return 1

    def make_request(self) -> set:
        req = requests.get(self.current_url)
        code = req.status_code

        return (req, code)

    def download(self, site_id) -> Union[None, bs]:
        tries, code = 0, 0
        request, soup = None, None

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
        url = self.cfg.URL

        if not url.startswith("http://") and not url.startswith("https://"):
            return f"http://{url}{i}"

        return f"{self.cfg.URL}{i}"
