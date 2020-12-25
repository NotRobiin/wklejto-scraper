from re import search
import datetime as dt
from document import Document


class Website:
    def __init__(self, soup, index: int) -> None:
        self.soup = soup
        self.index = index
        self.password = None
        self.valid = None
        self.content = None
        self.author = None
        self.date = None
        self.empty = None

    def to_doc(self) -> Document:
        self.index = int(self.index)

        if self.has_password():
            doc = Document(protected=self.has_password(), site_id=self.index,)
        else:
            doc = Document(
                protected=self.has_password(),
                author=self.get_author(),
                date=self.get_date(),
                content=self.get_content(),
                site_id=self.index,
            )

        return doc

    def get_content(self) -> str:
        if self.content is None:
            self.content = self.soup.find("pre", {"class": "de1"}).text.replace(
                "\xa0", " "
            )

        return self.content

    def get_author(self) -> str:
        if self.author is None:
            txt = self.soup.find("td", {"class": "tdm"}).text
            pattern = r"(?<=Dodane przez: )(.*)(?= \()"
            self.author = search(pattern, txt).group(0)

        return self.author

    def get_date(self) -> str:
        if self.date is None:
            txt = self.soup.find("td", {"class": "tdm"}).text
            pattern = r"([0-9])+-([0-9])+-([0-9])+ ([0-9])+:([0-9])+"
            match = search(pattern, txt).group(0)
            self.date = dt.datetime.strptime(match, "%Y-%m-%d %H:%M")

        return self.date

    def validate(self) -> bool:
        if self.is_empty():
            return False

        if self.has_password():
            return True

        if self.has_content():
            return True

        return False

    def is_valid(self) -> bool:
        if self.valid is None:
            self.valid = self.validate()

        return self.valid

    def has_content(self) -> bool:
        if self.content is None:
            return bool(self.soup.find("pre", {"class": "de1"}))

        return self.content

    def is_empty(self) -> bool:
        if self.empty is None:
            self.empty = bool(self.soup.find("form", {"id": "formwyslij"}))

        return self.empty

    def has_password(self) -> bool:
        if self.password is None:
            self.password = bool(self.soup.find("input", {"name": "haslo"}))

        return self.password
