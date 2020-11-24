from os import system
import helper_functions as hf
import datetime as dt
from threading import Semaphore


class Logger:
    def __init__(self, config, database, helper):
        self.cfg = config
        self.helper = helper
        self.db = database
        self.progress = 0
        self.goal = len(self.cfg.RANGE)
        self.start_time = dt.datetime.now()
        self.screen_lock = Semaphore(value=1)

    def log_fail(self, scraper, tries, max_tries) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        url = scraper.current_url
        delay = self.cfg.TRY_DELAY

        print(
            f"Failed to resolve website '{url}' ({tries} / {max_tries}). Waiting {delay} second(s)..."
        )

    def log_progress(self, scraper) -> None:
        if not self.cfg.FRONT_END_ENABLED:
            return

        self.screen_lock.acquire()

        hf.clear()

        started = dt.datetime.strftime(self.start_time, "%H:%M:%S")
        elapsed = hf.elapsed_time(self.start_time)
        progress_perc = hf.percentage(self.progress, self.goal)
        failed = len(self.helper.failed)
        protected = len(self.helper.protected)
        failed_perc = hf.percentage(failed, self.goal)
        protected_perc = hf.percentage(protected, self.goal)

        message = f"""
        Currently working on: '{scraper.current_url}'
        Working with: {self.cfg.THREAD_AMOUNT} threads
        Progress: {self.progress} / {self.goal} ({progress_perc:.2f}%) ({self.goal - self.progress} left)
        Pushed: {self.db.pushes}
        Duplicates: {self.db.duplicates}
        Started: {started}
        Elapsed: {elapsed}
        Failed: {failed} / {self.goal} ({failed_perc:.2f}%)
        Protected: {protected} / {self.goal} ({protected_perc:.2f}%)
        \n"""

        print(message)
        self.screen_lock.release()
