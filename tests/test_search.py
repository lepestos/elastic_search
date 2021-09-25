import unittest
import time

import index
import search

class SearchCase(unittest.TestCase):
    def test_add_text_document(self):
        id_ = search.add_text_document('Was ist hier los', '2019-07-25 12:42:13', ['rubric1', 'rubric2', 'rubric3'])
        time.sleep(2)
        self.assertEqual(200, index.get_document_by_id('search', 'documents', id_).status_code)
        index.delete_document_by_id('search', 'documents', id_)

    def test_add_multiple_text_documents(self):
        bodies = [
            ('AAA', '2019-03-25 12:40:13', ['r1', 'r2']),
            ('BBB', '2019-04-22 13:45:10', ['r2', 'r3'])
        ]
        ids = search.add_multiple_text_documents(bodies)
        time.sleep(2)
        for id_ in ids:
            self.assertEqual(200, index.get_document_by_id('search', 'documents', id_).status_code)
        for id_ in ids:
            index.delete_document_by_id('search', 'documents', id_)

    def test_add_csv_file(self):
        with open('test_posts.csv', 'r') as f:
            ids = search.add_csv_file(f)
        time.sleep(2)
        for id_ in ids:
            self.assertEqual(200, index.get_document_by_id('search', 'documents', id_).status_code)
        for id_ in ids:
            index.delete_document_by_id('search', 'documents', id_)

    def test_search_document(self):
        id_ = search.add_text_document('Was ist hier los', '2019-07-25 12:42:13', ['rubric1', 'rubric2', 'rubric3'])
        self.assertEqual(200, index.get_document_by_id('search', 'documents', id_).status_code)
        time.sleep(3)
        query_result = search.search_document('Was ist hier los')
        query_ids = [document['id_'] for document in query_result]
        self.assertIn(id_, query_ids)
        index.delete_document_by_id('search', 'documents', id_)

