import unittest
import time

import index
import search
import async_search

class AsyncSearchTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        index.delete_index('index1')

    def test_run_add_text_documents(self):
        async_search.run_add_text_documents(
            ['Was ist hier los'], ['2019-07-25 12:42:13'], [['rubric1', 'rubric2', 'rubric3']], 'index1'
        )
        time.sleep(2)
        self.assertEqual(1, index.index_counter('index1'))
        async_search.run_add_text_documents(
            ['Ist das normal'], ['2019-07-25 12:42:13'], [['rubric1', 'rubric5', 'rubric3']], 'index1'
        )
        time.sleep(2)
        self.assertEqual(2, index.index_counter('index1'))
        index.delete_index('index1')

    def test_add_csv_file(self):
        for i in range(1,6):
            with open('test_posts.csv', 'r') as f:
                async_search.add_csv_file(f, 'index1')
            time.sleep(3)
            self.assertEqual(2 * i, index.index_counter('index1'))
        index.delete_index('index1')

    def test_search_document(self):
        search.add_text_document('Was ist hier los', '2019-07-25 12:42:13', ['rubric1', 'rubric2', 'rubric3'], 'index1')
        time.sleep(2)
        self.assertEqual(1, len(async_search.search_document('Was ist hier los', 'index1')))
        search.add_text_document('Was ist hier los', '2019-07-25 12:42:13', ['rubric1', 'rubric2', 'rubric3'], 'index1')
        time.sleep(2)
        self.assertEqual(2, len(async_search.search_document('Was ist hier los', 'index1')))
        index.delete_index('index1')