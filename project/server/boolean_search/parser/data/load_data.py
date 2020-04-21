from typing import List, Set, Tuple

import numpy as np
from lxml import etree

from project.server.boolean_search.parser.data.dto import ArticleRawInfo
from project.server.inverted_index.index.dto import WordInformation
from project.server.inverted_index.index.building import (
    get_all_words,
    build_inverted_index,
    get_words_for_document
)
from project.server.inverted_index.index.sorting import (
    map_index_table,
    sort_mapped_data,
    calculate_tf_idf
)
from project.server.inverted_index.processing.process_input import clear_article_entities
from project.server.inverted_index.xml_work.load_data import load_xml_data


def load_articles_data(file_path: str) -> List[WordInformation]:
    """Load data and build inverted index."""

    loaded_data = load_xml_data(file_path)
    stemmed_articles = clear_article_entities(loaded_data)
    words_for_document = get_words_for_document(stemmed_articles)

    words = get_all_words(stemmed_articles)

    inverted_index_table = build_inverted_index(words, stemmed_articles)
    mapped_data = map_index_table(inverted_index_table)

    data_with_tf_idf = calculate_tf_idf(words_for_document, mapped_data)

    return sort_mapped_data(data_with_tf_idf)


def load_raw_data(file_path: str, ids: Set[int]) -> List[ArticleRawInfo]:
    """Load data by input ids."""

    result = []
    utf8_parser = etree.XMLParser(encoding='utf-8')

    with open(file_path) as fobj:
        xml = fobj.read()

    root = etree.fromstring(
        xml.encode('utf-8'),
        utf8_parser
    )

    for document in root.getchildren():

        temp_dict = {}
        input_id = int(document.get('id'))

        if input_id in ids:

            for elem in document.getchildren():

                if elem.tag in ['url', 'title']:
                    temp_dict[elem.tag] = elem.text

            result.append(ArticleRawInfo(**temp_dict))
            temp_dict.clear()

    return result


def convert_to_matrix(input_data: List[WordInformation]) -> List[List[float]]:
    """Convert stats for words to matrix"""

    return [
        [
          stat.tf_idf_value
          for stat in elem.statistics
        ]
        for elem in input_data
    ]


def create_svd(
        input_data: List[List[float]]
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    return np.linalg.svd(input_data)
