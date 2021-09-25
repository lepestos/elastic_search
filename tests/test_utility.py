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
        expected = {
            "settings": {
                "analysis": {
                    "filter": {
                        "ru_stop": {
                            "type": "stop",
                            "stopwords": "_russian_"
                        },
                        "ru_stemmer": {
                            "type": "stemmer",
                            "language": "russian"
                        }
                    },
                    "analyzer": {
                        "default": {
                            "char_filter": [
                                "html_strip"
                            ],
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "ru_stop",
                                "ru_stemmer"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                    "properties": {
                        "age": {
                            "type": "integer"
                        },
                    }
            }
        }
        res = utility.build_settings([('age', 'integer')])
        self.assertEqual(expected, res)

    def test_build_query(self):
        expected = {
            "_source": False,
            "query": {
                "match": {
                    "text": {
                        "query": "jewelry",
                        "operator": "and"
                    }
                }
            }
        }
        res = utility.build_query("text", "jewelry")
        self.assertEqual(expected, res)

        expected = {
            "_source": False,
            "query": {
                "match": {
                    "name": {
                        "query": "John",
                        "operator": "and"
                    }
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

    def test_to_seconds(self):
        dates = ['2000-01-01T00:00:00+00:00', '2010-10-30T00:00:00+00:00', '2019-11-30T14:44:35+00:00']
        in_seconds = [946684800, 1288396800, 1575125075]
        for i, d in zip(in_seconds, dates):
            self.assertEqual(i, utility.to_seconds(d))