import asyncio
from typing import Iterable, List

import aiohttp

import utility


BASE_URL = 'http://127.0.0.1:9200/'

async def add_document(index_: str, body: dict, session: aiohttp.ClientSession):
    url = f'{BASE_URL}{index_}/_doc'
    await session.post(url, json=body)


async def get_document_by_id(index_: str, id_: str, session: aiohttp.ClientSession) -> aiohttp.ClientResponse:
    url = f'{BASE_URL}{index_}/_doc/{id_}'
    response = await session.get(url)
    return response

async def get_documents_by_id(index_: str, ids: Iterable[str]) -> List[dict]:
    tasks = []
    async with aiohttp.ClientSession() as session:
        for id_ in ids:
            task = asyncio.create_task(get_document_by_id(index_, id_, session))
            tasks.append(task)
        docs = await asyncio.gather(*tasks)
    return [await doc.json() for doc in docs]

def run_get_documents_by_id(index_: str, ids: Iterable[str]) -> List[dict]:
    return asyncio.run(get_documents_by_id(index_, ids))


async def delete_document_by_id(index_: str, id_: str, session: aiohttp.ClientSession):
    url = f'{BASE_URL}{index_}/{id_}'
    with session.delete(url) as response:
        await response.read()

async def add_documents_to_schema(index_: str, bodies: Iterable[dict]):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for body in bodies:
            task = asyncio.create_task(
                add_document(index_, body, session)
            )
            tasks.append(task)
        await asyncio.gather(*tasks)

def run_add_documents_to_schema(index_: str, bodies: Iterable[dict]):
    asyncio.run(add_documents_to_schema(index_, bodies))