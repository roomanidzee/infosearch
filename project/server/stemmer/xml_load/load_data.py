
from typing import List

from lxml import etree

from project.server.stemmer.xml_load.dto import ArticleInfoStemmed


def load_xml_data(file_path: str) -> List[ArticleInfoStemmed]:
    """Load XML data into dataclasses"""

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

        for elem in document.getchildren():

            if elem.tag in ['title', 'text']:
                temp_dict[elem.tag] = elem.text

        result.append(ArticleInfoStemmed(**temp_dict))
        temp_dict.clear()

    return result
