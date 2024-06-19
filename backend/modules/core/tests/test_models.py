# myapp/core/tests/test_models.py

import uuid

from django.test import TestCase
from django.utils import timezone

from modules.core.models import CeleryResult


class CeleryResultModelTest(TestCase):

    def setUp(self):
        self.task_id = uuid.uuid4()
        self.celery_result = CeleryResult.objects.create(
            task_id=self.task_id,
            task_name="Test Task",
            arguments=[123, "test", {"arg1": 123, "arg2": "abc"}],
            is_success=True,
            result={"message": "Success"},
            errors=None,
            logs=["Log line 1", "Log line 2"],
        )

    def test_celery_result_creation(self):
        self.assertIsInstance(self.celery_result, CeleryResult)
        self.assertEqual(self.celery_result.task_id, uuid.UUID(str(self.task_id)))
        self.assertEqual(self.celery_result.task_name, "Test Task")
        self.assertEqual(
            self.celery_result.arguments, [123, "test", {"arg1": 123, "arg2": "abc"}]
        )
        self.assertTrue(self.celery_result.is_success)
        self.assertEqual(self.celery_result.result, {"message": "Success"})
        self.assertIsNone(self.celery_result.errors)
        self.assertEqual(self.celery_result.logs, ["Log line 1", "Log line 2"])

    def test_auto_created_fields(self):
        self.assertIsNotNone(self.celery_result.created_at)
        self.assertIsNotNone(self.celery_result.updated_at)
        self.assertLess(self.celery_result.created_at, timezone.now())
        self.assertLess(self.celery_result.updated_at, timezone.now())
        self.assertGreaterEqual(
            self.celery_result.updated_at, self.celery_result.created_at
        )
