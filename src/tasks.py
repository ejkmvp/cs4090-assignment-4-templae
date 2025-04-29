import json
import os
from datetime import datetime

# File path for task storage
DEFAULT_TASKS_FILE = "tasks.json"

def load_tasks(file_path=DEFAULT_TASKS_FILE):
    """
    Load tasks from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing tasks
        
    Returns:
        list: List of task dictionaries, empty list if file doesn't exist
    """
    try:
        with open(file_path, "r") as f:
            content = json.load(f)
            assert type(content) == list #assert that the content is a list
            for task in content:
                assert set(task.keys()) == set(["id", "title", "description", "priority", "category", "due_date", "completed", "created_at"]) #assert all keys are present
                #assert expectations on all fields
                assert type(task["id"]) == int
                assert type(task["title"]) == str
                assert type(task["description"]) == str
                assert task["priority"] in ["Low", "Medium", "High"]
                assert task["category"] in ["Work", "Personal", "School", "Other"]
                assert type(task["due_date"]) == str
                assert type(task["completed"]) == bool
                assert type(task["created_at"]) == str
            return content
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Handle corrupted JSON file
        print(f"Warning: {file_path} contains invalid JSON. Creating new tasks list.")
        return []
    except AssertionError as e:
        print(f"Warning: {file_path} contains invalid tasks. Creating new task list: {e}")
        return []

def save_tasks(tasks, file_path=DEFAULT_TASKS_FILE):
    """
    Save tasks to a JSON file.
    
    Args:
        tasks (list): List of task dictionaries
        file_path (str): Path to save the JSON file
    """
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=2)

def generate_unique_id(tasks):
    """
    Generate a unique ID for a new task.
    
    Args:
        tasks (list): List of existing task dictionaries
        
    Returns:
        int: A unique ID for a new task
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def filter_tasks_by_priority(tasks, priority):
    """
    Filter tasks by priority level.
    
    Args:
        tasks (list): List of task dictionaries
        priority (str): Priority level to filter by (High, Medium, Low)
        
    Returns:
        list: Filtered list of tasks matching the priority
    """
    return [task for task in tasks if task.get("priority") == priority]

def filter_tasks_by_category(tasks, category):
    """
    Filter tasks by category.
    
    Args:
        tasks (list): List of task dictionaries
        category (str): Category to filter by
        
    Returns:
        list: Filtered list of tasks matching the category
    """
    return [task for task in tasks if task.get("category") == category]

def filter_tasks_by_completion(tasks, completed=True):
    """
    Filter tasks by completion status.
    
    Args:
        tasks (list): List of task dictionaries
        completed (bool): Completion status to filter by
        
    Returns:
        list: Filtered list of tasks matching the completion status
    """
    return [task for task in tasks if task.get("completed") == completed]

def search_tasks(tasks, query):
    """
    Search tasks by a text query in title and description.
    
    Args:
        tasks (list): List of task dictionaries
        query (str): Search query
        
    Returns:
        list: Filtered list of tasks matching the search query
    """
    query = query.lower()
    return [
        task for task in tasks 
        if query in task.get("title", "").lower() or 
           query in task.get("description", "").lower()
    ]

def get_overdue_tasks(tasks, filterOverdue="Overdue"):
    today = datetime.now().strftime("%Y-%m-%d")
    if filterOverdue == "All":
        return tasks
    if filterOverdue == "Not Overdue":
        return [
            task for task in tasks 
            if not task.get("completed", False) and 
            task.get("due_date", "") >= today
        ]
    return [
        task for task in tasks 
        if not task.get("completed", False) and 
        task.get("due_date", "") < today
    ]

def order_tasks(tasks, order_by):
    if order_by == "Priority":
        priorityMap = {"High": 1, "Medium": 2, "Low": 3}
        return sorted(tasks, key=(lambda x: priorityMap.get(x.get("priority", ""), 3)))    
    if order_by == "Category":
        return sorted(tasks, key=(lambda x: x.get("category", "")))
    if order_by == "Due Date":
        return sorted(tasks, key=(lambda x: x.get("due_date", "")))