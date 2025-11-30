"""
API views for task analysis endpoints.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .scoring import PriorityScorer
from .serializers import TaskSerializer, TaskAnalyzeSerializer
from datetime import date, timedelta


@csrf_exempt
@api_view(['POST'])
def analyze_tasks(request):
    """
    Analyze and sort tasks by priority.
    
    POST /api/tasks/analyze/
    
    Request body:
    {
        "tasks": [
            {
                "title": "Fix login bug",
                "due_date": "2025-11-30",
                "estimated_hours": 3,
                "importance": 8,
                "dependencies": []
            }
        ],
        "strategy": "smart_balance"  // optional
    }
    
    Returns sorted tasks with priority scores.
    """
    try:
        # Validate input
        serializer = TaskAnalyzeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid input', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tasks = serializer.validated_data['tasks']
        strategy = serializer.validated_data.get('strategy', 'smart_balance')
        
        # Convert serialized tasks to dictionaries
        task_dicts = []
        for task in tasks:
            task_dict = {
                'id': task.get('id') or task.get('title'),
                'title': task['title'],
                'due_date': task.get('due_date'),
                'estimated_hours': task.get('estimated_hours', 4),
                'importance': task.get('importance', 5),
                'dependencies': task.get('dependencies', [])
            }
            task_dicts.append(task_dict)
        
        # Analyze and sort tasks
        result = PriorityScorer.analyze_and_sort_tasks(task_dicts, strategy=strategy)
        
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': 'Internal server error', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['GET', 'POST'])
def suggest_tasks(request):
    """
    Get top 3 task suggestions for today.
    
    GET /api/tasks/suggest/?strategy=smart_balance
    POST /api/tasks/suggest/ with tasks in body
    
    Query parameters (GET) or body (POST):
    - strategy: Sorting strategy (optional, default: smart_balance)
    - tasks: List of tasks (POST only)
    
    Returns top 3 tasks with explanations.
    """
    try:
        strategy = request.query_params.get('strategy') or (request.data.get('strategy') if hasattr(request, 'data') and request.data else 'smart_balance')
        
        # Sample tasks for demonstration if none provided
        sample_tasks = [
            {
                'id': 'task_1',
                'title': 'Review pull requests',
                'due_date': str(date.today()),
                'estimated_hours': 2,
                'importance': 7,
                'dependencies': []
            },
            {
                'id': 'task_2',
                'title': 'Fix critical bug',
                'due_date': str(date.today() - timedelta(days=1)),  # Yesterday
                'estimated_hours': 4,
                'importance': 9,
                'dependencies': []
            },
            {
                'id': 'task_3',
                'title': 'Update documentation',
                'due_date': str(date.today() + timedelta(days=7)),  # Next week
                'estimated_hours': 1,
                'importance': 5,
                'dependencies': []
            }
        ]
        
        # Check if tasks provided in request
        tasks = None
        if request.method == 'POST' and hasattr(request, 'data') and request.data:
            tasks = request.data.get('tasks')
        
        if not tasks:
            # Use sample tasks for demonstration
            tasks = sample_tasks
            message = "Using sample tasks. Provide tasks via POST body for real analysis."
        else:
            message = "Analyzed provided tasks."
        
        # Analyze tasks
        result = PriorityScorer.analyze_and_sort_tasks(tasks, strategy=strategy)
        
        # Get top 3
        top_tasks = result['tasks'][:3]
        
        # Format response with explanations
        suggestions = []
        for i, task in enumerate(top_tasks, 1):
            suggestions.append({
                'rank': i,
                'task': {
                    'title': task['title'],
                    'due_date': task.get('due_date'),
                    'estimated_hours': task.get('estimated_hours'),
                    'importance': task.get('importance'),
                },
                'priority_score': task['priority_score'],
                'why_this_task': task.get('explanation', 'High priority based on multiple factors'),
                'component_scores': task.get('component_scores', {})
            })
        
        return Response({
            'suggestions': suggestions,
            'strategy_used': strategy,
            'message': message,
            'circular_dependencies_detected': len(result.get('circular_dependencies', [])) > 0
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': 'Internal server error', 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

