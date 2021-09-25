import requests

import utility


BASE_URL = 'http://127.0.0.1:9200/'


def get_base_page():
    return requests.get(BASE_URL)

def get_index(index_name):
    return requests.get(BASE_URL + index_name)

def create_index(index_name):
    return requests.put(BASE_URL + index_name)

def delete_index(index_name):
    return requests.delete(BASE_URL + index_name)

def delete_all_indices():
    for ind in list_all_indices():
        delete_index(ind)

def add_document(index, schema, body):
    return requests.post(f'{BASE_URL}{index}/{schema}', json=body)

def get_document_by_id(index, schema, id_):
    return requests.get(f'{BASE_URL}{index}/{schema}/{id_}')

def list_all_indices():
    r = requests.get(BASE_URL + '_aliases')
    return list(r.json().keys())

def search_document(index, schema, field, content):
    body = utility.build_query(field, content)
    return requests.get(f'{BASE_URL}{index}/{schema}/_search?size=500', json=body)

def delete_document_by_id(index, schema, id_):
    return requests.delete(f'{BASE_URL}{index}/{schema}/{id_}')

def index_counter(index):
    return requests.get(f'{BASE_URL}{index}/_count').json()['count']