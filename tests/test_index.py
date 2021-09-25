import unittest
import time

import index


class IndexTestCase(unittest.TestCase):
    def test_connection(self):
        r = index.get_base_page()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['cluster_name'], 'elasticsearch')

    def test_create_index(self):
        index.create_index('index1')
        self.assertEqual(index.get_index('index1').status_code, 200)
        index.delete_index('index1')

    def test_delete_index(self):
        index.create_index('index2')
        self.assertEqual(index.get_index('index2').status_code, 200)
        index.delete_index('index2')
        self.assertEqual(index.get_index('index2').status_code, 404)

    def test_add_document(self):
        r = index.add_document("index3", "schema4", {"name": "John"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(index.get_document_by_id("index3", "schema4", r.json()["_id"]).status_code, 200)
        index.delete_index("index3")

    def test_search_document(self):
        added_doc = index.add_document("index4", "schema4", {"name": "Jack"})
        added_doc_id = added_doc.json()['_id']
        time.sleep(4)
        search_res = index.search_document("index4", "schema4", "name", "Jack")
        self.assertIn(added_doc_id, [hit['_id'] for hit in search_res.json()['hits']['hits']])
        index.delete_index("index4")

    def test_delete_document_by_id(self):
        added_doc = index.add_document("index5", "schema5", {"name": "Jack"})
        added_doc_id = added_doc.json()['_id']
        index.delete_index("index5")
        self.assertEqual(404, index.get_document_by_id("index5", "schema5", added_doc_id).status_code)
