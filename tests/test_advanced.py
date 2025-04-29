import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import search_tasks, load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks
import datetime

def mock_file_open():
    #according to the python docs, these have to be impled. ill just have them all do nothing and hope it works
    def __enter__(self):
        return "File"

    def __exit__(self, a, b, c):
        pass


@pytest.fixture
def singleTask():
    return [{
    "id": 1,
    "title": f"test title",
    "description": f"test description",
    "priority": "High",
    "category": "Work",
    "due_date": datetime.datetime.now().strftime("%Y-%m-%d"),
    "completed": False,
    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]

@pytest.mark.parametrize("highestAccountNum", (0, 4, 12, 77))
def test_generate_unique_id(highestAccountNum, singleTask):
    task = dict(singleTask[0])
    task['id'] = int(highestAccountNum)
    assert generate_unique_id([task]) == int(highestAccountNum) + 1


def test_load_tasks(mocker, singleTask):
    mock_file_open = mocker.patch("builtins.open", mocker.mock_open(read_data="Test"))
    mock_json_load = mocker.patch("json.load", return_value=singleTask)
    result = load_tasks("testFile.json")
    assert len(result) == 1
    assert result[0]['id'] == 1
    mock_file_open.assert_called_once_with("testFile.json", "r")


def test_load_tasks_invalid_data(mocker, singleTask):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="Test"))
    taskKeys = list(singleTask[0].keys())
    singleTask[0]['placeholder'] = "placeholder"
    for x in range(len(taskKeys)):
        taskCopy = dict(singleTask[0])
        del taskCopy[taskKeys[x]]
        mock_json_load = mocker.patch("json.load", return_value=[taskCopy])
        result = load_tasks("testFile.json")
        print(result)
        assert result == []

