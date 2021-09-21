from elasticsearch import Elasticsearch
import utility

HOST = 'localhost'
PORT = 9200


def connect_elasticsearch():
    es = Elasticsearch([{'host': HOST, 'port': PORT}])
    if not es.ping():
        raise RuntimeError(f"Couldn't connect to {HOST}:{PORT}")
    print(f'Successfully connected to {HOST}:{PORT}')
    return es


def create_index(es_object, index_name, props):
    settings = utility.build_settings(props)

    try:
        if es_object.indices.exists(index_name):
            es_object.indices.delete(index_name)
        es_object.indices.create(index=index_name, ignore=400, body=settings)
    except Exception as ex:
        print(str(ex))

if __name__ == '__main__':
    es = connect_elasticsearch()
    for index in es.indices.get('*'):
        print(index, type(index))