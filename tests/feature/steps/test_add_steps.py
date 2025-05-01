import pytest
import datetime
import sys
import os
from pytest_bdd import scenario, given, when, then, scenarios, parsers

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
from tasks import search_tasks, load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks

def createTask(taskId=1, title="test title", description="test description", priority="Medium", category="Work", due_date="", completed=False):
    return {
        "id": taskId,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "due_date": due_date.strftime("%Y-%m-%d") if due_date != "" else (datetime.datetime.now() + datetime.timedelta(hours=24)).strftime("%Y-%m-%d"),
        "completed": completed,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


scenarios("../add_task.feature")
scenarios("../filter_tasks_priority.feature")
scenarios("../search_tasks.feature")

@pytest.fixture
def context():
    return {'inputTasks': [], 'outputTasks': []}


@given(parsers.parse("I have a task with id {x:d}"))
def create_n_tasks(x, context):
    context['inputTasks'].append(createTask(taskId=x))

@when("I create a new task")
def add_task(context):
    context['inputTasks'].append(createTask(taskId=generate_unique_id(context['inputTasks'])))

@then(parsers.parse("The newly created task will have id {x:d}"))
def check_task_ids(context, x):
    assert x in [task['id'] for task in context['inputTasks']]



@given(parsers.parse("I have a task with {x} Priority"))
def create_task_with_priority(context, x):
    context['inputTasks'].append(createTask(priority=x))

@when(parsers.parse("I filter for {x} Priority"))
def filter_by_priority(context, x):
    context['outputTasks'] = filter_tasks_by_priority(context['inputTasks'], x)

@then(parsers.parse("I only receive tasks with {x} Priority"))
def check_task_priority(context, x):
    for task in context['outputTasks']:
        assert task['priority'] == x



@given(parsers.parse("I have a task with {x} in the title"))
def create_task_title(context, x):
    context['inputTasks'].append(createTask(title=x))

@given(parsers.parse("I have a task with {x} in the description"))
def create_task_description(context, x):
    context['inputTasks'].append(createTask(description=x))

@when(parsers.parse("I search for the string {x}"))
def filter_search(context, x):
    context['outputTasks'] = search_tasks(context['inputTasks'], x)

@then(parsers.parse("There should be {x:d} tasks output"))
def check_search_result_count(context, x):
    assert len(context['outputTasks']) == x
    