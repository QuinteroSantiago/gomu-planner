from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from ..db.models import DailyTask, VariableTask

class DeleteTaskWindow(QDialog):
    task_deleted = pyqtSignal()

    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Delete Task")

        # Task selection
        self.task_combo = QComboBox()
        task_label = QLabel("Select Task:")
        task_label.setStyleSheet("color: black;")
        layout.addWidget(task_label)
        layout.addWidget(self.task_combo)
        self.update_task_combo()

        delete_button = QPushButton("Delete Task")
        delete_button.clicked.connect(self.delete_task)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def update_task_combo(self):
        self.task_combo.clear()

        # Fetch all daily tasks and variable tasks
        daily_tasks = self.config.session.query(DailyTask).all()
        variable_tasks = self.config.session.query(VariableTask).all()

        for task in daily_tasks:
            category_name = task.category.category_name if task.category else "None"
            self.task_combo.addItem(f"Daily[{category_name}]: {task.task_name}", userData=("daily", task.id))
        for task in variable_tasks:
            category_name = task.category.category_name if task.category else "None"
            self.task_combo.addItem(f"Variable[{category_name}]: {task.task_name}", userData=("variable", task.id))

    def delete_task(self):
        selected_task = self.task_combo.currentData()
        if selected_task is None:
            msg_box = QMessageBox(QMessageBox.Warning, "Error", "No task selected.")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()
            return

        task_type, task_id = selected_task
        if task_type == "daily":
            task = self.config.session.query(DailyTask).filter_by(id=task_id).first()
        elif task_type == "variable":
            task = self.config.session.query(VariableTask).filter_by(id=task_id).first()
        else:
            msg_box = QMessageBox(QMessageBox.Critical, "Error", "Invalid task type.")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()
            return

        if task:
            self.config.session.delete(task)
            self.config.session.commit()
            msg_box = QMessageBox(QMessageBox.Information, "Success", "Task deleted successfully!")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()
            self.task_deleted.emit()  # Emit the task_deleted signal
        else:
            msg_box = QMessageBox(QMessageBox.Critical, "Error", "Task not found.")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()

        self.update_task_combo()  # Refresh the task list
        self.accept()
