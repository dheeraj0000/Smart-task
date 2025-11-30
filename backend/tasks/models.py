"""
Task model for the Smart Task Analyzer.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Task(models.Model):
    """
    Represents a task with properties for priority calculation.
    """
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="Estimated hours to complete the task"
    )
    importance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Importance rating from 1-10"
    )
    dependencies = models.JSONField(
        default=list,
        help_text="List of task IDs that this task depends on"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

