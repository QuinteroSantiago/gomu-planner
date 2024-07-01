from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton,
                             QRadioButton, QHBoxLayout, QTimeEdit, QMessageBox, QDateEdit, QCalendarWidget)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, QDate
from datetime import datetime, time
from ..db.models import TaskCategory, Task

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
        # Task name input
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name")
        layout.addWidget(QLabel("Task Name:", styleSheet="color: black;"))
        layout.addWidget(self.task_name_input)

        # Category selection
        self.category_combo = QComboBox()
        categories = [cat.category_name for cat in self.config.session.query(TaskCategory).all()]
        self.category_combo.addItems(categories)
        layout.addWidget(QLabel("Select Category:", styleSheet="color: black;"))
        layout.addWidget(self.category_combo)

        # Frequency selection
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["Daily", "Weekly", "Monthly", "Yearly"])
        layout.addWidget(QLabel("Select Frequency:", styleSheet="color: black;"))
        layout.addWidget(self.frequency_combo)

        # Conditional inputs based on frequency
        self.frequency_combo.currentIndexChanged.connect(self.update_frequency_inputs)
        self.dynamic_inputs_layout = QVBoxLayout()
        layout.addLayout(self.dynamic_inputs_layout)
        self.update_frequency_inputs(self.frequency_combo.currentIndex())

        # Duration input
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Enter duration in minutes (1-1440)")
        self.duration_input.setValidator(QIntValidator(1, 1440, self))
        layout.addWidget(QLabel("Duration:", styleSheet="color: black;"))
        layout.addWidget(self.duration_input)


        # Start time selection
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat('HH:mm')
        layout.addWidget(QLabel("Start Time:", styleSheet="color: black;"))
        layout.addWidget(self.start_time_edit)

        # Save button
        save_button = QPushButton("Save Task")
        save_button.clicked.connect(self.save_task)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def update_frequency_inputs(self, index):
        # Clear existing widgets
        while self.dynamic_inputs_layout.count():
            child = self.dynamic_inputs_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Based on frequency, add specific input controls
        frequency = self.frequency_combo.currentText()
        if frequency == "Weekly":
            self.day_of_week_combo = QComboBox()
            self.day_of_week_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            self.dynamic_inputs_layout.addWidget(QLabel("Day of the Week:", styleSheet="color: black;"))
            self.dynamic_inputs_layout.addWidget(self.day_of_week_combo)
        elif frequency == "Monthly":
            self.day_of_month_input = QLineEdit()
            self.day_of_month_input.setPlaceholderText("Enter day of the month (1-31)")
            self.dynamic_inputs_layout.addWidget(QLabel("Day of the Month:", styleSheet="color: black;"))
            self.dynamic_inputs_layout.addWidget(self.day_of_month_input)
        elif frequency == "Yearly":
            self.date_of_year_edit = QDateEdit()
            self.date_of_year_edit.setCalendarPopup(True)
            self.date_of_year_edit.setDate(QDate.currentDate())
            self.dynamic_inputs_layout.addWidget(QLabel("Date of the Year:", styleSheet="color: black;"))
            self.dynamic_inputs_layout.addWidget(self.date_of_year_edit)

    def save_task(self):
        category_name = self.category_combo.currentText()
        category = self.config.session.query(TaskCategory).filter_by(category_name=category_name).first()
        if not category:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Category not found.")
            msg_box.setWindowTitle("Error")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()
            return
        duration = int(self.duration_input.text())
        task_name = self.task_name_input.text()
        start_time = self.start_time_edit.text().replace(':', '')
        category_id = category.id
        frequency = self.frequency_combo.currentText()

        try:
            if frequency == "Weekly":
                day_of_week = self.day_of_week_combo.currentIndex()
                Task.create(self.config.session, duration, task_name, category_id, frequency, day_of_week=day_of_week)
            elif frequency == "Monthly":
                day_of_month  = int(self.day_of_month_input.text())
                Task.create(self.config.session, duration, task_name, category_id, frequency, day_of_month=day_of_month)
            elif frequency == "Yearly":
                specific_date = self.date_of_year_edit.date().toPyDate()
                Task.create(self.config.session, duration, task_name, category_id, frequency, specific_date=specific_date)
            else:
                Task.create(self.config.session, duration, task_name, category_id, frequency)
            self.config.update_preferences(task_name, start_time)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Task added successfully!")
            msg_box.setWindowTitle("Success")
            msg_box.exec_()
            self.task_added.emit()
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText(f"Failed to add task: {str(e)}")
            msg_box.setWindowTitle("Error")
            msg_box.setStyleSheet("color: black;")
            msg_box.exec_()

        self.accept()  # Close the dialog
