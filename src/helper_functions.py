import datetime as dt
from os import system


def percentage(a, b) -> float:
    return float(100.0 * a / b)


def elapsed_time(from_time) -> str:
    sec_elapsed = (dt.datetime.now() - from_time).total_seconds()
    elapsed = str(dt.timedelta(seconds=sec_elapsed))[:-7]

    return elapsed


def log_fail(data) -> None:
    url = data["url"]
    tries = data["tries"]
    max_tries = data["max_tries"]
    delay = data["delay"]

    print(
        f"Failed to resolve website '{url}' ({tries} / {max_tries}). Waiting {delay} second(s)..."
    )


def log_progress(data) -> None:
    system("cls")

    p = data["progress"]
    goal = data["goal"]
    url = data["url"]
    failed = len(data["failed"])
    prot = len(data["protected"])
    pushes = data["pushes"]
    dupl = data["duplicates"]

    progress = percentage(p, goal)
    fail_perc = percentage(failed, goal)
    prot_perc = percentage(prot, goal)
    started = dt.datetime.strftime(data["start"], "%H:%M:%S")
    elapsed = elapsed_time(data["start"])

    print(f"Currently working on: '{url}'")
    print(f"Progress: {p} / {goal} ({progress:.2f}%) ({goal - p} left)")
    print(f"Pushed: {pushes}")
    print(f"Duplicates: {dupl}")
    print(f"Started: {started}")
    print(f"Elapsed: {elapsed}")
    print(f"Failed: {failed} / {goal} ({fail_perc:.2f}%)")
    print(f"Protected: {prot} / {goal} ({prot_perc:.2f}%)")
    print("\n")


def fix_spaces(e) -> str:
    return e.replace("\xa0", " ")
