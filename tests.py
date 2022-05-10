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
        data = {"data": [391, 5, 1, 1, 52]}
        result = api.send_data(data)
        self.assertEqual(result, {'predictions': [[0.0, 0.0, 0.0, 1.0, 0.0]]})

    def test_quality_eveluation(self):
        data = {"data": [391, 5, 1, 1, 52]}
        result = api.quality_value(data)
        self.assertEqual(result, 4)


if __name__ == '__main__':
    unittest.main()
