import datetime as dt
from os import system, name


def percentage(a, b) -> float:
    return float(100.0 * a / b)


def elapsed_time(from_time) -> str:
    sec_elapsed = (dt.datetime.now() - from_time).total_seconds()
    elapsed = str(dt.timedelta(seconds=sec_elapsed))[:-7]

    return elapsed


def clear() -> None:
    if name == "nt":
        system("cls")
    else:
        system("clear")


def fix_spaces(e) -> str:
    return e.replace("\xa0", " ")
