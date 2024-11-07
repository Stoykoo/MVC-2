from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, Task
from task_service import TaskService
from task_repository import TaskRepository

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, ValidationError

# Configuración del logging (Punto: **Error Handling**)
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'A3jR9KpL2vX7WqZ8sB6N1yP4'  # Necesario para WTForms
db.init_app(app)

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inyección de dependencias (Punto: **Dependencies**)
with app.app_context():
    task_repository = TaskRepository(db.session)
    task_service = TaskService(task_repository)

# Formulario con validación (Punto: **Validation**)
class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    due_date = DateField('Fecha de Vencimiento', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Añadir Tarea')

    def validate_due_date(form, field):
        if field.data < datetime.now().date():
            raise ValidationError('La fecha de vencimiento no puede ser en el pasado')

@app.route('/tasks', methods=['GET', 'POST'])
def task_list():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        due_date = form.due_date.data
        try:
            task_service.create_task(title, due_date)
            return redirect(url_for('task_list'))  # Uso de URL helpers (Punto: **Routing**)
        except Exception as e:
            logger.error(f"Error creando tarea: {e}")  # Logging de errores (Punto: **Error Handling**)
            return "Error al crear la tarea", 500
    else:
        if request.method == 'POST':
            logger.warning(f"Validación fallida: {form.errors}")
    try:
        tasks = task_service.get_all_tasks()
        for task in tasks:
            # Lógica de negocio movida del template al controlador (Punto: **View**)
            if task.completed:
                task.status = "Completada"
            elif task.due_date < datetime.now():
                task.status = "Vencida"
            else:
                task.status = "Pendiente"
        return render_template('task_view.html', tasks=tasks, form=form)
    except Exception as e:
        logger.error(f"Error obteniendo tareas: {e}")
        return "Error al obtener las tareas", 500

@app.route('/tasks/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    try:
        task = task_service.complete_task(task_id)
        if not task:
            return "Tarea no encontrada", 404
        return redirect(url_for('task_list'))  # Uso de URL helpers (Punto: **Routing**)
    except Exception as e:
        logger.error(f"Error completando tarea {task_id}: {e}")  # Logging de errores (Punto: **Error Handling**)
        return "Error al completar la tarea", 500
