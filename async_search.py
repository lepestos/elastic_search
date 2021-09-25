import asyncio
import csv

import aiohttp

import async_index
import utility
import index


PROPERTIES = (
    ('text', 'text'),
    ('created_date', 'date'),
    ('rubrics', 'text')
)


async def add_text_document(text, created_date, rubrics,
                            session, index_='search'):
    body = {'text': text, 'created_date': created_date, 'rubrics': rubrics}
    await async_index.add_document(index_, body, session)


async def add_text_documents(texts, created_dates, rubrics, index_='search'):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for t, d, r in zip(texts, created_dates, rubrics):
            task = asyncio.create_task(add_text_document(t, d, r, session, index_))
            tasks.append(task)
        await asyncio.gather(*tasks)


def run_add_text_documents(texts, created_dates, rubrics, index='search'):
    asyncio.run(add_text_documents(texts, created_dates, rubrics, index))


def add_csv_file(file, index_='search'):
    reader = csv.reader(file, quotechar='"', delimiter=',',
                        quoting=csv.QUOTE_ALL, skipinitialspace=True)
    if index_ not in index.list_all_indices():
        index.create_index(index_, PROPERTIES)
    texts, created_dates, rubrics = [], [], []
    next(reader)
    for t, d, r in reader:
        texts.append(t)
        created_dates.append(utility.date_to_el_format(d))
        rubrics.append(r)
    run_add_text_documents(texts, created_dates, rubrics, index_)


def search_document(text, index_='search'):
    response = index.search_document(index_, 'text', text)
    ids = [hit['_id'] for hit in response.json()['hits']['hits']]
    tasks = []
    docs = async_index.run_get_documents_by_id(index_, ids)
    res = []
    for id_, doc in zip(ids, docs):
        res.append({
            'id_': id_,
            'text': doc['_source']['text'],
            'created_date': doc['_source']['created_date'],
            'rubrics': doc['_source']['created_date']
        })
    return res



