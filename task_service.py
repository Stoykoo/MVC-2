from datetime import datetime
from models import Task

# Implementación de la lógica de negocio en el servicio (Punto: **Model**, **Controller**)
class TaskService:
    def __init__(self, task_repository):
        self.task_repository = task_repository

    def create_task(self, title, due_date):
        # Lógica de negocio
        task = Task(title=title, due_date=due_date)
        self.task_repository.add_task(task)
        return task

    def get_all_tasks(self):
        return self.task_repository.get_all_tasks()

    def get_task_by_id(self, task_id):
        return self.task_repository.get_task_by_id(task_id)

    def complete_task(self, task_id):
        task = self.task_repository.get_task_by_id(task_id)
        if not task:
            return None
        task.completed = True
        self.task_repository.update_task(task)
        return task

    def get_overdue_tasks(self):
        now = datetime.now()
        return Task.query.filter(Task.due_date < now, Task.completed == False).all()
