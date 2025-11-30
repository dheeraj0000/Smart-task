"""
Serializers for task API endpoints.
"""
from rest_framework import serializers
from datetime import date


class TaskSerializer(serializers.Serializer):
    """
    Serializer for task input/output.
    """
    id = serializers.CharField(required=False, allow_null=True)
    title = serializers.CharField(max_length=200)
    due_date = serializers.DateField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField(min_value=0.1)
    importance = serializers.IntegerField(min_value=1, max_value=10)
    dependencies = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    priority_score = serializers.FloatField(read_only=True, required=False)
    component_scores = serializers.DictField(read_only=True, required=False)
    explanation = serializers.CharField(read_only=True, required=False)
    
    def validate_due_date(self, value):
        """Validate due date is not too far in the past (optional validation)."""
        if value and value < date(2020, 1, 1):
            raise serializers.ValidationError("Due date cannot be before 2020.")
        return value
    
    def validate_dependencies(self, value):
        """Ensure dependencies is a list."""
        if not isinstance(value, list):
            return []
        return value


class TaskAnalyzeSerializer(serializers.Serializer):
    """
    Serializer for task analysis request.
    """
    tasks = TaskSerializer(many=True)
    strategy = serializers.ChoiceField(
        choices=['smart_balance', 'fastest_wins', 'high_impact', 'deadline_driven'],
        default='smart_balance',
        required=False
    )

