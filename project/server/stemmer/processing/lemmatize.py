from typing import List

import nltk
import string

from project.server.stemmer.xml_load.dto import ArticleInfoStemmed

from nltk.corpus import stopwords
from pymystem3 import Mystem

nltk.download("stopwords", quiet=True)


def process_input(
        input_data: List[ArticleInfoStemmed]
) -> List[ArticleInfoStemmed]:
    """Remove stop words and lemmatize input."""
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', 'к', 'на'])

    my_stemmer = Mystem()
    result = []

    for elem in input_data:
        title_without_sw = ' '.join(
            [
                elem1
                for elem1 in elem.title.split(' ')
                if elem1 not in stop_words and elem1 not in string.punctuation
            ]
        )

        text_without_sw = ' '.join(
            [
                elem1
                for elem1 in elem.text.split(' ')
                if elem1 not in stop_words and elem1 not in string.punctuation
            ]
        )

        final_title = ' '.join(
            my_stemmer.lemmatize(title_without_sw)
        ).replace(
            '\n', ' '
        ).replace(
            '.', ' '
        ).replace(
            '-', ' '
        )

        final_text = ' '.join(
            my_stemmer.lemmatize(text_without_sw)
        ).replace(
            '\n', ''
        ).replace(
            '.', ''
        ).replace(
            '-', ' '
        )

        result.append(
            ArticleInfoStemmed(
                title=final_title,
                text=final_text
            )
        )

    return result
