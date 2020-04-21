
from typing import List

from lxml import etree

from project.server.inverted_index.index.dto import WordInformation


def create_xml(
    word_info: List[WordInformation],
    path: str,
    action: str
):
    """Create XML with word information."""

    page = etree.Element('terms')

    if action == 'simple':
        for elem in word_info:
            term = etree.Element(
                'term',
                value=elem.value
            )

            for attr in elem.statistics:

                if attr.count_value != 0:
                    term.append(
                        etree.Element(
                            'doc',
                            id=str(attr.doc_id),
                            count=str(attr.count_value)
                        )
                    )

            page.append(term)

        doc = etree.ElementTree(page)
        doc.write(
            path,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        )
    elif action == 'tf_idf':
        for elem in word_info:
            term = etree.Element(
                'term',
                value=elem.value
            )

            for attr in elem.statistics:

                if attr.count_value != 0:

                    attrs = {
                        'id': str(attr.doc_id),
                        'count': str(attr.count_value),
                        'tf-idf': str(attr.tf_idf_value)
                    }

                    term.append(
                        etree.Element(
                            'doc',
                            attrs
                        )
                    )

            page.append(term)

        doc = etree.ElementTree(page)
        doc.write(
            path,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        )
