import helper_functions as hf


class Helper:
    def __init__(self, config):
        self.cfg = config
        self.failed = []
        self.protected = []

    def log_progress(self, scraper) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        data = {
            "progress": scraper.progress,
            "goal": scraper.goal,
            "start": scraper.start_time,
            "url": scraper.current_url,
            "failed": self.failed,
            "protected": self.protected,
            "pushes": scraper.db.pushes,
            "duplicates": scraper.db.duplicates,
        }

        hf.log_progress(data)

    def log_fail(self, scraper, tries, max_tries) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        data = {
            "url": scraper.current_url,
            "tries": tries,
            "max_tries": max_tries,
            "delay": self.cfg.TRY_DELAY,
        }

        hf.log_fail(data)

    def add_protected(self, site_id) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        self.protected.append({"id": "site_id", "reason": "Password protected"})

    def add_fail(self, site_id, reason="") -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        self.failed.append({"id": site_id, "reason": reason})
