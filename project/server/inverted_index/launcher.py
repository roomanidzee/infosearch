
from pathlib import Path

from project.server.inverted_index.index.building import (
    get_all_words,
    build_inverted_index,
    get_words_for_document
)
from project.server.inverted_index.index.sorting import (
    map_index_table,
    sort_mapped_data,
    calculate_tf_idf
)
from project.server.inverted_index.processing.process_input import clear_article_entities
from project.server.inverted_index.xml_work.create_xml import create_xml
from project.server.inverted_index.xml_work.load_data import load_xml_data

if __name__ == '__main__':

    file_path = Path(__file__).parent.parent / Path('crawler/article_results.xml')

    loaded_data = load_xml_data(str(file_path))
    stemmed_articles = clear_article_entities(loaded_data)

    words = get_all_words(stemmed_articles)
    words_for_document = get_words_for_document(stemmed_articles)

    inverted_index_table = build_inverted_index(words, stemmed_articles)
    mapped_data = map_index_table(inverted_index_table)

    sorted_data = sort_mapped_data(mapped_data)

    create_xml(
        sorted_data,
        'inverted_index.xml',
        'simple'
    )

    data_with_tf_idf = calculate_tf_idf(words_for_document, mapped_data)

    sorted_tf_idf_data = sort_mapped_data(data_with_tf_idf)
    create_xml(
        sorted_tf_idf_data,
        'inverted_index(tf_idf).xml',
        'tf_idf'
    )

    '''debugging
    for elem in mapped_data:

        if elem.value in ['слава', 'гнойный', 'кпсс', 'юрий', 'дудь', 'оксимирон']:
            print(elem.value)

            for attr in elem.statistics:

                if attr.count_value != 0:
                    print(attr)
    '''
