
import math
from typing import List, Set

import numpy as np

from project.server.inverted_index.index.dto import WordInformation
from project.server.boolean_search.parser.data.load_data import (
    convert_to_matrix,
    create_svd,
)


def not_query(
    column: str,
    input_data: List[WordInformation]
) -> List[WordInformation]:
    """Search words by 'not' query type"""

    word_info = next(
        (
            elem
            for elem in input_data
            if elem.value == column
        ),
        None
    )

    if not word_info:
        return []

    doc_ids = {
        stat.doc_id
        for stat in word_info.statistics
        if stat.count_value != 0
    }

    return [
        elem
        for elem in input_data
        if any(stat.doc_id not in doc_ids for stat in elem.statistics)
    ]


def get_document_ids(input_data: WordInformation) -> Set[int]:
    """Get document ids from word info."""
    return {elem.doc_id for elem in input_data.statistics if elem.count_value != 0}


def intersection_query(
    columns: List[str],
    input_data: List[WordInformation]
) -> List[int]:
    """Search words by intersection query type."""

    filtered_data = [
        elem
        for elem in input_data
        if elem.value in columns
    ]

    if not filtered_data:
        return list()

    sorted_data = sorted(
        filtered_data,
        key=lambda x: sum(
            elem.count_value
            for elem in x.statistics
        )
    )

    first_elem = get_document_ids(sorted_data[0])
    second_elem = get_document_ids(sorted_data[1])

    result = first_elem.intersection(second_elem)

    if len(sorted_data) == 2:
        return list(result)

    if not result:
        return list()

    for i in range(2, len(sorted_data)):

        elements = get_document_ids(sorted_data[i])

        intersection_result = result.intersection(elements)

        if not intersection_result:
            return list()

        result.update(intersection_result)

    return list(result)


def calculate_ranged_value(
    columns: List[str],
    doc_ids: Set[int],
    input_data: List[WordInformation]
) -> float:
    """Calculate ranged index value for search results."""

    filter_by_columns = [
        elem
        for elem in input_data
        if elem.value in columns
    ]

    documents_for_calculation = [
        attr
        for elem in filter_by_columns
        for attr in elem.statistics
        if attr.doc_id in doc_ids
    ]

    return sum(elem.tf_idf_value for elem in documents_for_calculation)


def vector_calc(
    input_val: float
) -> float:
    return math.pow(input_val, 2) + math.pow(input_val, 2)


def matrix_calc(
    input_val: np.ndarray
) -> float:
    return math.sqrt(
        np.power(
            input_val, 2
        ).sum()
    )



def calculate_cosinus_value(
    columns: List[str],
    doc_ids: Set[int],
    input_data: List[WordInformation]
) -> float:
    """Calculate vector model for search results."""

    filter_by_columns = [
        elem
        for elem in input_data
        if elem.value in columns
    ]

    documents_for_calculation = [
        attr
        for elem in filter_by_columns
        for attr in elem.statistics
        if attr.doc_id in doc_ids
    ]

    first_elem = sum(elem.tf_idf_value for elem in documents_for_calculation)

    vector_result = math.sqrt(
        sum(
            vector_calc(elem.tf_idf_value)
            for elem in documents_for_calculation
        )
    )

    second_elem = vector_result * math.sqrt(len(columns))

    return first_elem / second_elem


def calculate_cosinus_value_for_lsi(
    columns: List[str],
    doc_ids: Set[int],
    input_data: List[WordInformation],
    full_data: List[WordInformation]
) -> float:
    """Calculate vector model for search results by lsi method."""

    k = 4

    documents_matrix = np.array(convert_to_matrix(input_data)).transpose()

    filter_by_columns = [
        elem
        for elem in input_data
        if elem.value in columns
    ]

    documents_for_calculation = [
        elem
        for elem in filter_by_columns
        for attr in elem.statistics
        if attr.doc_id in doc_ids
    ]

    query_matrix = np.array(convert_to_matrix(documents_for_calculation)).transpose()

    full_matrix = convert_to_matrix(full_data)

    U, V, S = create_svd(full_matrix)

    U_changed = U[:, :k]
    S_changed = np.linalg.inv(S[0:k, 0:k])

    qm_shape = (
        query_matrix.shape[0],
        query_matrix.shape[1]
    )

    dm_shape = (
        documents_matrix.shape[0],
        documents_matrix.shape[1]
    )

    # only by this operations - ranged values

    if qm_shape[1] > U_changed.shape[1]:
        query_matrix = query_matrix[:, 0:U_changed.shape[1]]

    query_result = query_matrix * U_changed[0:qm_shape[0], 0:qm_shape[1]]
    query_final_result = query_result[np.nonzero(query_result)]

    doc_result = documents_matrix[:, 0:U_changed.shape[1]] * U_changed[0:dm_shape[0], :]
    doc_final_result = doc_result[np.nonzero(doc_result)]

    first_matrix = query_final_result[0:S_changed.shape[0]:, np.newaxis] * S_changed[0:query_final_result.shape[0], :]
    second_matrix = doc_final_result[:, np.newaxis] * S_changed

    first_elem = np.sum(first_matrix * second_matrix[0:query_final_result.shape[0], :])

    second_elem = math.sqrt(
        len(columns)
    ) * matrix_calc(first_matrix) * matrix_calc(second_matrix)

    return abs(first_elem) / abs(second_elem)
