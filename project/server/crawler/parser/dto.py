from typing import List
from dataclasses import dataclass


@dataclass
class ArticleInfo:
    """Information about article."""
    url: str
    title: str
    text: str
    keywords: List[str]