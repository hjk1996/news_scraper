from dataclasses import dataclass


@dataclass
class ArticleInfo:
    id: str
    url: str


@dataclass
class Article:
    id: str
    text: str
    image_dirs: list[str] | None
