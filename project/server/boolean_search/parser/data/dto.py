
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ArticleRawInfo:
    url: str
    title: str


@dataclass
class ArticleQueryResult:
    query: str
    data: Optional[List[ArticleRawInfo]]
    ranged_value: float = 0.0
    cosinus_value: float = 0.0


@dataclass
class ArticleVectorResult:
    query: str
    url: str
    cosinus_value: float
