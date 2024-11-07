from models import db, Task

# Separación del acceso a datos usando el patrón Repository (Punto: **Database Access**)
class TaskRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_tasks(self):
        return Task.query.all()

    def get_task_by_id(self, task_id):
        return Task.query.get(task_id)

    def add_task(self, task):
        self.db_session.add(task)
        self.db_session.commit()

    def update_task(self, task):
        self.db_session.commit()

    def delete_task(self, task):
        self.db_session.delete(task)
        self.db_session.commit()
