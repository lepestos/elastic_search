import asyncio
import csv
from typing import Dict, Iterable, List
from requests.models import Response

import aiohttp

import index
import utility
import syncindex


PROPERTIES = (
    ('text', 'text'),
    ('created_date', 'date'),
    ('rubrics', 'text')
)


async def add_text_document(text: str, created_date: str, rubrics: str,
                            session, index_='search'):
    body = {'text': text, 'created_date': created_date, 'rubrics': rubrics}
    await index.add_document(index_, body, session)


async def add_text_documents(texts: Iterable[str], created_dates: Iterable[str],
                             rubrics: Iterable[List[str]], index_: str ='search'):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for t, d, r in zip(texts, created_dates, rubrics):
            task = asyncio.create_task(add_text_document(t, d, r, session, index_))
            tasks.append(task)
        await asyncio.gather(*tasks)


def run_add_text_documents(texts: Iterable[str], created_dates: Iterable[str],
                           rubrics: Iterable[List[str]], index_: str ='search'):
    asyncio.run(add_text_documents(texts, created_dates, rubrics, index_))


def add_csv_file(file: str, index_='search'):
    with open(file, 'r') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)
        if index_ not in syncindex.list_all_indices():
            syncindex.create_index(index_, PROPERTIES)
        texts, created_dates, rubrics = [], [], []
        next(reader)
        for t, d, r in reader:
            texts.append(t)
            created_dates.append(utility.date_to_el_format(d))
            rubrics.append(r)
    run_add_text_documents(texts, created_dates, rubrics, index_)


def search_document(text: str, index_: str ='search'):
    response = syncindex.search_document(index_, 'text', text, 'created_date')
    return list_documents_in_response(response, index_)


def list_all_documents(index_: str = 'search') -> List[Dict]:
    response = syncindex.list_documents(index_)
    return list_documents_in_response(response, index_)


def list_documents_in_response(response: Response, index_: str) -> List[Dict]:
    ids = [hit['_id'] for hit in response.json()['hits']['hits']]
    docs = index.run_get_documents_by_id(index_, ids)
    res = []
    for id_, doc in zip(ids, docs):
        res.append({
            'id_': id_,
            'text': doc['_source']['text'],
            'created_date': doc['_source']['created_date'],
            'rubrics': doc['_source']['created_date']
        })
    return res
