from typing import List

from project.server.inverted_index.xml_work.dto import ArticleEntity
from project.server.stemmer.xml_load.dto import ArticleInfoStemmed
from project.server.stemmer.processing import clear_text, lemmatize


def clear_article_entities(
        input_data: List[ArticleEntity]
) -> List[ArticleEntity]:
    """Stemming article info from XML."""

    articles = sorted(input_data, key=lambda x: x.id)

    data_for_stemming = [
        ArticleInfoStemmed(
            title=elem.title,
            text=elem.text
        )
        for elem in articles
    ]

    cleared_data = clear_text.remove_special_symbols(data_for_stemming)
    simplified_data = lemmatize.process_input(cleared_data)

    for raw_elem, stemmed_elem in zip(articles, simplified_data):
        raw_elem.title = stemmed_elem.title
        raw_elem.text = stemmed_elem.text

        # replace multiple whitespaces by one
        raw_elem.title = ' '.join(raw_elem.title.split())
        raw_elem.text = ' '.join(raw_elem.text.split())

    for elem in articles:
        keywords = elem.keywords
        elem.keywords = []

        for attr in keywords:
            elem.keywords.extend(attr.lower().split(' '))

    return articles
