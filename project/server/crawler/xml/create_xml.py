
from typing import List

from lxml import etree

from project.server.crawler.parser.dto import ArticleInfo


def create_xml(
    articles: List[ArticleInfo],
    path: str
):
    """Create XML file with input articles."""

    page = etree.Element('documents')
    counter = 1

    for elem in articles:
        document = etree.Element(
            'document',
            id=str(counter)
        )

        url = etree.Element(
            'url'
        )
        url.text = elem.url

        title = etree.Element(
            'title'
        )
        title.text = elem.title

        text_elem = etree.Element(
            'text'
        )
        text_elem.text = elem.text

        keywords = etree.Element(
            'keywords'
        )
        keywords.text = ','.join(elem.keywords)

        document.append(url)
        document.append(title)
        document.append(text_elem)
        document.append(keywords)

        page.append(document)
        counter += 1

    doc = etree.ElementTree(page)
    doc.write(
        path,
        pretty_print=True,
        xml_declaration=True,
        encoding='UTF-8'
    )
