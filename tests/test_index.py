import unittest
import search


class SearchTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.es = search.connect_elasticsearch()
        for index in cls.es.indices.get('*'):
            cls.es.indices.delete(index)

    @classmethod
    def tearDownClass(cls):
        cls.es.transport.close()

    def test_connection(self):
        self.assertIsNotNone(self.es)

    def test_create_index(self):
        search.create_index(self.es, 'new_index', [("age", "integer")])
        self.es.indices.get('new_index')


if __name__ == '__main__':
    unittest.main()
