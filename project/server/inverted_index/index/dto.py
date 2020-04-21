from typing import List
from dataclasses import dataclass


@dataclass
class WordStatistic:
    """Class for representing word statistic in input corpus."""
    doc_id: int
    count_value: int
    tf_idf_value: float = 0.0


@dataclass
class WordInformation:
    """Class for representing fully-qualified info about word."""
    value: str
    statistics: List[WordStatistic]
