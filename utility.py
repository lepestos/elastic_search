from copy import deepcopy


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


def build_settings(pairs):
    settings = deepcopy(DEF_SETTINGS)
    settings["mappings"]["properties"] = pairs_to_el_format(pairs)
    return settings


def pairs_to_el_format(pairs):
    # converts list of (property, type) into ES readable format
    res = {}
    for property_, type_ in pairs:
        res[property_] = {
            'type': type_
        }
    return res


def build_query(field, content):
    res = deepcopy(DEF_QUERY)
    res["query"]["match"][field] = {}
    res["query"]["match"][field]["query"] = content
    res["query"]["match"][field]["operator"] = "and"
    return res.copy()

def date_to_el_format(date_str):
    date_, time_ = date_str.split()
    return f'{date_}T{time_}+00:00'