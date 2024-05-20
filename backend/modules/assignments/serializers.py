from modules.assignments.models import Assignment
from rest_framework import serializers


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        read_only_fields = ("id", "sum")
        fields = ("id", "first_term", "second_term", "sum")
