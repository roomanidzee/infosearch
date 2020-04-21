
from pathlib import Path

from project.server.stemmer.xml_load.load_data import load_xml_data
from project.server.stemmer.processing import clear_text, lemmatize

if __name__ == '__main__':

    file_path = Path(__file__).parent.parent / Path('crawler/article_results.xml')
    loaded_data = load_xml_data(str(file_path))

    cleared_data = clear_text.remove_special_symbols(loaded_data)
    lemmatized_data = lemmatize.process_input(cleared_data)

    with open('result_data.txt', 'w', encoding='utf-8') as file_obj:
        for elem in lemmatized_data:
            file_obj.write("%s\n" % str(elem))
