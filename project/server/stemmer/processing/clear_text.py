import re
from typing import List

from project.server.stemmer.xml_load.dto import ArticleInfoStemmed


def remove_special_symbols(
        input_data: List[ArticleInfoStemmed]
) -> List[ArticleInfoStemmed]:
    """Clear text from special symbols."""

    result = []

    re_emoji = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')

    for elem in input_data:
        cleared_title = re.sub('[^а-яА-Яa-zA-Z0-9 -]', '', elem.title)

        cleared_text = re.sub('[^а-яА-Яa-zA-Z0-9 -]', '', elem.text)
        cleared_text = re.sub('http\S+', '', cleared_text)
        cleared_text = re_emoji.sub(r'', cleared_text)

        result.append(
            ArticleInfoStemmed(
                title=cleared_title.lower(),
                text=cleared_text.lower()
            )
        )

    return result
