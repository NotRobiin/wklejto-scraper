import datetime as dt
from os import system


def percentage(a, b):
    return 100.0 * a / b


def elapsed_time(from_time):
    sec_elapsed = (dt.datetime.now() - from_time).total_seconds()
    elapsed = str(dt.timedelta(seconds=sec_elapsed))[:-7]

    return elapsed


def log_fail(data):
    url = data["url"]
    tries = data["tries"]
    max_tries = data["max_tries"]
    delay = data["delay"]

    print(
        f"Failed to resolve website '{url}' ({tries} / {max_tries}). Waiting {delay} second(s)..."
    )


def log_progress(data):
    system("cls")

    p = data["progress"]
    goal = data["goal"]
    start = data["start"]
    url = data["url"]
    failed = data["failed"]
    prot = data["protected"]
    pushes = data["pushes"]
    dupl = data["duplicates"]

    progress_perc = percentage(p, goal)
    fail_perc = percentage(len(failed), goal)
    prot_perc = percentage(len(prot), goal)
    left = goal - p
    started = dt.datetime.strftime(start, "%H:%M:%S")
    elapsed = elapsed_time(start)

    print(f"Currently working on: '{url}'")
    print(f"Progress: {p} / {goal} ({progress_perc:.2f}%) ({left} left)")
    print(f"Pushed: {pushes}")
    print(f"Duplicates: {dupl}")
    print(f"Started: {started}")
    print(f"Elapsed: {elapsed}")
    print(f"Failed: {len(failed)} / {goal} ({fail_perc:.2f}%)")
    print(f"Protected: {len(prot)} / {goal} ({prot_perc:.2f}%)")
    print("\n")


def fix_spaces(e):
    return e.replace("\xa0", " ")
