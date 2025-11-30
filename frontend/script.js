// Global state
let tasks = [];
const API_BASE_URL = '/api';

// Strategy descriptions
const strategyDescriptions = {
    'smart_balance': 'Balances urgency, importance, effort, and dependencies for optimal task prioritization.',
    'fastest_wins': 'Prioritizes low-effort tasks to maximize quick wins and build momentum.',
    'high_impact': 'Focuses on high-importance tasks regardless of urgency or effort.',
    'deadline_driven': 'Prioritizes tasks based primarily on due dates and deadlines.'
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Update strategy description on change
    const strategySelect = document.getElementById('strategy');
    const strategyDescription = document.getElementById('strategy-description');
    
    strategySelect.addEventListener('change', function() {
        strategyDescription.textContent = strategyDescriptions[this.value] || '';
    });
    
    // Form submission
    const taskForm = document.getElementById('task-form');
    taskForm.addEventListener('submit', function(e) {
        e.preventDefault();
        addTaskFromForm();
    });
    
    // Load tasks from localStorage if available
    loadTasksFromStorage();
    updateTaskList();
});

// Tab switching
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName + '-tab').classList.add('active');
}

// Add task from form
function addTaskFromForm() {
    const form = document.getElementById('task-form');
    const formData = new FormData(form);
    
    const task = {
        title: formData.get('title'),
        due_date: formData.get('due_date') || null,
        estimated_hours: parseFloat(formData.get('estimated_hours')),
        importance: parseInt(formData.get('importance')),
        dependencies: formData.get('dependencies') 
            ? formData.get('dependencies').split(',').map(d => d.trim()).filter(d => d)
            : []
    };
    
    // Validate
    if (!task.title || !task.estimated_hours || !task.importance) {
        showError('Please fill in all required fields.');
        return;
    }
    
    if (task.importance < 1 || task.importance > 10) {
        showError('Importance must be between 1 and 10.');
        return;
    }
    
    if (task.estimated_hours <= 0) {
        showError('Estimated hours must be greater than 0.');
        return;
    }
    
    // Add ID if not present
    if (!task.id) {
        task.id = 'task_' + Date.now();
    }
    
    tasks.push(task);
    saveTasksToStorage();
    updateTaskList();
    form.reset();
    
    // Show success message
    showSuccess('Task added successfully!');
}

// Load bulk tasks from JSON
function loadBulkTasks() {
    const jsonInput = document.getElementById('json-input').value.trim();
    
    if (!jsonInput) {
        showError('Please paste JSON task data.');
        return;
    }
    
    try {
        const parsedTasks = JSON.parse(jsonInput);
        
        if (!Array.isArray(parsedTasks)) {
            showError('JSON must be an array of tasks.');
            return;
        }
        
        // Validate and add IDs
        parsedTasks.forEach((task, index) => {
            if (!task.title) {
                throw new Error(`Task at index ${index} is missing required field 'title'`);
            }
            
            if (!task.id) {
                task.id = 'task_' + Date.now() + '_' + index;
            }
            
            // Set defaults
            task.due_date = task.due_date || null;
            task.estimated_hours = task.estimated_hours || 4;
            task.importance = task.importance || 5;
            task.dependencies = task.dependencies || [];
        });
        
        tasks = parsedTasks;
        saveTasksToStorage();
        updateTaskList();
        showSuccess(`Loaded ${parsedTasks.length} tasks successfully!`);
        
    } catch (error) {
        showError('Invalid JSON format: ' + error.message);
    }
}

// Update task list display
function updateTaskList() {
    const taskList = document.getElementById('task-list');
    const taskCount = document.getElementById('task-count');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    taskCount.textContent = tasks.length;
    analyzeBtn.disabled = tasks.length === 0;
    
    if (tasks.length === 0) {
        taskList.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📋</div><p>No tasks added yet. Add tasks to get started!</p></div>';
        return;
    }
    
    taskList.innerHTML = tasks.map((task, index) => `
        <div class="task-item">
            <div class="task-item-info">
                <div class="task-item-title">${escapeHtml(task.title)}</div>
                <div class="task-item-details">
                    Due: ${task.due_date || 'No due date'} | 
                    Hours: ${task.estimated_hours}h | 
                    Importance: ${task.importance}/10
                    ${task.dependencies.length > 0 ? ` | Depends on: ${task.dependencies.join(', ')}` : ''}
                </div>
            </div>
            <button class="task-item-remove" onclick="removeTask(${index})">Remove</button>
        </div>
    `).join('');
}

// Remove task
function removeTask(index) {
    tasks.splice(index, 1);
    saveTasksToStorage();
    updateTaskList();
}

// Clear all tasks
function clearTasks() {
    if (confirm('Are you sure you want to clear all tasks?')) {
        tasks = [];
        saveTasksToStorage();
        updateTaskList();
        document.getElementById('output-section').style.display = 'none';
    }
}

