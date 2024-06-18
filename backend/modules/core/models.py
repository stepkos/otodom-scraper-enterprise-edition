import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class CeleryResult(BaseModel):
    task_id = models.CharField(max_length=255, unique=True)
    task_name = models.CharField(max_length=255)
    arguments = models.JSONField(null=True, blank=True)
    is_success = models.BooleanField(null=False, blank=False, default=True)
    result = models.JSONField(null=True, blank=True)
    errors = models.JSONField(null=True, blank=True)
    logs = models.JSONField(null=True, blank=True)



