from pathlib import Path

from project.server.crawler.parser.links_retrieve import (
    get_source_links,
    get_articles_links,
)
from project.server.crawler.parser.article_info_retrieve import get_article_info
from project.server.crawler.xml.create_xml import create_xml

from multiprocessing import Pool

if __name__ == '__main__':
    file_path = Path(__file__) / Path('articles.xml')

    article_links = get_articles_links(
        get_source_links()
    )

    with Pool(10) as p:
        articles = p.map(get_article_info, article_links)

    create_xml(
        articles,
        'article_results.xml'
    )
