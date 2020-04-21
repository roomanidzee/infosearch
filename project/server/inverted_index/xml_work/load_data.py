from typing import List

from lxml import etree

from project.server.inverted_index.xml_work.dto import ArticleEntity


def load_xml_data(file_path: str) -> List[ArticleEntity]:
    """Retreive article data from xml file."""

    result = []
    utf8_parser = etree.XMLParser(encoding='utf-8')

    with open(file_path) as fobj:
        xml = fobj.read()

    root = etree.fromstring(
        xml.encode('utf-8'),
        utf8_parser
    )

    for document in root.getchildren():

        temp_dict = {
            'id': int(document.get('id'))
        }

        for elem in document.getchildren():

            if elem.tag in ['title', 'text']:
                temp_dict[elem.tag] = elem.text

            if elem.tag == 'keywords':
                temp_dict[elem.tag] = elem.text.split(',')

        result.append(ArticleEntity(**temp_dict))
        temp_dict.clear()

    return result
