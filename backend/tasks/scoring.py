"""
Priority scoring algorithm for tasks.

This module implements the core priority calculation logic that considers:
- Urgency (due date proximity)
- Importance (user-provided rating)
- Effort (estimated hours)
- Dependencies (blocking relationships)
"""
from datetime import date, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict


class PriorityScorer:
    """
    Calculates priority scores for tasks based on multiple factors.
    
    The scoring algorithm uses configurable weights to balance different
    priority factors. This allows for different sorting strategies.
    """
    
    # Default weights for "Smart Balance" strategy
    DEFAULT_WEIGHTS = {
        'urgency': 0.35,      # 35% weight on due date
        'importance': 0.30,   # 30% weight on importance
        'effort': 0.20,       # 20% weight on effort (inverse - lower effort = higher score)
        'dependencies': 0.15  # 15% weight on blocking other tasks
    }
    
    # Strategy-specific weight configurations
    STRATEGY_WEIGHTS = {
        'fastest_wins': {
            'urgency': 0.20,
            'importance': 0.20,
            'effort': 0.50,  # Heavily favor low-effort tasks
            'dependencies': 0.10
        },
        'high_impact': {
            'urgency': 0.15,
            'importance': 0.60,  # Heavily favor high importance
            'effort': 0.15,
            'dependencies': 0.10
        },
        'deadline_driven': {
            'urgency': 0.70,  # Heavily favor urgent tasks
            'importance': 0.15,
            'effort': 0.10,
            'dependencies': 0.05
        },
        'smart_balance': DEFAULT_WEIGHTS
    }
    
    @staticmethod
    def calculate_urgency_score(due_date: Optional[str], current_date: date = None) -> float:
        """
        Calculate urgency score based on due date.
        
        Scoring logic:
        - Past due: Score increases exponentially with days overdue
        - Today: Maximum score (1.0)
        - Future: Score decreases as days until due date increase
        - No due date: Minimum urgency score (0.1)
        
        Args:
            due_date: Due date string in YYYY-MM-DD format or None
            current_date: Current date (defaults to today)
            
        Returns:
            Urgency score between 0.0 and 1.0+
        """
        if current_date is None:
            current_date = date.today()
        
        if not due_date:
            return 0.1  # Low urgency for tasks without due dates
        
        try:
            due = date.fromisoformat(due_date) if isinstance(due_date, str) else due_date
        except (ValueError, AttributeError):
            return 0.1  # Invalid date format
        
        days_diff = (due - current_date).days
        
        if days_diff < 0:
            # Past due: exponential penalty
            # Formula: 1.0 + (days_overdue * 0.1)
            # This ensures past-due tasks always score higher than future tasks
            return 1.0 + (abs(days_diff) * 0.1)
        elif days_diff == 0:
            return 1.0  # Due today - maximum urgency
        elif days_diff <= 7:
            # Due within a week: high urgency
            return 0.9 - (days_diff * 0.1)
        elif days_diff <= 30:
            # Due within a month: medium urgency
            return 0.3 - ((days_diff - 7) / 23 * 0.2)
        else:
            # Due far in future: low urgency
            return max(0.1, 0.1 - ((days_diff - 30) / 365 * 0.05))
    
    @staticmethod
    def calculate_importance_score(importance: int) -> float:
        """
        Normalize importance rating (1-10) to 0.0-1.0 scale.
        
        Args:
            importance: Importance rating from 1 to 10
            
        Returns:
            Normalized importance score
        """
        if not isinstance(importance, (int, float)):
            return 0.5  # Default for invalid input
        
        # Clamp to valid range
        importance = max(1, min(10, int(importance)))
        
        # Normalize to 0.0-1.0 (1 -> 0.1, 10 -> 1.0)
        return (importance - 1) / 9.0
    
    @staticmethod
    def calculate_effort_score(estimated_hours: float) -> float:
        """
        Calculate effort score (inverse relationship - lower effort = higher score).
        
        Lower effort tasks are "quick wins" and should score higher.
        Uses logarithmic scaling to prevent very small tasks from dominating.
        
        Args:
            estimated_hours: Estimated hours to complete task
            
        Returns:
            Effort score between 0.0 and 1.0
        """
        if not isinstance(estimated_hours, (int, float)) or estimated_hours <= 0:
            return 0.5  # Default for invalid input
        
        # Use inverse logarithmic relationship
        # Tasks under 1 hour get high score, tasks over 8 hours get low score
        if estimated_hours <= 1:
            return 1.0
        elif estimated_hours <= 4:
            return 1.0 - ((estimated_hours - 1) / 3 * 0.3)
        elif estimated_hours <= 8:
            return 0.7 - ((estimated_hours - 4) / 4 * 0.3)
        else:
            # Very long tasks get diminishing returns
            return max(0.1, 0.4 - ((estimated_hours - 8) / 16 * 0.3))
    
    @staticmethod
    def calculate_dependency_score(task_id: Any, task_list: List[Dict[str, Any]]) -> float:
        """
        Calculate dependency score based on how many tasks depend on this task.
        
        Tasks that block other tasks should have higher priority.
        Also detects circular dependencies.
        
        Args:
            task_id: ID of the current task
            task_list: List of all tasks
            
        Returns:
            Dependency score between 0.0 and 1.0
        """
        if not task_list:
            return 0.0
        
        # Count how many tasks depend on this task
        dependents_count = 0
        for task in task_list:
            deps = task.get('dependencies', [])
            if isinstance(deps, list) and task_id in deps:
                dependents_count += 1
        
        # Normalize: 0 dependents = 0.0, 3+ dependents = 1.0
        if dependents_count == 0:
            return 0.0
        elif dependents_count == 1:
            return 0.5
        elif dependents_count == 2:
            return 0.75
        else:
            return 1.0
    
    @staticmethod
    def detect_circular_dependencies(tasks: List[Dict[str, Any]]) -> List[List[Any]]:
        """
        Detect circular dependencies in the task list.
        
        Uses DFS to find cycles in the dependency graph.
        
        Args:
            tasks: List of tasks with dependencies
            
        Returns:
            List of cycles found (each cycle is a list of task IDs)
        """
        # Build adjacency list
        graph = defaultdict(list)
        task_ids = []
        
        for task in tasks:
            task_id = task.get('id') or task.get('title')  # Use title as fallback ID
            if task_id:
                task_ids.append(task_id)
                deps = task.get('dependencies', [])
                if isinstance(deps, list):
                    graph[task_id] = deps
        
        # DFS to detect cycles
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, []):
                if neighbor in task_ids:  # Only check if neighbor exists
                    dfs(neighbor, path[:])
            
            rec_stack.remove(node)
        
        for task_id in task_ids:
            if task_id not in visited:
                dfs(task_id, [])
        
        return cycles
    
    @classmethod
    def calculate_priority_score(
        cls,
        task: Dict[str, Any],
        task_list: List[Dict[str, Any]],
        strategy: str = 'smart_balance',
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive priority score for a task.
        
        Args:
            task: Task dictionary with required fields
            task_list: List of all tasks (for dependency calculation)
            strategy: Sorting strategy name
            weights: Custom weights (overrides strategy if provided)
            
        Returns:
            Dictionary with task data, score, and component scores
        """
        # Get weights based on strategy
        if weights:
            w = weights
        else:
            w = cls.STRATEGY_WEIGHTS.get(strategy, cls.DEFAULT_WEIGHTS)
        
        # Extract task data with validation
        task_id = task.get('id') or task.get('title')
        due_date = task.get('due_date')
        importance = task.get('importance', 5)
        estimated_hours = task.get('estimated_hours', 4)
        
        # Calculate component scores
        urgency_score = cls.calculate_urgency_score(due_date)
        importance_score = cls.calculate_importance_score(importance)
        effort_score = cls.calculate_effort_score(estimated_hours)
        dependency_score = cls.calculate_dependency_score(task_id, task_list)
        
        # Calculate weighted total score
        total_score = (
            urgency_score * w['urgency'] +
            importance_score * w['importance'] +
            effort_score * w['effort'] +
            dependency_score * w['dependencies']
        )
        
        # Generate explanation
        explanation = cls._generate_explanation(
            urgency_score, importance_score, effort_score, dependency_score,
            due_date, importance, estimated_hours, total_score
        )
        
        return {
            **task,
            'priority_score': round(total_score, 3),
            'component_scores': {
                'urgency': round(urgency_score, 3),
                'importance': round(importance_score, 3),
                'effort': round(effort_score, 3),
                'dependencies': round(dependency_score, 3)
            },
            'explanation': explanation
        }
    
    @staticmethod
    def _generate_explanation(
        urgency: float,
        importance: float,
        effort: float,
        dependency: float,
        due_date: Optional[str],
        importance_rating: int,
        estimated_hours: float,
        total_score: float
    ) -> str:
        """
        Generate human-readable explanation for the priority score.
        """
        reasons = []
        
        if urgency >= 0.8:
            if due_date:
                try:
                    due = date.fromisoformat(due_date) if isinstance(due_date, str) else due_date
                    if due < date.today():
                        days_overdue = (date.today() - due).days
                        reasons.append(f"Overdue by {days_overdue} day(s)")
                    else:
                        reasons.append("Due very soon")
                except:
                    reasons.append("High urgency")
            else:
                reasons.append("High urgency")
        
        if importance >= 0.7:
            reasons.append(f"High importance ({importance_rating}/10)")
        
        if effort >= 0.7:
            reasons.append(f"Quick win ({estimated_hours}h estimated)")
        
        if dependency >= 0.5:
            reasons.append("Blocks other tasks")
        
        if not reasons:
            reasons.append("Standard priority task")
        
        return "; ".join(reasons)
    
    @classmethod
    def analyze_and_sort_tasks(
        cls,
        tasks: List[Dict[str, Any]],
        strategy: str = 'smart_balance',
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a list of tasks and return them sorted by priority.
        
        Args:
            tasks: List of task dictionaries
            strategy: Sorting strategy to use
            weights: Custom weights (optional)
            
        Returns:
            Dictionary with sorted tasks, circular dependencies, and metadata
        """
        if not tasks:
            return {
                'tasks': [],
                'circular_dependencies': [],
                'strategy': strategy,
                'message': 'No tasks provided'
            }
        
        # Validate and clean tasks
        validated_tasks = []
        for i, task in enumerate(tasks):
            # Ensure each task has an ID
            if 'id' not in task:
                task['id'] = task.get('title', f'task_{i}')
            
            # Validate required fields
            if 'title' not in task:
                continue  # Skip invalid tasks
            
            # Set defaults for missing fields
            task.setdefault('due_date', None)
            task.setdefault('importance', 5)
            task.setdefault('estimated_hours', 4)
            task.setdefault('dependencies', [])
            
            validated_tasks.append(task)
        
        # Detect circular dependencies
        circular_deps = cls.detect_circular_dependencies(validated_tasks)
        
        # Calculate scores for all tasks
        scored_tasks = []
        for task in validated_tasks:
            scored_task = cls.calculate_priority_score(task, validated_tasks, strategy, weights)
            scored_tasks.append(scored_task)
        
        # Sort by priority score (descending)
        scored_tasks.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return {
            'tasks': scored_tasks,
            'circular_dependencies': circular_deps,
            'strategy': strategy,
            'total_tasks': len(scored_tasks),
            'message': f'Analyzed {len(scored_tasks)} tasks using {strategy} strategy'
        }

