import unittest
import utility


class UtilityTestCase(unittest.TestCase):
    def test_pairs_to_el_format(self):
        res = utility.pairs_to_el_format([('property', 'type')])
        expected = {
            'property': {
                'type': 'type'
            }
        }
        self.assertEqual(res, expected)
        res = utility.pairs_to_el_format([('property1', 'type1'), ('property2', 'type2')])
        expected = {
            'property1': {
                'type': 'type1'
            },
            'property2': {
                'type': 'type2'
            }
        }
        self.assertEqual(res, expected)


    def test_build_settings(self):
        res = utility.build_settings([('age', 'integer')])
        expected = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "age": {
                        "type": "integer"
                    },
                }
            }
        }
        self.assertEqual(res, expected)

        res = utility.build_settings([('age', 'integer'), ('name', 'text')])
        expected = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "age": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "text"
                    },
                }
            }
        }
        self.assertEqual(res, expected)

    def test_build_query(self):
        expected = {
            "_source": False,
            "query": {
                "match": {
                    "text": "jewelry"
                }
            }
        }
        res = utility.build_query("text", "jewelry")
        self.assertEqual(expected, res)

        expected = {
            "_source": False,
            "query": {
                "match": {
                    "name": "John"
                }
            }
        }
        res = utility.build_query("name", "John")
        self.assertEqual(expected, res)

    def test_date_to_el_format(self):
        expected = ['2021-22-08T17:18:42+00:00', '2019-02-08T07:18:02+00:00']
        res = [utility.date_to_el_format(ds) for ds in ['2021-22-08 17:18:42', '2019-02-08 07:18:02']]
        for r, e in zip(res, expected):
            self.assertEqual(e, r)