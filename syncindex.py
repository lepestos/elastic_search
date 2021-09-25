import requests
from typing import Dict, Iterable, List, Optional, Tuple

import utility


BASE_URL = 'http://127.0.0.1:9200/'


def get_base_page() -> requests.models.Response:
    return requests.get(BASE_URL)

def get_index(index_name: str) -> requests.models.Response:
    return requests.get(BASE_URL + index_name)

def create_index(index_name: str, properties: Optional[Iterable[Tuple]]=None) -> requests.models.Response:
    settings = None
    if properties is not None:
        settings = utility.build_settings(properties)
    return requests.put(BASE_URL + index_name, json=settings)

def delete_index(index_name: str) -> requests.models.Response:
    return requests.delete(BASE_URL + index_name)

def delete_all_indices():
    for ind in list_all_indices():
        delete_index(ind)

def add_document(index: str, body: Dict)  -> requests.models.Response:
    return requests.post(f'{BASE_URL}{index}/_doc', json=body)

def get_document_by_id(index: str, id_: str) -> requests.models.Response:
    return requests.get(f'{BASE_URL}{index}/_doc/{id_}')

def list_all_indices() -> List[str]:
    r = requests.get(BASE_URL + '_aliases')
    return list(r.json().keys())

def search_document(index: str, field: str, content: str) -> requests.models.Response:
    body = utility.build_query(field, content)
    return requests.get(f'{BASE_URL}{index}/_search?size=500', json=body)

def delete_document_by_id(index: str, id_: str) -> requests.models.Response:
    return requests.delete(f'{BASE_URL}{index}/{id_}')

def index_counter(index: str) -> int:
    return requests.get(f'{BASE_URL}{index}/_count').json()['count']