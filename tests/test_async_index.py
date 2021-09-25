from time import sleep
import unittest

import index
import async_index

class AsyncIndexTestCase(unittest.TestCase):
    def test_run_add_documents_to_schema(self):
        bodies = [{'name': f'Jason #{i}'} for i in range(531)]
        async_index.run_add_documents_to_schema('index1', bodies)
        sleep(5)
        self.assertEqual(531, index.index_counter('index1'))
        index.delete_index('index1')

    def test_run_get_documents_by_id(self):
        bodies = [{'name': f'Jason #{i}'} for i in range(5)]
        ids = []
        for body in bodies:
            ids.append(index.add_document('index1', body).json()['_id'])
        sleep(2)
        self.assertEqual(5, len(async_index.run_get_documents_by_id('index1', ids)))