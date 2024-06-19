from django.test import TestCase

from modules.core.utils import flatten, is_json_serializable


class TestCeleryTaskDecorator(TestCase):

    def test_is_json_serializable(self):
        self.assertTrue(is_json_serializable({"key": "value"}))
        self.assertFalse(is_json_serializable(set()))
        self.assertFalse(is_json_serializable(lambda x: x))
        self.assertTrue(is_json_serializable([1, 2, 3]))

    def test_flatten(self):
        self.assertEqual(flatten([1, [2, [3, 4], 5], 6]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(flatten([[[1]], [2, [3, [4, [5]]]]]), [1, 2, 3, 4, 5])
