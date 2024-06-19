from unittest.mock import patch

from django.test import TestCase

from modules.scrapers.services.custom_logger import CustomLogger


class TestCustomLogger(TestCase):

    @patch("celery.utils.log.get_task_logger")
    def test_log_error(self, mock_get_task_logger):
        mock_logger = mock_get_task_logger(__name__)
        custom_logger = CustomLogger(logger=mock_logger)

        custom_logger.log_error("Test error")

        self.assertFalse(custom_logger.success)
        self.assertIn("Test error", custom_logger.errors)
        self.assertIn("Error Test error", custom_logger.logs)
        mock_logger.error.assert_called_with("Test error")

    @patch("celery.utils.log.get_task_logger")
    def test_log_info(self, mock_get_task_logger):
        mock_logger = mock_get_task_logger(__name__)
        custom_logger = CustomLogger(logger=mock_logger)

        custom_logger.log_info("Test info")

        self.assertIn("Test info", custom_logger.logs)
        mock_logger.info.assert_not_called()

    def test_get_result_dict(self):
        custom_logger = CustomLogger()

        custom_logger.log_error("Test error")
        custom_logger.log_info("Test info")

        result = custom_logger.get_result_dict()

        expected_result = {
            "success": False,
            "errors": ["Test error"],
            "logs": ["Error Test error", "Test info"],
        }

        self.assertEqual(result, expected_result)
