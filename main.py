import csv
from typing import List, Dict

class Database:
    def __init__(self):
        self.mem_db: List[Dict] = []

        with open('data/tasks.csv', 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            labels = rows.pop(0)

            for row in rows:
                self.mem_db.append(dict())
                for i, box in enumerate(row):
                    self.mem_db[-1][labels[i]] = box

    def get_task(self, task_id: int) -> Dict:
        return self.mem_db[task_id]
    
    def add_task(self, task: Dict):
        self.mem_db.append(task)

        with open('data/tasks.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(task.values())

if __name__ == '__main__':
    db = Database()
    db.get_task(0)
    db.add_task({'Name': 'demo', 'Description': 'demo', 'Due Date': '2020-01-01'})
