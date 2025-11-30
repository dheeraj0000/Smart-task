"""
Unit tests for the priority scoring algorithm.
"""
from django.test import TestCase
from datetime import date, timedelta
from tasks.scoring import PriorityScorer


class PriorityScoringTests(TestCase):
    """
    Test suite for priority scoring algorithm.
    """
    
    def test_urgency_score_past_due(self):
        """Test that past-due tasks get higher urgency scores."""
        yesterday = str(date.today() - timedelta(days=1))
        last_week = str(date.today() - timedelta(days=7))
        
        score_yesterday = PriorityScorer.calculate_urgency_score(yesterday)
        score_last_week = PriorityScorer.calculate_urgency_score(last_week)
        score_future = PriorityScorer.calculate_urgency_score(str(date.today() + timedelta(days=7)))
        
        # Past-due tasks should score higher than future tasks
        self.assertGreater(score_yesterday, score_future)
        self.assertGreater(score_last_week, score_future)
        # More overdue = higher score
        self.assertGreater(score_yesterday, score_last_week)
    
    def test_urgency_score_due_today(self):
        """Test that tasks due today get maximum urgency score."""
        today = str(date.today())
        score = PriorityScorer.calculate_urgency_score(today)
        
        # Should be close to 1.0 (maximum)
        self.assertGreaterEqual(score, 0.9)
    
    def test_importance_score_normalization(self):
        """Test that importance scores are properly normalized."""
        score_1 = PriorityScorer.calculate_importance_score(1)
        score_5 = PriorityScorer.calculate_importance_score(5)
        score_10 = PriorityScorer.calculate_importance_score(10)
        
        # Should be in ascending order
        self.assertLess(score_1, score_5)
        self.assertLess(score_5, score_10)
        # Should be in valid range
        self.assertGreaterEqual(score_1, 0.0)
        self.assertLessEqual(score_10, 1.0)
    
    def test_effort_score_inverse_relationship(self):
        """Test that lower effort tasks score higher."""
        score_1h = PriorityScorer.calculate_effort_score(1)
        score_4h = PriorityScorer.calculate_effort_score(4)
        score_8h = PriorityScorer.calculate_effort_score(8)
        
        # Lower effort should score higher
        self.assertGreater(score_1h, score_4h)
        self.assertGreater(score_4h, score_8h)
    
    def test_dependency_score_blocking_tasks(self):
        """Test that tasks blocking others get higher dependency scores."""
        task_list = [
            {'id': 'task_1', 'title': 'Task 1', 'dependencies': []},
            {'id': 'task_2', 'title': 'Task 2', 'dependencies': ['task_1']},
            {'id': 'task_3', 'title': 'Task 3', 'dependencies': ['task_1']},
        ]
        
        score_task1 = PriorityScorer.calculate_dependency_score('task_1', task_list)
        score_task2 = PriorityScorer.calculate_dependency_score('task_2', task_list)
        
        # Task 1 blocks 2 tasks, should score higher
        self.assertGreater(score_task1, score_task2)
    
    def test_circular_dependency_detection(self):
        """Test detection of circular dependencies."""
        tasks_with_cycle = [
            {'id': 'task_1', 'title': 'Task 1', 'dependencies': ['task_2']},
            {'id': 'task_2', 'title': 'Task 2', 'dependencies': ['task_1']},
        ]
        
        cycles = PriorityScorer.detect_circular_dependencies(tasks_with_cycle)
        self.assertGreater(len(cycles), 0)
        
        # Test no cycles
        tasks_no_cycle = [
            {'id': 'task_1', 'title': 'Task 1', 'dependencies': []},
            {'id': 'task_2', 'title': 'Task 2', 'dependencies': ['task_1']},
        ]
        
        cycles = PriorityScorer.detect_circular_dependencies(tasks_no_cycle)
        self.assertEqual(len(cycles), 0)
    
    def test_priority_score_calculation(self):
        """Test complete priority score calculation."""
        task = {
            'id': 'test_task',
            'title': 'Test Task',
            'due_date': str(date.today()),
            'estimated_hours': 2,
            'importance': 8,
            'dependencies': []
        }
        
        task_list = [task]
        result = PriorityScorer.calculate_priority_score(task, task_list, strategy='smart_balance')
        
        # Should have all required fields
        self.assertIn('priority_score', result)
        self.assertIn('component_scores', result)
        self.assertIn('explanation', result)
        
        # Priority score should be positive
        self.assertGreater(result['priority_score'], 0)
        
        # Component scores should be present
        self.assertIn('urgency', result['component_scores'])
        self.assertIn('importance', result['component_scores'])
        self.assertIn('effort', result['component_scores'])
        self.assertIn('dependencies', result['component_scores'])
    
    def test_different_sorting_strategies(self):
        """Test that different strategies produce different rankings."""
        tasks = [
            {
                'id': 'urgent_low_importance',
                'title': 'Urgent but not important',
                'due_date': str(date.today()),
                'estimated_hours': 2,
                'importance': 3,
                'dependencies': []
            },
            {
                'id': 'important_not_urgent',
                'title': 'Important but not urgent',
                'due_date': str(date.today() + timedelta(days=30)),
                'estimated_hours': 4,
                'importance': 9,
                'dependencies': []
            },
        ]
        
        # Deadline driven should favor urgent task
        result_deadline = PriorityScorer.analyze_and_sort_tasks(tasks, strategy='deadline_driven')
        
        # High impact should favor important task
        result_impact = PriorityScorer.analyze_and_sort_tasks(tasks, strategy='high_impact')
        
        # Results should differ
        self.assertNotEqual(
            result_deadline['tasks'][0]['id'],
            result_impact['tasks'][0]['id']
        )
    
    def test_analyze_and_sort_empty_list(self):
        """Test handling of empty task list."""
        result = PriorityScorer.analyze_and_sort_tasks([])
        
        self.assertEqual(len(result['tasks']), 0)
        self.assertEqual(len(result['circular_dependencies']), 0)
    
    def test_analyze_and_sort_with_missing_fields(self):
        """Test handling of tasks with missing optional fields."""
        tasks = [
            {
                'id': 'minimal_task',
                'title': 'Minimal Task',
                # Missing optional fields
            }
        ]
        
        result = PriorityScorer.analyze_and_sort_tasks(tasks)
        
        # Should handle gracefully with defaults
        self.assertEqual(len(result['tasks']), 1)
        self.assertIn('priority_score', result['tasks'][0])

