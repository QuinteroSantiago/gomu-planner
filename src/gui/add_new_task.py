from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton,
        QRadioButton, QHBoxLayout, QTimeEdit, QMessageBox)
from PyQt5.QtGui import QIntValidator
from datetime import time
from ..db.models import DailyTask, TaskCategory, VariableTask

class AddTaskWindow(QDialog):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Add New Task")

        # Category selection
        self.category_combo = QComboBox()
        categories = [cat.category_name for cat in self.config.session.query(TaskCategory).all()]
        self.category_combo.addItems(categories)
        category_label = QLabel("Select Category:")
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)

        # Duration input
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration in minutes (1-1440)")

        # Set up the validator
        validator = QIntValidator(1, 1440, self)  # Minimum 1 minute, maximum 1440 minutes
        self.duration_input.setValidator(validator)

        duration_label = QLabel("Duration:")
        layout.addWidget(duration_label)
        layout.addWidget(self.duration_input)

        # Task name input
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name")
        task_name_label = QLabel("Task Name:")
        layout.addWidget(task_name_label)
        layout.addWidget(self.task_name_input)

        # Task type selection
        self.daily_task_radio = QRadioButton("Daily Task")
        self.variable_task_radio = QRadioButton("Variable Task")
        task_type_label = QLabel("Task Type:")
        layout.addWidget(task_type_label)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.daily_task_radio)
        radio_layout.addWidget(self.variable_task_radio)
        layout.addLayout(radio_layout)
        self.daily_task_radio.setChecked(True)  # Default selection

        # Start time selection
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat('HH:mm')
        start_time_label = QLabel("Start Time:")
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
            QMessageBox.critical(self, "Error", "Category not found.")
            return
        duration = int(self.duration_input.text())
        task_name = self.task_name_input.text()
        start_time = self.start_time_edit.time().toString('HH:mm:ss')
        start_time = time.fromisoformat(start_time)
        category_id = category.id
        if self.daily_task_radio.isChecked():
            try:
                DailyTask.create(self.config.session, start_time, duration, task_name, category_id)
                QMessageBox.information(self, "Success", "Daily task added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add daily task: {str(e)}")
        else:
            try:
                VariableTask.create(self.config.session, duration, task_name, category_id)
                QMessageBox.information(self, "Success", "Variable task added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add variable task: {str(e)}")

        self.accept()  # Close the dialog
