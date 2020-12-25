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

    def log_fail(self, scraper, tries) -> None:
        if self.cfg.FRONT_END_TYPE in ["min", "disabled"]:
            return

        url = scraper.current_url
        delay = self.cfg.TRY_DELAY
        mx = self.cfg.MAX_TRIES

        print(
            f"Failed to resolve website '{url}' ({tries} / {mx}). Waiting {delay} second(s)..."
        )

    def log_progress(self, scraper) -> None:
        if self.cfg.FRONT_END_TYPE == "disabled":
            return

        self.screen_lock.acquire()
        hf.clear()

        is_min = self.cfg.FRONT_END_TYPE == "min"
        message = is_min and self.format_min_log(scraper) or self.format_log(scraper)

        print(message)
        self.screen_lock.release()

    def format_min_log(self, scraper) -> str:
        started = dt.datetime.strftime(self.start_time, "%H:%M:%S")
        elapsed = hf.elapsed_time(self.start_time)
        progress_perc = f"{hf.percentage(self.progress, self.goal):.2f}"
        failed = len(self.helper.failed)
        protected = len(self.helper.protected)

        msg = f"{'Start':<14}{'Elapsed':<14}{'Pushed':<14}{'Failed':<14}{'Protected':<14}{'Progress'}\n"
        msg += f"{started:<14}{elapsed:<14}{self.db.pushes:<14}{failed:<14}{protected:<14}{progress_perc}%"
        msg = msg.strip()
        msg += "\n\n"

        return msg

    def format_log(self, scraper) -> str:
        started = dt.datetime.strftime(self.start_time, "%H:%M:%S")
        elapsed = hf.elapsed_time(self.start_time)
        progress_perc = f"{hf.percentage(self.progress, self.goal):.2f}"
        failed = len(self.helper.failed)
        protected = len(self.helper.protected)
        failed_perc = hf.percentage(failed, self.goal)
        protected_perc = hf.percentage(protected, self.goal)

        msg = f"""
        Currently working on: '{scraper.current_url}'
        Working with: {self.cfg.THREAD_AMOUNT} threads
        Progress: {self.progress} / {self.goal} ({progress_perc}%) ({self.goal - self.progress} left)
        Pushed: {self.db.pushes}
        Duplicates: {self.db.duplicates}
        Started: {started}
        Elapsed: {elapsed}
        Failed: {failed} ({failed_perc:.2f}%)
        Protected: {protected} ({protected_perc:.2f}%)
        \n"""

        return msg
