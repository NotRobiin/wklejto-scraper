class Document:
    __slots__ = ["protected", "author", "date", "content", "site_id"]

    def __init__(self, **kwargs) -> None:
        for key in self.__slots__:
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, None)

    def get(self) -> dict["str"]:
        return {x: getattr(self, x) for x in self.__slots__}

