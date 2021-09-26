import unittest
import time

import syncindex
import syncsearch
import search
import utility

class SearchTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
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

    def test_add_csv_file(self):
        for i in range(1,6):
            search.add_csv_file('test_posts.csv', 'index1')
            time.sleep(3)
            self.assertEqual(2 * i, syncindex.index_counter('index1'))

    def test_search_document(self):
        syncsearch.add_text_document('Was ist hier los', '2019-07-25 12:42:13',
                                     ['rubric1', 'rubric2', 'rubric3'], 'index1')
        time.sleep(2)
        self.assertEqual(1, len(search.search_document('Was ist hier los', 'index1')))
        syncsearch.add_text_document('Was ist hier los', '2019-07-25 12:42:13',
                                     ['rubric1', 'rubric2', 'rubric3'], 'index1')
        time.sleep(2)
        self.assertEqual(2, len(search.search_document('Was ist hier los', 'index1')))

    def test_list_all_documents(self):
        texts = ['Was ist hier los', 'Was ist passiert', 'Was ist hier los', 'Ist das normal']
        for text in texts:
            syncsearch.add_text_document(text , '2019-07-25 12:42:13',
                                         ['rubric1', 'rubric2', 'rubric3'], 'index1')
        time.sleep(2)
        docs = search.list_all_documents('index1')
        self.assertEqual(4, len(docs))
        self.assertSetEqual(set(texts), {doc['text'] for doc in docs})

class PostsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        syncindex.delete_index('index1')
        search.add_csv_file('posts.csv', 'index1')
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        syncindex.delete_index('index1')

    def test_index_created(self):
        self.assertIn('index1', syncindex.list_all_indices())

    def test_loaded_all_data(self):
        self.assertEqual(1500, len(search.list_all_documents('index1')))

    def test_search(self):
        self.assertEqual(3, len(search.search_document('hi', 'index1')))
        self.assertEqual(19, len(search.search_document('поступают', 'index1')))
        self.assertEqual(20, len(search.search_document('председатель', 'index1')))
        self.assertEqual(7, len(search.search_document('любовь и голуби', 'index1')))

    def test_chronological_order(self):
        res = search.search_document('председатель', 'index1')
        for prev, nxt in zip(res, res[1:]):
            self.assertGreaterEqual(utility.to_seconds(prev['created_date']),
                                    utility.to_seconds(nxt['created_date']))
