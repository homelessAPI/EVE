from pathlib import Path
import os
import json
import uuid

db = []

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR/"tasks.json"

def add_task(task):
    data = read_data()

    data.append(task)
    db.append(task)

    write_data(data)

def read_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as file:
        return json.load(file)
    
def write_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

def generate_id():
    return str(uuid.uuid4())

while True:
    print("1) Add task")
    print("2) view tasks")
    print("3) delete tasks")
    print("3) update tasks")
    print("5) exit")

    choice = input("Enter command or the number corresponding to the task: ")

    if choice == "1":
        task_name = input("enter task name: ")
        description = input("enter task description: ")

        task = {"ID": generate_id(), "task_name": task_name, "description": description}

        add_task(task)
        print("\n******************")
        print("Successful")
        print("******************\n")
    
    elif choice == "2":
        print("\n******************")
        data = read_data()
        if data:
            for i in data:
                print(i)
                print("******************\n")
                
        else:
            print("empty")
            print("******************\n")

    elif choice == "3":
        data = read_data()
        task_name = input("Enter task name: ")

        for i in data:
            if i["task_name"] == task_name:
                removable = i
                data.remove(removable)
                write_data(data)

    elif choice == "4":
        task_name = input("Enter task number: ")

        

            
    elif choice == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')

    elif choice == "5":
        break