// Analyze tasks
async function analyzeTasks() {
    if (tasks.length === 0) {
        showError('Please add at least one task before analyzing.');
        return;
    }
    
    const strategy = document.getElementById('strategy').value;
    
    // Show loading
    showLoading(true);
    hideError();
    
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/analyze/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tasks: tasks,
                strategy: strategy
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze tasks');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error details:', error);
        let errorMessage = 'Error analyzing tasks: ' + error.message;
        if (error.message === 'Failed to fetch') {
            errorMessage = 'Failed to connect to server. Please make sure the Django server is running on http://127.0.0.1:8000/';
        }
        showError(errorMessage);
    } finally {
        showLoading(false);
    }
}

// Display results
function displayResults(data) {
    const outputSection = document.getElementById('output-section');
    const resultsDiv = document.getElementById('results');
    const suggestionsDiv = document.getElementById('suggestions');
    const circularWarning = document.getElementById('circular-warning');
    
    outputSection.style.display = 'block';
    
    // Show circular dependency warning
    if (data.circular_dependencies && data.circular_dependencies.length > 0) {
        circularWarning.style.display = 'block';
        circularWarning.innerHTML = `
            <strong>⚠️ Warning:</strong> Circular dependencies detected! 
            Cycles: ${data.circular_dependencies.map(cycle => cycle.join(' → ')).join(', ')}
        `;
    } else {
        circularWarning.style.display = 'none';
    }
    
    // Display top 3 suggestions
    const top3 = data.tasks.slice(0, 3);
    suggestionsDiv.innerHTML = '<h3>🎯 Top 3 Recommendations</h3>' + 
        top3.map((task, index) => `
            <div class="suggestion-card">
                <div class="suggestion-rank">#${index + 1}</div>
                <div class="suggestion-title">${escapeHtml(task.title)}</div>
                <div class="suggestion-reason">${escapeHtml(task.explanation || 'High priority based on multiple factors')}</div>
                <div style="margin-top: 10px; opacity: 0.9;">
                    Priority Score: <strong>${task.priority_score.toFixed(3)}</strong>
                </div>
            </div>
        `).join('');
    
    // Display all tasks sorted by priority
    resultsDiv.innerHTML = '<h3>All Tasks (Sorted by Priority)</h3>' +
        data.tasks.map((task, index) => {
            const priorityClass = getPriorityClass(task.priority_score);
            const priorityLabel = getPriorityLabel(task.priority_score);
            
            return `
                <div class="result-item ${priorityClass}">
                    <div class="result-header">
                        <div class="result-title">#${index + 1}: ${escapeHtml(task.title)}</div>
                        <span class="priority-badge ${priorityLabel}">${priorityLabel} Priority</span>
                    </div>
                    
                    <div class="priority-score">Priority Score: ${task.priority_score.toFixed(3)}</div>
                    
                    <div class="result-details">
                        <div class="result-detail-item">
                            <div class="result-detail-label">Due Date</div>
                            <div class="result-detail-value">${task.due_date || 'No due date'}</div>
                        </div>
                        <div class="result-detail-item">
                            <div class="result-detail-label">Estimated Hours</div>
                            <div class="result-detail-value">${task.estimated_hours}h</div>
                        </div>
                        <div class="result-detail-item">
                            <div class="result-detail-label">Importance</div>
                            <div class="result-detail-value">${task.importance}/10</div>
                        </div>
                        <div class="result-detail-item">
                            <div class="result-detail-label">Dependencies</div>
                            <div class="result-detail-value">${task.dependencies.length > 0 ? task.dependencies.join(', ') : 'None'}</div>
                        </div>
                    </div>
                    
                    <div class="explanation">
                        <strong>Why this task:</strong> ${escapeHtml(task.explanation || 'Standard priority task')}
                    </div>
                    
                    ${task.component_scores ? `
                        <div style="margin-top: 15px; font-size: 0.9em; color: #666;">
                            <strong>Component Scores:</strong>
                            Urgency: ${task.component_scores.urgency.toFixed(2)} | 
                            Importance: ${task.component_scores.importance.toFixed(2)} | 
                            Effort: ${task.component_scores.effort.toFixed(2)} | 
                            Dependencies: ${task.component_scores.dependencies.toFixed(2)}
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    
    // Scroll to results
    outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Get priority class based on score
function getPriorityClass(score) {
    if (score >= 0.7) return 'high-priority';
    if (score >= 0.4) return 'medium-priority';
    return 'low-priority';
}

// Get priority label
function getPriorityLabel(score) {
    if (score >= 0.7) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
}

// Utility functions
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

function showSuccess(message) {
    // Simple success notification (could be enhanced with a toast library)
    const successDiv = document.createElement('div');
    successDiv.className = 'error';
    successDiv.style.background = '#d4edda';
    successDiv.style.color = '#155724';
    successDiv.style.borderColor = '#c3e6cb';
    successDiv.textContent = '✓ ' + message;
    document.querySelector('main').insertBefore(successDiv, document.querySelector('main').firstChild);
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Local storage functions
function saveTasksToStorage() {
    try {
        localStorage.setItem('smart_task_analyzer_tasks', JSON.stringify(tasks));
    } catch (e) {
        console.warn('Could not save to localStorage:', e);
    }
}

function loadTasksFromStorage() {
    try {
        const saved = localStorage.getItem('smart_task_analyzer_tasks');
        if (saved) {
            tasks = JSON.parse(saved);
        }
    } catch (e) {
        console.warn('Could not load from localStorage:', e);
        tasks = [];
    }
}

