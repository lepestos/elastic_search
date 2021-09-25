import unittest
import time

import syncindex
import syncsearch
import search

class SearchTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        syncindex.delete_index('index1')

    def test_run_add_text_documents(self):
        search.run_add_text_documents(
            ['Was ist hier los'], ['2019-07-25 12:42:13'], [['rubric1', 'rubric2', 'rubric3']], 'index1'
        )
        time.sleep(2)
        self.assertEqual(1, syncindex.index_counter('index1'))
        search.run_add_text_documents(
            ['Ist das normal'], ['2019-07-25 12:42:13'], [['rubric1', 'rubric5', 'rubric3']], 'index1'
        )
        time.sleep(2)
        self.assertEqual(2, syncindex.index_counter('index1'))
        syncindex.delete_index('index1')

    def test_add_csv_file(self):
        for i in range(1,6):
            with open('test_posts.csv', 'r') as f:
                search.add_csv_file(f, 'index1')
            time.sleep(3)
            self.assertEqual(2 * i, syncindex.index_counter('index1'))
        syncindex.delete_index('index1')

    def test_search_document(self):
        syncsearch.add_text_document('Was ist hier los', '2019-07-25 12:42:13', ['rubric1', 'rubric2', 'rubric3'], 'index1')
        time.sleep(2)
        self.assertEqual(1, len(search.search_document('Was ist hier los', 'index1')))
        syncsearch.add_text_document('Was ist hier los', '2019-07-25 12:42:13', ['rubric1', 'rubric2', 'rubric3'], 'index1')
        time.sleep(2)
        self.assertEqual(2, len(search.search_document('Was ist hier los', 'index1')))
        syncindex.delete_index('index1')