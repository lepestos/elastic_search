from copy import deepcopy
from datetime import datetime
from typing import Dict, Iterable, Tuple, Optional

DEF_SETTINGS = {
    "settings": {
        "analysis": {
            "filter": {
                "ru_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "ru_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "default": {
                    "char_filter": [
                        "html_strip"
                    ],
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "ru_stop",
                        "ru_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {}
    }
}

DEF_QUERY = {
    "_source": False,
    "query": {
        "match": {
        }
    }
}


def build_settings(pairs: Iterable[Tuple]) -> Dict:
    settings = deepcopy(DEF_SETTINGS)
    settings["mappings"]["properties"] = pairs_to_el_format(pairs)
    return settings


def pairs_to_el_format(pairs: Iterable[Tuple]) -> Dict:
    # converts list of (property, type) into ES readable format
    res = {}
    for property_, type_ in pairs:
        res[property_] = {
            'type': type_
        }
    return res


def build_query(field: str, content: str, sort_by: Optional[str] = None) -> Dict:
    res = deepcopy(DEF_QUERY)
    res["query"]["match"][field] = {}
    res["query"]["match"][field]["query"] = content
    res["query"]["match"][field]["operator"] = "and"
    if sort_by is not None:
        res["sort"] = [{sort_by: {"order": "desc"}}]
    return res.copy()


def date_to_el_format(date_str: str) -> str:
    date_, time_ = date_str.split()
    return f'{date_}T{time_}+00:00'


def to_seconds(el_time: str) -> int:
    date, time = el_time.split('T')
    time = time.split('+')[0]
    d = datetime(*[int(s) for s in date.split('-')],
                 *[int(s) for s in time.split(':')])
    d0 = datetime(1970, 1, 1)
    return int((d-d0).total_seconds())