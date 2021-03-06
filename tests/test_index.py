from time import sleep
import unittest

import syncindex
import index

class IndexTestCase(unittest.TestCase):
    def test_run_add_documents_to_schema(self):
        bodies = [{'name': f'Jason #{i}'} for i in range(531)]
        index.run_add_documents_to_schema('index1', bodies)
        sleep(5)
        self.assertEqual(531, syncindex.index_counter('index1'))
        syncindex.delete_index('index1')

    def test_run_get_documents_by_id(self):
        bodies = [{'name': f'Jason #{i}'} for i in range(5)]
        ids = []
        for body in bodies:
            ids.append(syncindex.add_document('index1', body).json()['_id'])
        sleep(2)
        self.assertEqual(5, len(index.run_get_documents_by_id('index1', ids)))