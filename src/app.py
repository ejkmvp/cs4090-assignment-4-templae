import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, get_overdue_tasks, order_tasks
import subprocess
import os

@st.dialog("Test Runner")
def run_command(command):
    with st.spinner("Running Tests"):
        currentDirectory = os.getcwd() #store current directory so we can go back after running test. I feel like this is necessary because we dont want to start writing our tasks.json to other dirs
        os.chdir("../")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.code(result.stdout + result.stderr, language='bash')
        if result.returncode == 0:
            st.success("Tests Passed!")
        else:
            st.error("Tests Failed!")
        os.chdir(currentDirectory)

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title and task_due_date and task_due_date >= datetime.now().date():
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    st.sidebar.button("Run Tasks.py Basic Unit Tests", on_click=run_command, args=["pytest tests/test_basic.py"])
    st.sidebar.button("Run Mocked Loading Tests", on_click=run_command, args=["pytest tests/test_advanced.py"]) #TODO Specifically sleect the mock test
    st.sidebar.button("Run Parametrizeed ID Generation Test", on_click=run_command, args=["pytest tests/test_advanced.py"]) #TODO Specifically sleect the param test
    st.sidebar.button("Get Coverage Report", on_click=run_command, args=["pytest --cov=src tests/"])
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col3:
        filter_overdue = st.selectbox("Filter by Due", ["All", "Overdue", "Not Overdue"])
    order_type = st.radio("Order By...", ["Priority", "Due Date", "Category"])
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    filtered_tasks = get_overdue_tasks(filtered_tasks, filter_overdue)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # TODO Apply Ordering
    ordered_tasks = order_tasks(filtered_tasks, order_type)

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

if __name__ == "__main__":
    main()