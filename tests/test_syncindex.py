import unittest
import time

import syncindex


class SyncIndexTestCase(unittest.TestCase):
    def test_connection(self):
        r = syncindex.get_base_page()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['cluster_name'], 'elasticsearch')

    def test_create_index(self):
        syncindex.create_index('index1')
        self.assertEqual(syncindex.get_index('index1').status_code, 200)
        syncindex.delete_index('index1')

    def test_delete_index(self):
        syncindex.create_index('index2')
        self.assertEqual(syncindex.get_index('index2').status_code, 200)
        syncindex.delete_index('index2')
        self.assertEqual(syncindex.get_index('index2').status_code, 404)

    def test_add_document(self):
        r = syncindex.add_document("index3", {"name": "John"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(syncindex.get_document_by_id("index3", r.json()["_id"]).status_code, 200)
        syncindex.delete_index("index3")

    def test_search_document(self):
        added_doc = syncindex.add_document("index4", {
            "name": "Jack"
        })
        added_doc_id = added_doc.json()['_id']
        time.sleep(4)
        search_res = syncindex.search_document("index4", "name", "Jack")
        self.assertIn(added_doc_id, [hit['_id'] for hit in search_res.json()['hits']['hits']])
        syncindex.delete_index("index4")

    def test_delete_document_by_id(self):
        added_doc = syncindex.add_document("index5", {
            "name": "Jack"
        })
        added_doc_id = added_doc.json()['_id']
        syncindex.delete_index("index5")
        self.assertEqual(404, syncindex.get_document_by_id("index5", added_doc_id).status_code)
