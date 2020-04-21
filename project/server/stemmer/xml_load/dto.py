from dataclasses import dataclass


@dataclass
class ArticleInfoStemmed:
    """Dataclass for representing stemmed data."""
    title: str
    text: str
