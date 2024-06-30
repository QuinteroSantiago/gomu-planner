from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QComboBox,
    QLabel, QTimeEdit, QMessageBox, QDialog)
from datetime import datetime

class AdjustTimeWindow(QDialog):
    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Adjust Task Time")

        # Task selection dropdown
        self.task_combo = QComboBox()
        task_names = [task.task_name for task in self.config.tasks]
        self.task_combo.addItems(task_names)
        task_label = QLabel("Select Task:")
        task_label.setStyleSheet("color: black;")
        layout.addWidget(task_label)
        layout.addWidget(self.task_combo)

        # Time input
        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        time_label = QLabel("New Start Time:")
        time_label.setStyleSheet("color: black;")
        layout.addWidget(time_label)
        layout.addWidget(self.time_input)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_new_time)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_new_time(self):
        task_name = self.task_combo.currentText()
        new_time = self.time_input.text().replace(':', '')
        try:
            # Ensure input is exactly 4 digits and digits only
            if len(new_time) != 4 or not new_time.isdigit():
                raise ValueError("Please enter time in HHMM format, where HH is hour and MM is minute.")
            self.config.update_preferences(task_name, new_time)
            self.accept()
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Time", f"Invalid time format: {str(e)}")
