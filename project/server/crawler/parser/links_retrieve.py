
import time
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup


def get_source_links() -> List[str]:
    """Retrieve links for articles from file."""
    file_path = Path(__file__).parent.parent / Path("urls.txt")

    file_source = open(str(file_path), 'r')
    lines = file_source.readlines()
    file_source.close()

    lines = [
        elem.replace('\n', '')
        for elem in lines
    ]

    return lines


def get_articles_links(
    source_links: List[str]
) -> List[str]:
    """Retrieve links to articles."""
    result = []

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36 '
    }

    for elem in source_links:
        time.sleep(120)

        html_content = requests.get(elem, headers=headers).content
        soup = BeautifulSoup(html_content, 'lxml')

        container = soup.select_one('div.grid-container div.feed-grid')

        for elem1 in container.select('div.row div a.post-grid-link[href]'):
            result.append(elem1['href'])
        
        print(f'Collected links from url {elem}')
    
    print('\n')

    return result
