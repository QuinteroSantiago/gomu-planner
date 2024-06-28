from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QComboBox,
    QLabel, QLineEdit, QMessageBox, QDialog)
from datetime import datetime

class AdjustTimeWindow(QDialog):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Adjust Task Time")

        # Task selection dropdown
        self.task_combo = QComboBox()
        task_names = [task.task_name for task in self.config.variable_tasks]
        self.task_combo.addItems(task_names)
        layout.addWidget(QLabel("Select Task:"))
        layout.addWidget(self.task_combo)

        # Time input
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Enter new time (HHMM)")
        layout.addWidget(QLabel("New Time:"))
        layout.addWidget(self.time_input)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_new_time)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_new_time(self):
        task_name = self.task_combo.currentText()
        new_time = self.time_input.text()
        try:
            # Ensure input is exactly 4 digits and digits only
            if len(new_time) != 4 or not new_time.isdigit():
                raise ValueError("Please enter time in HHMM format, where HH is hour and MM is minute.")
            datetime.strptime(new_time, '%H%M')
            self.config.update_preferences(task_name, new_time)
            self.accept()
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Time", f"Invalid time format: {str(e)}")
