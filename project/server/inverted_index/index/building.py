from typing import DefaultDict, List, Set, Dict
from collections import defaultdict

from project.server.inverted_index.index.dto import WordStatistic
from project.server.inverted_index.xml_work.dto import ArticleEntity

INDEX_TABLE_TYPE = DefaultDict[str, List[WordStatistic]]


def get_all_words(input_data: List[ArticleEntity]) -> Set[str]:
    """Get all words from input data."""

    result = set()

    for elem in input_data:
        result.update(elem.title.split(' '))
        result.update(elem.text.split(' '))
        result.update(elem.keywords)

    return {
        elem
        for elem in result
        if (
               not elem.startswith('0')
           ) and (
               not (elem.isnumeric() or len(elem) == 1)
           ) and (
               not ((len(elem) <= 5) and (any(sym.isnumeric() for sym in elem)))
           ) and(
               not 'pictwittercom' in elem
           )
    }


def build_inverted_index(
        words: Set[str],
        input_data: List[ArticleEntity]
) -> INDEX_TABLE_TYPE:
    """Building of inverted index tree."""

    words_dict: INDEX_TABLE_TYPE = defaultdict(list)
    temp_storage = []

    for elem in words:

        for article in input_data:
            temp_storage.extend(article.title.split(' '))
            temp_storage.extend(article.text.split(' '))
            temp_storage.extend(article.keywords)

            words_dict[elem].append(
                WordStatistic(
                    doc_id=article.id,
                    count_value=temp_storage.count(elem)
                )
            )

            temp_storage.clear()

    return words_dict


def get_words_for_document(
     input_data: List[ArticleEntity]
) -> Dict[int, int]:
    """Retrieve words count for each document."""

    result_dict = {}
    temp_storage = []

    for article in input_data:
        temp_storage.extend(article.title.split(' '))
        temp_storage.extend(article.text.split(' '))
        temp_storage.extend(article.keywords)

        result_dict[article.id] = len(temp_storage)
        temp_storage.clear()

    return result_dict
