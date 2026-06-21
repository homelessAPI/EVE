from pathlib import Path
from tabulate import tabulate
import os
import json
import uuid


BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR/"tasks.json"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_id():
    return str(uuid.uuid4())

class Database:
    def read_data():
        if not os.path.exists(FILE_PATH):
            return []
        with open(FILE_PATH, "r") as file:
            return json.load(file)
        
    def write_data(data):
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)

class DataOperations:

    def add_task():
        task_name = input("Enter the name of your task: ")
        Description = input("Enter its description: ")

        task = {"task name": task_name, "Description": Description}

        data = Database.read_data()

        if data != []:

            for i in data:
                if task["task name"] == i["task name"]:
                    print("   !! task name already exists !!   ")
                    return
                
            data.append(task)

        else:
            data.append(task)

        Database.write_data(data)
        clear()
        print("   ++ Added Successfully ++   ")
    
    def view_tasks():
        clear()

        table = []

        dataset = Database.read_data()
        for i, task in enumerate(dataset, start=1):
            table.append([
                i,
                task["task name"],
                task["Description"]
            ])
        print("\nTable Set\n")
        print(tabulate(table, headers=["ID", "NAME", "DESCRIPTION"], tablefmt="grid"))

    def update_tasks():
        task_name = input("Enter the name of your task: ")
        change_item = input("What item would you like to change from it: ")
        change_value = input("What would you like to change from it: ")

        dataset = Database.read_data()

        for i in dataset:
            if i["task name"] == task_name:
                i[change_item] = change_value

        Database.write_data(dataset)
        clear()
        print("   ++ Updated Successfully ++   ")

    def delete_tasks():
        task_name = input("Enter the name of your task: ")

        dataset = Database.read_data()
        
        dataset = [task for task in dataset if task.get("task name") != task_name]
        
        Database.write_data(dataset)
        clear()
        print("   ++ deleted Successfully ++   ")


print("""====================================
        ANIME TRACKER CLI """)

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
        
        DataOperations.add_task()
    
    elif choice == "2" or choice == "view":

        DataOperations.view_tasks()
    

    elif choice == "3" or choice == "delete":
        DataOperations.delete_tasks()

    elif choice == "4" or choice == "update":

        DataOperations.update_tasks()

    elif choice == "clear":
        clear()

    elif choice == "5" or choice == "quit":
        break

