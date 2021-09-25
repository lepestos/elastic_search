import csv
from typing import Dict, Iterable, TextIO, Tuple, List

import syncindex
import utility

def add_text_document(text: str, created_date: str, rubrics: str, index_: str ='search') -> str:
    body = {
        'text': text,
        'created_date': utility.date_to_el_format(created_date),
        'rubrics': rubrics
    }
    r = syncindex.add_document(index_, body)
    return r.json()['_id']

def add_multiple_text_documents(docs: Iterable[Tuple[str]], index_: str ='search') -> Tuple[str]:
    ids = []
    for text, created_date, rubrics in docs:
        ids.append(add_text_document(text, created_date, rubrics, index_))
    return tuple(ids)

def add_csv_file(file: TextIO) -> Tuple[str]:
    reader = csv.reader(file, quotechar='"', delimiter=',',
                        quoting=csv.QUOTE_ALL, skipinitialspace=True)
    next(reader)
    ids = []
    for text, created_date, rubrics in reader:
        ids.append(add_text_document(text, created_date, rubrics))
    return tuple(ids)

def search_document(text: str) -> List[Dict]:
    response = syncindex.search_document('search', 'text', text)
    ids = [hit['_id'] for hit in response.json()['hits']['hits']]
    res = []
    for id_ in ids:
        doc = syncindex.get_document_by_id('search', id_)
        res.append({
            'id_': id_,
            'text': doc.json()['_source']['text'],
            'created_date': doc.json()['_source']['created_date'],
            'rubrics': doc.json()['_source']['created_date']
        })
    return res

