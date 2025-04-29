import pytest
import datetime
import sys
import os

#TODO we are gonna have to do some weird path 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import search_tasks, load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks

#Functions tested so far..
    #Search
    #filter completion
    #filter by category
    #get overdue tasks

@pytest.fixture
def taskListOne():
    #Generate tasks which every combination of priority and category, due date (before or after current date), and completion status
    taskList = []
    taskId = 1
    for priority in ["Low", "Medium", "High"]:
        for category in ["Work", "Personal", "School", "Other"]:
            for dueDate in [datetime.datetime.now() - datetime.timedelta(days = 2), datetime.datetime.now() + datetime.timedelta(days = 2)]:
                for completionStatus in [False, True]:
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

def test_search_tasks_no_text(taskListOne):
    result = search_tasks(taskListOne, "")
    assert len(result) == len(taskListOne)

def test_search_tasks_description(taskListOne):
    result = search_tasks(taskListOne, " description 9")
    #print(taskListOne[0].get("description", ""))
    #exit()
    assert len(result) == 1
    assert result[0].get("id") == 9

def test_search_tasks_title(taskListOne):
    result = search_tasks(taskListOne, " title 8")
    assert len(result) == 1
    assert result[0].get("id") == 8

def test_filter_tasks_by_completion_completed(taskListOne):
    result = filter_tasks_by_completion(taskListOne)
    assert len(result) == 24
    assert result[0].get("id") == 2

def test_filter_tasks_by_completion_not_completed(taskListOne):
    result = filter_tasks_by_completion(taskListOne, False)
    assert len(result) == 24
    assert result[0].get("id") == 1

def test_filter_tasks_by_category(taskListOne):
    result = filter_tasks_by_category(taskListOne, "Work")
    assert len(result) == 12
    assert result[0].get("id") == 1

def test_get_overdue_tasks(taskListOne):
    result = get_overdue_tasks(taskListOne)
    assert len(result) == 12
    assert False not in [result[x].get("completed") == False for x in range(len(result))]
    assert 3 not in [result[x].get("id") for x in range(len(result))]

def test_filter_tasks_by_priority(taskListOne):
    for priority in ["Low", "Medium", "High"]:
        result = filter_tasks_by_priority(taskListOne, priority)
        assert len(result) == 16
        assert False not in [result[x].get("priority") == priority for x in range(len(result) - 1)]

def test_generate_unique_id_no_tasks():
    assert generate_unique_id([]) == 1

def test_generate_unique_id(taskListOne):
    assert generate_unique_id(taskListOne) == 49

def test_load_tasks_no_file():
    randomFileName = "random1234567890.json"
    assert randomFileName not in os.listdir()
    assert len(load_tasks(randomFileName)) == 0

def test_load_tasks_file_corrupted():
    randomFileName = "random1234567890.json"
    assert randomFileName not in os.listdir()
    g = open(randomFileName, "w")
    g.write("{'test': 1}}\n")
    g.close()
    assert len(load_tasks(randomFileName)) == 0
    os.remove(randomFileName)