import csv

import index
import utility

def add_text_document(text, created_date, rubrics):
    body = {'text': text, 'created_date': created_date, 'rubrics': rubrics}
    r = index.add_document("search", "documents", body)
    return r.json()['_id']

def add_multiple_text_documents(docs):
    ids = []
    for text, created_date, rubrics in docs:
        ids.append(add_text_document(text, created_date, rubrics))
    return tuple(ids)

def add_csv_file(file):
    reader = csv.reader(file, quotechar='"', delimiter=',',
                        quoting=csv.QUOTE_ALL, skipinitialspace=True)
    next(reader)
    ids = []
    for text, created_date, rubrics in reader:
        ids.append(add_text_document(
            text, utility.date_to_el_format(created_date), rubrics
        ))
    return tuple(ids)

def search_document(text):
    response = index.search_document('search', 'documents', 'text', text)
    ids = [hit['_id'] for hit in response.json()['hits']['hits']]
    res = []
    for id_ in ids:
        doc = index.get_document_by_id('search', 'documents', id_)
        res.append({
            'id_': id_,
            'text': doc.json()['_source']['text'],
            'created_date': doc.json()['_source']['created_date'],
            'rubrics': doc.json()['_source']['created_date']
        })
    return res

