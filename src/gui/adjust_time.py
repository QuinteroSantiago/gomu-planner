from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QComboBox,
    QLabel, QTimeEdit, QMessageBox, QDialog, QRadioButton, QGroupBox)
from datetime import datetime
from PyQt5.QtCore import QTime
import sys
from ..db.models import Task

class AdjustTimeWindow(QDialog):
    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        self.no_tasks = self.check_no_tasks()  # Initial check for tasks
        layout = QVBoxLayout()
        if self.no_tasks:
            # Display the error message and set up a basic layout for the message
            self.setWindowTitle("No Tasks to Adjust")
            task_label = QLabel("No tasks to adjust.")
            task_label.setStyleSheet("color: black;")
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.close)  # Connect the Close button to close the dialog
            layout.addWidget(task_label)
            layout.addWidget(close_button)
            self.setLayout(layout)
            return

        self.setWindowTitle("Adjust Task Time")

        # Task selection dropdown
        self.task_combo = QComboBox()
        task_names = [task.task_name for task in self.config.tasks]
        self.task_combo.addItems(task_names)
        task_label = QLabel("Select Task:")
        task_label.setStyleSheet("color: black;")
        layout.addWidget(task_label)
        layout.addWidget(self.task_combo)

        # Radio buttons for choosing adjustment type
        self.radio_group_box = QGroupBox("Adjustment Type")
        self.radio_layout = QVBoxLayout()

        self.radio_time = QRadioButton("Adjust Start Time")
        self.radio_frequency = QRadioButton("Change Frequency")
        self.radio_specific_day = QRadioButton("Set Specific Day")

        self.radio_time.setChecked(True)  # Default selection

        self.radio_layout.addWidget(self.radio_time)
        self.radio_layout.addWidget(self.radio_frequency)
        self.radio_layout.addWidget(self.radio_specific_day)
        self.radio_group_box.setLayout(self.radio_layout)

        layout.addWidget(self.radio_group_box)

        # Input field for new time or new parameters based on radio selection
        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        self.time_label = QLabel("New Start Time:")
        self.time_label.setStyleSheet("color: black;")
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_input)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_new_time)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def check_no_tasks(self):
        # Check if there are any tasks available for deletion
        tasks = self.config.session.query(Task).all()
        return len(tasks) == 0

    def save_new_time(self):
        task_name = self.task_combo.currentText()
        task = self.config.session.query(Task).filter_by(task_name=task_name).first()

        if not task:
            QMessageBox.critical(self, "Error", "Task not found.")
            return

        try:
            if self.radio_time.isChecked():
                new_time_str = self.time_input.text()
                new_time = QTime.fromString(new_time_str, "HH:mm").toPyTime()
                task.preferences[task_name] = new_time  # Assuming 'preferences' dict holds times
            elif self.radio_frequency.isChecked():
                new_frequency = self.time_input.text()  # Example input could be "weekly"
                task.frequency = new_frequency
            elif self.radio_specific_day.isChecked():
                # Convert day name to number: Monday = 0, Sunday = 6
                day_str = self.time_input.text()
                day_number = datetime.strptime(day_str, '%A').weekday()
                task.specific_day = day_number

            self.config.session.commit()
            QMessageBox.information(self, "Success", "Task updated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update task: {str(e)}")
            sys.stderr.write(f"Error: {str(e)}\n")
