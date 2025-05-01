import pytest
import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import search_tasks, load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks, order_tasks, delete_tasks

@pytest.fixture
def taskListOne():
    #Generate tasks which every combination of priority and category, due date (before or after current date), and completion status
    taskList = []
    taskId = 1
    for dueDate in [datetime.datetime.now() - datetime.timedelta(days = 2), datetime.datetime.now() + datetime.timedelta(days = 2)]:
        for completionStatus in [False, True]:
            taskList.append({
                "id": taskId,
                "title": f"test title {taskId}",
                "description": f"test description {taskId}",
                "priority": "Medium",
                "category": "Work",
                "due_date": dueDate.strftime("%Y-%m-%d"),
                "completed": completionStatus,
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            taskId += 1
    return taskList

@pytest.fixture
def taskListTwo():
    taskList = []
    taskId = 1
    for dueDate in [datetime.datetime.now() + datetime.timedelta(days = 2), datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(days = 2)]:
        for completionStatus in [False, True]:
            for priority in ["High", "Medium", "Low"]:
                for category  in ["Work", "Personal", "School", "Other"]:
                    taskList.append({
                        "id": taskId,
                        "title": f"test title {taskId}",
                        "description": f"test description {taskId}",
                        "priority": priority,
                        "category": category,
                        "due_date": dueDate.strftime("%Y-%m-%d"),
                        "completed": completionStatus,
                        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    taskId += 1
    return taskList


#Feature 1 - Add filtering for overdue tasks
#Test 1 - overdue task function returns overdue tasks that are not completed
def test_tdd_get_overdue_tasks_overdue(taskListOne):
    overdueTasks = get_overdue_tasks(taskListOne)
    assert len(overdueTasks) == 1
    assert set([overdueTasks[0]['id']]) == set([1])

#Write to pass

#Test 2 - overdue task function allows filtering for non-overdue tasks that are not completed
def test_tdd_get_overdue_tasks_not_overdue(taskListOne):
    overdueTasks = get_overdue_tasks(taskListOne, "Not Overdue")
    assert len(overdueTasks) == 1
    assert set([overdueTasks[0]['id']]) == set([3])

#Write to pass

#Test 3 - overdue task function does no filtering if "all" is passed through
def test_tdd_get_overdue_tasks_all(taskListOne):
    overdueTasks = get_overdue_tasks(taskListOne, "All")
    assert len(overdueTasks) == 4

#Write to pass
#Refactor


#Feature 2 - Add ordering by different fields

#Test 1 - allow ordering by Due Date
def test_tdd_order_tasks_order_by_due_date(taskListTwo):
    ordered_tasks = order_tasks(taskListTwo, "Due Date")
    for x in range(len(ordered_tasks) - 1):
        assert ordered_tasks[x]['due_date'] <= ordered_tasks[x+1]['due_date']

#Test 2 - allow ordering by priority
def test_tdd_order_tasks_order_by_priority(taskListTwo):
    ordered_tasks = order_tasks(taskListTwo, "Priority")
    symbolOrder = ["High", "Medium", "Low"]
    currentSymbol = 0
    for task in ordered_tasks:
        assert currentSymbol < 3
        if task['priority'] == symbolOrder[currentSymbol]:
            continue
        else:
            currentSymbol += 1

#Test 3 - allow ordering by category
def test_tdd_order_tasks_order_by_category(taskListTwo):
    ordered_tasks = order_tasks(taskListTwo, "Category")
    symbolOrder = ["Other", "Personal", "School", "Work"]
    currentSymbol = 0
    for task in ordered_tasks:
        assert currentSymbol < 4
        if task['category'] == symbolOrder[currentSymbol]:
            continue
        else:
            currentSymbol += 1


#Feature 3 - delete visible tasks
#Test 1 - Delete tasks function deletes all visible tasks
def test_tdd_delete_tasks_all_visible_tasks(taskListTwo):
    tasks = taskListTwo
    filteredTasks = tasks[0:5]
    tasks = delete_tasks(tasks, filteredTasks)
    for task in filteredTasks:
        assert task not in tasks

#Test 2 - tasks not in the filtered list do not get deleted
def test_tdd_delete_tasks_keep_invisible_tasks(taskListTwo):
    tasks = taskListTwo
    filteredTasks = tasks[0:5]
    outputTasks = delete_tasks(tasks, filteredTasks)
    for task in tasks[5:]:
        assert task in outputTasks


