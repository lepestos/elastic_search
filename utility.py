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


def build_settings(pairs):
    settings = DEF_SETTINGS.copy()
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