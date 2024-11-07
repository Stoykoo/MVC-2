from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    # Validación en el modelo (Punto: **Validation**)
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("El título es requerido")
        return value

    @validates('due_date')
    def validate_due_date(self, key, value):
        if not value:
            raise ValueError("La fecha de vencimiento es requerida")
        if value < datetime.now():
            raise ValueError("La fecha de vencimiento no puede ser en el pasado")
        return value

    # Nota: Se ha movido la lógica de negocio al servicio (Punto: **Model**)
