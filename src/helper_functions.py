import datetime as dt
from os import system
from bs4 import BeautifulSoup as bs
from re import search


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


def get_content(soup):
    txt = soup.find("pre", {"class": "de1"}).text.replace("\xa0", " ")

    return txt


def get_author(soup) -> str:
    txt = soup.find("td", {"class": "tdm"}).text
    pattern = r"(?<=Dodane przez: )(.*)(?= \()"
    date = search(pattern, txt).group(0)

    return date


def get_date(soup) -> str:
    txt = soup.find("td", {"class": "tdm"}).text
    pattern = r"([0-9])+-([0-9])+-([0-9])+ ([0-9])+:([0-9])+"
    match = search(pattern, txt).group(0)
    date = dt.datetime.strptime(match, "%Y-%m-%d %H:%M")

    return date


def is_valid_page(soup) -> bool:
    if empty_page(soup):
        return False

    if is_password_protected(soup):
        return True

    if has_content(soup):
        return True

    return False


def has_content(soup) -> bool:
    content = soup.find("pre", {"class": "de1"})

    return bool(content is not None)


def empty_page(soup) -> bool:
    el = soup.find("form", {"id": "formwyslij"})

    return bool(el is not None)


def is_password_protected(soup) -> bool:
    password = soup.find("input", {"name": "haslo"})

    return bool(password is not None)
