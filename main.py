import csv
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime as dt

class Database:
    def __init__(self):
        self.mem_db: List[Dict] = []
        self.DB_FILE = 'data/tasks.csv'
        self.DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

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
        return self.mem_db[task_id]
    
    def add_task(self, task: Dict) -> None:
        self.mem_db.append(task)

        with open(self.DB_FILE, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(task.values())
    
    def get_dt_from_str(self, str_to_decode : str) -> dt:
        return dt.strptime(str_to_decode, self.DT_FORMAT)
    
    def get_str_from_dt(self, dt_to_encode : dt) -> str:
        return dt.strftime(dt_to_encode, self.DT_FORMAT)

if __name__ == '__main__':
    db = Database()
    task = db.get_task(0)
    print(task["Due date"])