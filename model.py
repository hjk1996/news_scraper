from ast import keyword
from dataclasses import dataclass, field
from datetime import datetime



@dataclass
class ArticleInfo:
    id: str = field(repr=True, hash=True)
    _date: str = field(repr=False)
    press: str = field(repr=True)
    reporter: str | None = field(repr=False)
    title: str = field(repr=True)
    _category1: str | None = field(repr=False)
    _category2: str | None = field(repr=False)
    _category3: str | None = field(repr=False)
    _event_type_1: str | None = field(repr=False)
    _event_type_2: str | None = field(repr=False)
    _event_type_3: str | None = field(repr=False)
    _related_people: str | None = field(repr=False)
    _related_location: str | None = field(repr=False)
    _related_institutions: str | None = field(repr=False)
    _keywords: str = field(repr=False)
    _features: str = field(repr=False)
    content_preview: str = field(repr=False)
    url: str = field(repr=False)
    excluded: bool | None = field(repr=False)
    content: str | None = field(repr=False)
    search_keyword: str = field(repr=False) 
    image_urls: list[str] | None = field(repr=False)

    date: datetime = field(repr=True, init=False)
    category1: list[str] | None = field(repr=False, init=False)
    category2: list[str] | None = field(repr=False, init=False)
    category3: list[str] | None = field(repr=False, init=False)
    event_type_1: list[str] | None = field(repr=False, init=False)
    event_type_2: list[str] | None = field(repr=False, init=False)
    event_type_3: list[str] | None = field(repr=False, init=False)
    related_people: list[str] | None = field(repr=False, init=False)
    related_location: list[str] | None = field(repr=False, init=False)
    related_institutions: list[str] | None = field(repr=False, init=False)
    keywords: list[str] = field(repr=False, init=False)
    features: list[str] = field(repr=False, init=False)

    def __post_init__(self):
        self.date = datetime.strptime(self._date, "%Y%m%d")
        self.category1 = self._category1.split(">") if self._category1 else None
        self.category2 = self._category2.split(">") if self._category2 else None
        self.category3 = self._category3.split(">") if self._category3 else None
        self.event_type_1 = self._event_type_1.split(">") if self._event_type_1 else None
        self.event_type_2 = self._event_type_2.split(">") if self._event_type_2 else None
        self.event_type_3 = self._event_type_3.split(">") if self._event_type_3 else None
        self.related_people = self._related_people.split(",") if self._related_people else None
        self.related_location = self._related_location.split(",") if self._related_location else None
        self.related_institutions = self._related_institutions.split(",") if self._related_institutions else None
        self.keywords = self._keywords.split(",") if self._keywords else None
        self.features = self._features.split(",") if self._features else None

        



@dataclass
class Article:
    id: str
    text: str
    image_dirs: list[str] | None
