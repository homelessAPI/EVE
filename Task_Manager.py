from pathlib import Path
from tabulate import tabulate
import os
import json

BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "tasks.json"

FIELD_NAME = "name"
FIELD_DESCRIPTION = "description"
FIELD_STATUS = "status"
DEFAULT_STATUS = "Incomplete"

LEGACY_FIELD_KEYS = {
    "task name": FIELD_NAME,
    "Description": FIELD_DESCRIPTION,
    "Status": FIELD_STATUS,
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def normalize_task(task):
    if FIELD_NAME in task:
        return task

    return {
        new_key: task[old_key]
        for old_key, new_key in LEGACY_FIELD_KEYS.items()
        if old_key in task
    }


def normalize_name(name):
    return name.strip()


def task_name_exists(tasks, name):
    normalized_name = normalize_name(name).lower()
    return any(
        normalize_name(task[FIELD_NAME]).lower() == normalized_name
        for task in tasks
    )


class TaskStorage:
    @staticmethod
    def load_tasks():
        if not TASKS_FILE.exists():
            return []

        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)

        return [normalize_task(task) for task in tasks]

    @staticmethod
    def save_tasks(tasks):
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file, indent=4)


class TaskManager:
    @staticmethod
    def add_task():
        name = normalize_name(input("Enter the name of your task: "))
        if not name:
            print("   !! task name cannot be empty !!   ")
            return

        tasks = TaskStorage.load_tasks()

        if task_name_exists(tasks, name):
            print("   !! task name already exists !!   ")
            return

        description = input("Enter its description: ")

        task = {
            FIELD_NAME: name,
            FIELD_DESCRIPTION: description,
            FIELD_STATUS: DEFAULT_STATUS,
        }

        tasks.append(task)
        TaskStorage.save_tasks(tasks)
        clear_screen()
        print("   ++ Added Successfully ++   ")

    @staticmethod
    def view_tasks():
        clear_screen()

        rows = []
        tasks = TaskStorage.load_tasks()

        for index, task in enumerate(tasks, start=1):
            rows.append([
                index,
                task[FIELD_NAME],
                task[FIELD_DESCRIPTION],
                task[FIELD_STATUS],
            ])
        print("\nTask List\n")
        print(tabulate(rows, headers=["ID", "NAME", "DESCRIPTION", "STATUS"], tablefmt="grid"))

    @staticmethod
    def update_task():
        name = input("Enter the name of your task: ")
        field = input("What field would you like to change (name, description, status): ")
        new_value = input("Enter the new value: ")

        tasks = TaskStorage.load_tasks()

        for task in tasks:
            if task[FIELD_NAME] == name:
                task[field] = new_value

        TaskStorage.save_tasks(tasks)
        clear_screen()
        print("   ++ Updated Successfully ++   ")

    @staticmethod
    def delete_task(delete_mode):
        tasks = TaskStorage.load_tasks()

        if delete_mode == "one":
            name = input("Enter the name of your task: ")
            tasks = [task for task in tasks if task[FIELD_NAME] != name]

            TaskStorage.save_tasks(tasks)
            clear_screen()
            print("   ++ Deleted Successfully ++   ")

        elif delete_mode == "all":
            tasks.clear()
            TaskStorage.save_tasks(tasks)
            clear_screen()
            print("   ++ All Tasks Deleted Successfully ++   ")


print("""====================================
        TASK MANAGER CLI """)

while True:
    print("""
====================================
1. Add task
2. View task List
3. Delete task
4. Update task
5. Exit
====================================
""")

    choice = input("Enter command or the number corresponding to the task: ")

    if choice == "1" or choice == "add":
        TaskManager.add_task()

    elif choice == "2" or choice == "view":
        TaskManager.view_tasks()

    elif choice == "3" or choice.startswith("delete"):
        if choice == "3" or choice == "delete":
            TaskManager.delete_task("one")

        elif choice == "delete -all":
            TaskManager.delete_task("all")

    elif choice == "4" or choice == "update":
        TaskManager.update_task()

    elif choice == "clear":
        clear_screen()

    elif choice == "5" or choice == "quit":
        break
