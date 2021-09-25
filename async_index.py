import asyncio

import aiohttp

import utility


BASE_URL = 'http://127.0.0.1:9200/'

async def add_document(index, schema, body, session):
    url = f'{BASE_URL}{index}/{schema}'
    await session.post(url, json=body)


async def get_document_by_id(index, schema, id_, session):
    url = f'{BASE_URL}{index}/{schema}/{id_}'
    response = await session.get(url)
    return response

async def get_documents_by_id(index, schema, ids):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for id_ in ids:
            task = asyncio.create_task(get_document_by_id(index, schema, id_, session))
            tasks.append(task)
        docs = await asyncio.gather(*tasks)
    return [await doc.json() for doc in docs]

def run_get_documents_by_id(index, schema, ids):
    return asyncio.run(get_documents_by_id(index, schema, ids))

async def search_document(index, schema, field, content, session):
    body = utility.build_query(field, content)
    url = f'{BASE_URL}{index}/{schema}/_search?size=500'
    response = session.get(url, json=body)
    return response

async def delete_document_by_id(index, schema, id_, session):
    url = f'{BASE_URL}{index}/{schema}/{id_}'
    with session.delete(url) as response:
        await response.read()
        return response

async def add_documents_to_schema(index, schema, bodies):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for body in bodies:
            task = asyncio.create_task(
                add_document(index, schema, body, session)
            )
            tasks.append(task)
        await asyncio.gather(*tasks)

def run_add_documents_to_schema(index, schema, bodies):
    asyncio.run(add_documents_to_schema(index, schema, bodies))