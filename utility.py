import json
from copy import deepcopy


DEF_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
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
    res["query"]["match"][field] = content
    return res.copy()
