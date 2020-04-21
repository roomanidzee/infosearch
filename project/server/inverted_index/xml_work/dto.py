
from typing import List
from dataclasses import dataclass


@dataclass
class ArticleEntity:
    """Class for representing Article entity from xml."""
    id: int
    title: str
    text: str
    keywords: List[str]
