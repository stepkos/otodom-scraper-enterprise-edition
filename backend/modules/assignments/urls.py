from django.urls import re_path
from modules.assignments.views import AssignmentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"assignments", AssignmentViewSet, basename="assignments")
assignments_urlpatterns = router.urls
