from re import search
import datetime as dt


class Website:
    def __init__(self, soup, index):
        self.soup = None or soup

        self.index = None or index
        self.password = None
        self.valid = None
        self.content = None

    def get_content(self) -> str:
        txt = self.soup.find("pre", {"class": "de1"}).text.replace("\xa0", " ")

        return txt

    def get_author(self) -> str:
        txt = self.soup.find("td", {"class": "tdm"}).text
        pattern = r"(?<=Dodane przez: )(.*)(?= \()"
        date = search(pattern, txt).group(0)

        return date

    def get_date(self) -> str:
        txt = self.soup.find("td", {"class": "tdm"}).text
        pattern = r"([0-9])+-([0-9])+-([0-9])+ ([0-9])+:([0-9])+"
        match = search(pattern, txt).group(0)
        date = dt.datetime.strptime(match, "%Y-%m-%d %H:%M")

        return date

    def is_valid(self) -> bool:
        if self.is_empty():
            return False

        if self.is_password_protected():
            return True

        if self.has_content():
            return True

        return False

    def has_content(self) -> bool:
        content = self.soup.find("pre", {"class": "de1"})

        return bool(content is not None)

    def is_empty(self) -> bool:
        el = self.soup.find("form", {"id": "formwyslij"})

        return bool(el is not None)

    def is_password_protected(self) -> bool:
        p = self.soup.find("input", {"name": "haslo"})

        return bool(p is not None)
