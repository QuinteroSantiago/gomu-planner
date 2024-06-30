from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ..db.models import Task

class DeleteTaskWindow(QDialog):
    task_deleted = pyqtSignal()

    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        self.no_tasks = self.check_no_tasks()  # Initial check for tasks
        layout = QVBoxLayout()
        self.setLayout(layout)
        if self.no_tasks:
            # Display the error message and set up a basic layout for the message
            self.setWindowTitle("No Tasks to Delete")
            task_label = QLabel("No Tasks to delete.")
            task_label.setStyleSheet("color: black;")
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.close)  # Connect the Close button to close the dialog
            layout.addWidget(task_label)
            layout.addWidget(close_button)
            return

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

    def check_no_tasks(self):
        # Check if there are any tasks available for deletion
        tasks = self.config.session.query(Task).all()
        return len(tasks) == 0

    def update_task_combo(self):
        self.task_combo.clear()
        tasks = self.config.session.query(Task).all()

        for task in tasks:
            category_name = task.category.category_name if task.category else "None"
            self.task_combo.addItem(f"Task [{category_name}]: {task.task_name}", userData=("variable", task.id))

    def delete_task(self):
        selected_task = self.task_combo.currentData()[1]
        if selected_task is None:
            msg_box = QMessageBox(QMessageBox.Warning, "Error", "No task selected.")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()
            return
        task_id = selected_task
        if task_id:
            task = self.config.session.query(Task).filter_by(id=task_id).first()
            if task:
                self.config.session.delete(task)
                self.config.session.commit()
                msg_box = QMessageBox(QMessageBox.Information, "Success", "Task deleted successfully!")
                msg_box.setStyleSheet("color: black;")
                self.task_deleted.emit()
                msg_box.exec_()
                self.update_task_combo()  # Refresh the task list
                self.accept()
            else:
                msg_box = QMessageBox(QMessageBox.Critical, "Error", "Task not found.")
                msg_box.setStyleSheet("color: black;")
                msg_box.exec_()
