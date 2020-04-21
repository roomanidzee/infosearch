import copy
import math
from functools import reduce
from typing import Dict, List

from project.server.inverted_index.index.building import INDEX_TABLE_TYPE
from project.server.inverted_index.index.dto import WordInformation


def map_index_table(input_data: INDEX_TABLE_TYPE) -> List[WordInformation]:
    """Mapping index tree data to object representation."""

    return [
        WordInformation(
            value=key,
            statistics=value
        )
        for key, value in input_data.items()
    ]


def calculate_tf_idf(
    words_count: Dict[int, int],
    input_data: List[WordInformation]
) -> List[WordInformation]:
    """Calculate tf-idf for each word information."""

    data_for_change = copy.deepcopy(input_data)
    doc_collection_size = len(list(words_count.keys()))

    for elem in data_for_change:

        doc_count = reduce(
            lambda count, item: count + (item.count_value != 0),
            elem.statistics,
            0
        )

        for info in elem.statistics:

            if info.count_value != 0:
                tf = info.count_value / words_count.get(info.doc_id)

                idf = math.log(doc_collection_size / doc_count)

                info.tf_idf_value = round(tf * idf, 4)

    return data_for_change


def sort_mapped_data(input_data: List[WordInformation]) -> List[WordInformation]:
    """Sort result set of data by word value and document id."""

    for elem in input_data:
        elem.statistics = sorted(elem.statistics, key=lambda item: item.doc_id)

    return sorted(input_data, key=lambda item: item.value)
