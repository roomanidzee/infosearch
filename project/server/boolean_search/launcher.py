import json
from pathlib import Path
from typing import List
from dataclasses import asdict

from project.server.boolean_search.parser.data.dto import (
    ArticleQueryResult,
    ArticleVectorResult,
)
from project.server.boolean_search.parser.data.load_data import (
    load_articles_data,
    load_raw_data
)
from project.server.boolean_search.parser.queries.search import (
    not_query,
    intersection_query,
    calculate_ranged_value,
    calculate_cosinus_value,
    calculate_cosinus_value_for_lsi
)
from project.server.inverted_index.index.dto import WordInformation


def process_query(
        search_file_path: str,
        query_input: str,
        input_data: List[WordInformation]
) -> ArticleQueryResult:
    """Method for processing input search query."""
    parts = query_input.split(' ')

    if len(parts) <= 1:
        raise ValueError('Unsupported query type')

    not_query_columns = [
        elem
        for elem in parts
        if elem.startswith('-')
    ]

    intersection_columns = [
        elem
        for elem in parts
        if not elem.startswith('-')
    ]

    if (not not_query_columns) and (not intersection_columns):
        raise ValueError('Unsupported query type')

    result_ids = set()
    not_query_result = list()
    ranged_value = 0.0
    cosinus_value = 0.0

    if not_query_columns:

        not_query_columns = [
            elem.replace('-', '')
            for elem in not_query_columns
        ]

        for elem in not_query_columns:
            not_query_result.extend(
                not_query(elem, input_data)
            )

        if not not_query_result:
            return ArticleQueryResult(
                query=query_input,
                data=[],
            )

        if intersection_columns:

            intersection_result = intersection_query(
                intersection_columns,
                not_query_result
            )

            if not intersection_result:
                return ArticleQueryResult(
                    query=query_input,
                    data=[]
                )

            result_ids.update(intersection_result)

            ranged_value = calculate_ranged_value(
                intersection_columns,
                result_ids,
                not_query_result
            )

            # cosinus_value = calculate_cosinus_value(
            # intersection_columns,
            # result_ids,
            # not_query_result
            # )
            cosinus_value = calculate_cosinus_value_for_lsi(
                intersection_columns,
                result_ids,
                not_query_result,
                input_data
            )

        else:

            result_ids.update(
                [
                    stat.doc_id
                    for elem in not_query_result
                    for stat in elem.statistics
                ]
            )

    else:

        if intersection_columns:
            intersection_result = intersection_query(
                intersection_columns,
                input_data
            )

            if not intersection_result:
                return ArticleQueryResult(
                    query=query_input,
                    data=[]
                )

            result_ids.update(intersection_result)

            ranged_value = calculate_ranged_value(
                intersection_columns,
                result_ids,
                input_data
            )

            # cosinus_value = calculate_cosinus_value(
            # intersection_columns,
            # result_ids,
            # input_data
            # )

            cosinus_value = calculate_cosinus_value_for_lsi(
                intersection_columns,
                result_ids,
                input_data,
                input_data
            )

        else:
            return ArticleQueryResult(
                query=query_input,
                data=[]
            )

    raw_data = load_raw_data(search_file_path, result_ids)

    return ArticleQueryResult(
        query=query_input,
        data=raw_data,
        ranged_value=ranged_value,
        cosinus_value=cosinus_value
    )


if __name__ == '__main__':
    queries = [
        'гнойный го горе',
        '-голова голос голосовой',
        'пункт становиться праздник',
        '-такой -таков сэмпл локация',
        'внешне внешний самый уверять уметь',
        'вообще идея низкий плохо покупать',
    ]

    file_path = Path(__file__).parent.parent / Path('crawler/article_results.xml')

    articles_data = load_articles_data(str(file_path))

    search_results = [
        asdict(
            process_query(
                file_path,
                elem,
                articles_data
            )
        )
        for elem in queries
    ]

    vectors = [
        asdict(
            ArticleVectorResult(
                query=item['query'],
                url=item['data'][0]['url'],
                cosinus_value=item['cosinus_value']
            ) if item['data'] else
            ArticleVectorResult(
                query=item['query'],
                url='',
                cosinus_value=0.0
            )
        )
        for item in search_results
    ]

    vectors.sort(
        reverse=True,
        key=lambda item: item['cosinus_value']
    )

    with open('search_results_lsi.json', 'w', encoding='utf8') as json_fp:
        json.dump(
            {
                'results': vectors
            },
            json_fp,
            indent=4,
            ensure_ascii=False
        )
