
import time

import requests
from bs4 import BeautifulSoup

from project.server.crawler.parser.dto import ArticleInfo


def get_article_info(elem: str) -> ArticleInfo:
    """Retrieve information from articles."""

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36 '
    }

    time.sleep(60)
    print(f"Collecting info from link {elem}...")

    html_content = requests.get(elem, headers=headers).content
    soup = BeautifulSoup(html_content, 'lxml')

    base = 'div.grid-container div.single-post-grid div'

    title_query = f'{base} div.post-header div.post-header-container div.post-header-title div.the_title'

    title = soup.select_one(title_query).get_text()

    text_query = f'{base} div.post-inside div.post-content p'
    text_parts = []

    for elem1 in soup.select(text_query):
        temp_text = elem1.get_text().replace(
            '<strong>', ''
        ).replace(
            '</strong>', ''
        )

        text_parts.append(temp_text)

    full_text = ' '.join(text_parts)

    tags_query = f'{base} div.post-inside div.post-content div.tags a'
    tags = []

    for elem1 in soup.select(tags_query):
        tags.append(elem1.get_text())

    article = ArticleInfo(
        url=elem,
        title=title,
        text=full_text,
        keywords=tags
    )

    print(article)

    return article
