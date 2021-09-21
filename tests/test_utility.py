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
