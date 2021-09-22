import index
import csv

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
        ids.append(add_text_document(text, created_date, rubrics))
    return tuple(ids)
