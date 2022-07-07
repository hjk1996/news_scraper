from dataclasses import dataclass


@dataclass
class Article:
    text: str
    image_dirs: list[str]
