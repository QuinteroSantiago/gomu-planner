from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton,
        QRadioButton, QHBoxLayout, QTimeEdit, QMessageBox)
from PyQt5.QtGui import QIntValidator
from datetime import datetime, time
from ..db.models import TaskCategory, Task
from PyQt5.QtCore import pyqtSignal

class AddTaskWindow(QDialog):
    task_added = pyqtSignal()

    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Add New Task")

        # Category selection
        self.category_combo = QComboBox()
        categories = [cat.category_name for cat in self.config.session.query(TaskCategory).all()]
        self.category_combo.addItems(categories)
        category_label = QLabel("Select Category:")
        category_label.setStyleSheet("color: black;")
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)

        # Duration input
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration in minutes (1-1440)")

        # Set up the validator
        validator = QIntValidator(1, 1440, self)  # Minimum 1 minute, maximum 1440 minutes
        self.duration_input.setValidator(validator)

        duration_label = QLabel("Duration:")
        duration_label.setStyleSheet("color: black;")
        layout.addWidget(duration_label)
        layout.addWidget(self.duration_input)

        # Task name input
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name")
        task_name_label = QLabel("Task Name:")
        task_name_label.setStyleSheet("color: black;")
        layout.addWidget(task_name_label)
        layout.addWidget(self.task_name_input)

        # Start time selection
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat('HH:mm')
        start_time_label = QLabel("Start Time:")
        start_time_label.setStyleSheet("color: black;")
        layout.addWidget(start_time_label)
        layout.addWidget(self.start_time_edit)

        # Save button
        save_button = QPushButton("Save Task")
        save_button.clicked.connect(self.save_task)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_task(self):
        category_name = self.category_combo.currentText()
        category = self.config.session.query(TaskCategory).filter_by(category_name=category_name).first()
        if not category:
            msg_box = QMessageBox(QMessageBox.Critical, "Error", "Category not found.")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()
            return
        duration = int(self.duration_input.text())
        task_name = self.task_name_input.text()
        start_time = self.start_time_edit.text().replace(':', '')
        category_id = category.id
        try:
            Task.create(self.config.session, duration, task_name, category_id)
            self.config.update_preferences(task_name, start_time)
            msg_box = QMessageBox(QMessageBox.Information, "Success", "Task added successfully!")
            msg_box.setStyleSheet("color: black;")
            self.task_added.emit()
            msg_box.exec_()
        except Exception as e:
            msg_box = QMessageBox(QMessageBox.Critical, "Error", f"Failed to add task: {str(e)}")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()

        self.accept()  # Close the dialog
