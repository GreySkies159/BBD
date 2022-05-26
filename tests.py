import unittest

import api
import controller as con


class MyTestCase(unittest.TestCase):

    def test_average_text_size(self):
        file_to_parse = 'C:/Users/eglus/Desktop/bbd/pdfReferences/3858.pdf'

        result = con.get_most_common_size_from_file(file_to_parse)
        self.assertEqual(result, 10)

    def test_structure(self):
        file_to_parse = 'C:/Users/eglus/Desktop/bbd/pdfReferences/391.pdf'
        result = con.structure_evaluation(file_to_parse)
        self.assertEqual(result, (1, 1, 1, 1, 1, 1, 52))

    def test_integration_send(self):
        data = {"data": [0.054868121133181375, 1.0, 1, 1, 0.15249266862170088]}
        result = api.send_data(data)
        self.assertEqual(result, {'predictions': [[2.78428e-05, 0.0692753, 0.456691, 0.474005, 9.09898e-15]]})

    def test_quality_eveluation(self):
        data = {"data": [0.054868121133181375, 1.0, 1, 1, 0.15249266862170088]}
        result = api.quality_value(data)
        self.assertEqual(result, 4)

    def test_authors_split(self):
        authors_list = 'Ali Narin, Ceren Kaya, Ziynet Pamuk'
        result = con.split_authors_list(authors_list)
        self.assertEqual(result, ["Ali Narin", "Ceren Kaya", "Ziynet Pamuk"])

    def test_authors_split_without_spaces(self):
        authors_list = 'Ali Narin,Ceren Kaya,Ziynet Pamuk'
        result = con.split_authors_list(authors_list)
        self.assertEqual(result, ["Ali Narin", "Ceren Kaya", "Ziynet Pamuk"])

    def test_authors_split_with_semicolon(self):
        authors_list = 'Ali Narin;Ceren Kaya;Ziynet Pamuk'
        result = con.split_authors_list(authors_list)
        self.assertIsNot(result, ["Ali Narin", "Ceren Kaya", "Ziynet Pamuk"])


if __name__ == '__main__':
    unittest.main()
