import csv
from typing import List, Dict
from datetime import datetime as dt
from datetime import timedelta as td
from copy import deepcopy
import colored
from colored import stylize
import os
# undergradinfo@math.oregonstate.edu 

class Database:
    def __init__(self):
        self.mem_db: List[Dict] = []
        self.DB_FILE = 'data/tasks.csv'
        self.DT_FORMAT = "%Y-%m-%d %H:%M:%S"

        try:
            with open(self.DB_FILE, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                labels = rows.pop(0)

                for row in rows:
                    self.mem_db.append(dict())
                    for i, box in enumerate(row):
                        try:
                            self.mem_db[-1][labels[i]] = self.get_dt_from_str(box)
                        except ValueError:
                            self.mem_db[-1][labels[i]] = box
            
            print(f"Imported {len(self.mem_db)} tasks from", self.DB_FILE)
        except FileNotFoundError:
            raise FileNotFoundError(f"The provided database path ({self.DB_FILE}) does not exist.")

    def get_task(self, task_id: int) -> Dict:
        try:
            return self.mem_db[task_id]
        except IndexError:
            print("(Warning!) That task does not exist, returning none.")
            return None

    def get_raw_db(self) -> List[Dict]:
        return self.mem_db
    
    def add_task(self, task: Dict) -> None:
        self.mem_db.append(task)

        with open(self.DB_FILE, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(task.values())
    
    def remove_task(self, index : int):
        self.mem_db.pop(index)

        with open(self.DB_FILE, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i, line in enumerate(d):
                if i != index+1:
                    f.write(line)
            f.truncate()
    
    def get_dt_from_str(self, str_to_decode : str) -> dt:
        return dt.strptime(str_to_decode, self.DT_FORMAT)
    
    def get_str_from_dt(self, dt_to_encode : dt) -> str:
        return dt.strftime(dt_to_encode, self.DT_FORMAT)

def get_date_from_input(str_date : str) -> dt:
    # offset
    if str_date[-1] != "m" and str_date[-1] != "d":
        idate = dt(dt.now().year, dt.now().month, dt.now().day, 23, 59, 59, 0) + td(int(str_date))
        
        return idate
    elif str_date[-1] == "d":
        idate = dt(dt.now().year, dt.now().month, int(str_date[:-1]), 23, 59, 59, 0)

        if idate < dt.now():
            idate = dt(dt.now().year, dt.now().month+1, int(str_date[:-1]), 23, 59, 59, 0)
        return idate
    elif str_date[-1] == "m":
        parts = str_date.split("d")

        idate = dt(dt.now().year, dt.now().month + int(parts[1][:-1]), int(parts[0]), 23, 59, 59, 0)

        return idate
    
    return None
    
def add_task(db : Database) -> None:
    print("Format: <task name (req)>/<days until due date (not req)>/<priority (defaults to 2)>/<time to complete (defaults to 0.5)>/<desc (not req)>")
    task_str = input("Enter task here: ")
    if task_str == "help":
        print("Leave a section blank to not include it.")
        print("Type CANCEL or C or EXIT or E to cancel adding the task.")
        print("Type d after the number of days to signal that you are specifying a date instead of an offset of days.")
        print("A number and then a d means that day of the current month, unless that date is in the past.")
        print("If it is in the past the next month is assumed. Skip forward months by typing another number and an m: 10d1m")
        print("That above example would set the due date for the tenth of next month.")

        print()
        add_task(db)
        return
    elif task_str.lower() == "cancel" or task_str.lower() == "c" or task_str.lower() == "exit" or task_str.lower() == "e":
        return
    
    try:
        parts = task_str.split("/")
        print(parts)
        task = {}
        if len(parts) == 1:
            task["Name"] = parts[0]
            task["Due date"] = "None"
            task["Priority"] = "2"
            task["Time"] = "0.5"
            task["Description"] = "None"

            db.add_task(task)
        elif len(parts) == 2:
            task["Name"] = parts[0]
            task["Due date"] = get_date_from_input(parts[1])
            task["Description"] = "None"
            task["Priority"] = "2"
            task["Time"] = "0.5"

            db.add_task(task)
        elif len(parts) == 3:
            task["Name"] = parts[0]
            task["Due date"] = get_date_from_input(parts[1])
            task["Description"] = "None"
            task["Priority"] = parts[2]
            task["Time"] = "0.5"

            db.add_task(task)
        elif len(parts) == 4:
            task["Name"] = parts[0]
            task["Due date"] = get_date_from_input(parts[1])
            task["Description"] = "None"
            task["Priority"] = parts[2]
            task["Time"] = parts[3]

            db.add_task(task)
        elif len(parts) == 5:
            task["Name"] = parts[0]
            task["Due date"] = get_date_from_input(parts[1])
            task["Description"] = "None"
            task["Priority"] = parts[2]
            task["Time"] = parts[3]

            db.add_task(task)
    except:
        print("Could not parse input, try again.")
        add_task(db)

def get_ordered_tasks(db : Database, mode : int = 0) -> List[Dict]:
    if mode == 0:
        tasks_to_print = deepcopy(db.get_raw_db())

        while(True):
            swaps = 0
            for i in range(len(tasks_to_print)-1):
                if tasks_to_print[i]["Due date"] == "None" and tasks_to_print[i+1]["Due date"] != "None":
                    tasks_to_print[i], tasks_to_print[i+1] = tasks_to_print[i+1], tasks_to_print[i]
                    swaps += 1
                elif tasks_to_print[i]["Due date"] == "None" and tasks_to_print[i+1]["Due date"] == "None":
                    continue
                elif tasks_to_print[i]["Due date"] > tasks_to_print[i+1]["Due date"]:
                    tasks_to_print[i], tasks_to_print[i+1] = tasks_to_print[i+1], tasks_to_print[i]
                    swaps += 1
                elif tasks_to_print[i]["Due date"] == tasks_to_print[i+1]["Due date"] and tasks_to_print[i]["Priority"] < tasks_to_print[i+1]["Priority"]:
                    tasks_to_print[i], tasks_to_print[i+1] = tasks_to_print[i+1], tasks_to_print[i]
                    swaps += 1
            
            if swaps == 0:
                break
    
    return tasks_to_print

def view_tasks(db : Database, mode : int = 0):
    tasks_to_print = get_ordered_tasks(db, mode)
        
    for task in tasks_to_print:
        print(task)

def remove_tasks(db : Database):
    task_name = input("Enter task name to remove (accepts partial name): ")
    task_name = task_name.lower()

    if task_name == "exit" or task_name == "cancel" or task_name == "e" or task_name == "c":
        return
    
    valid_matches = []
    for index, task in enumerate(db.get_raw_db()):
        if task_name in task["Name"]:
            valid_matches.append(index)
    
    if len(valid_matches) > 1:
        print("Please specify which task you meant:")

        for i in range(len(valid_matches)):
            print(f"{i+1} - {db.get_task(valid_matches[i])['Name']}")
        
        while True:
            try:
                num = int(input("Enter the number here: ")) - 1
                if num < 1 or num > len(valid_matches):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input, try again.")
                continue
        
        db.remove_task(valid_matches[num])
    elif len(valid_matches) == 0:
        print("Hmmm, there is no task that matches that name. Reenter below.")
        remove_tasks(db)
        return
    elif len(valid_matches) == 1:
        db.remove_task(valid_matches[0])

    print(f"Successfully removed task.")

def get_due_tonight(tasks : List[Dict]):
    due_tonight = []

    for task in tasks:
        try:
            if task["Due date"].day == dt.now().day:
                due_tonight.append(task)
            else:
                break
        except AttributeError:
            break

    return due_tonight

def cprint(text : str, color : str = "white"):
    print(stylize(text, colored.fg(color)))

def view_dashboard(db):
    tasks = get_ordered_tasks(db)
    tasks = tasks[:8]
    due_tonight = get_due_tonight(tasks)
    tasks = tasks[len(due_tonight):]

    print("     === Dashboard ===")
    if len(due_tonight) != 0:
        total_hours = 0.0
        skippable = 0.0
        cprint("--Due Tonight", "red")
        for task in due_tonight:
            print(f"Task: {task['Name']}")

            if int(task['Priority']) == 1:
                res = colored.attr('reset')
                col = colored.fg('green')
            elif int(task['Priority']) == 2:
                res = colored.attr('reset')
                col = colored.fg('yellow')
            elif int(task['Priority']) == 3:
                res = colored.attr('reset')
                col = colored.fg('red')

            print(f"Priority: {col}Level {task['Priority']}{res}")
            print(f"Estimated length: {task['Time']} hours")
            if task['Description'] != "None":
                print(f"Desc: {task['Description']}")
            print()

            if int(task['Priority']) > 1:
                total_hours += float(task['Time'])
            else:
                skippable += float(task['Time'])
                total_hours += float(task['Time'])
    
        if total_hours <= 1:
            cprint(f"Total hours of work tonight: {total_hours}", "green")
        elif total_hours <= 2.5:
            cprint(f"Total hours of work tonight: {total_hours}", "yellow")
        elif total_hours > 2.5:
            cprint(f"Total hours of work tonight: {total_hours}", "red")
        
        if total_hours - skippable <= 1:
            cprint(f"It's possible to cut that down to {total_hours - skippable} hours by skipping lower priority tasks.", "green")
        elif total_hours - skippable <= 2.5:
            cprint(f"It's possible to cut that down to {total_hours - skippable} hours by skipping lower priority tasks.", "yellow")
        elif total_hours - skippable > 2.5:
            cprint(f"It's possible to cut that down to {total_hours - skippable} hours by skipping lower priority tasks.", "red")

        print()

    if len(tasks) != 0:
        cprint("--Due Later--", "green")
        for task in tasks:
            print(f"Task: {task['Name']}")
            date_str = dt.strftime(task['Due date'], "%B %-d")
            print(f"Due: {date_str} at midnight")

            if int(task['Priority']) == 1:
                res = colored.attr('reset')
                col = colored.fg('green')
            elif int(task['Priority']) == 2:
                res = colored.attr('reset')
                col = colored.fg('yellow')
            elif int(task['Priority']) == 3:
                res = colored.attr('reset')
                col = colored.fg('red')

            print(f"Priority: {col}Level {task['Priority']}{res}")
            print(f"Estimated length: {task['Time']} hours")
            if task['Description'] != "None":
                print(f"Desc: {task['Description']}")
            print()
    
    if len(tasks) == 0 and len(due_tonight) == 0:
        print("There are no tasks to display!")
        print()
        
# Priority Scale:
# 1 - Possible to skip without impact to grade
# 2 - Should do it to avoid minor grade impact
# 3 - This assignment will have a large impact on the final grade

if __name__ == '__main__':
    db = Database()
    while True:
        os.system('clear')
        view_dashboard(db)
        print("1 - add task")
        print("2 - remove task")

        try:
            choice = int(input("> "))

            if choice == 1:
                add_task(db)
            elif choice == 2:
                remove_tasks(db)
            
            raise ValueError
        except ValueError:
            continue
