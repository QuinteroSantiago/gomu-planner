from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QComboBox, QLabel, QLineEdit, QDialog)
from datetime import datetime
import chime

class LoggingWindow(QDialog):
    def __init__(self, style_sheet=None):
        super().__init__()
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Log Activity")

        # Activity dropdown
        self.activity_combo = QComboBox()
        activities = ['READ', 'WRKT', 'CORE', 'GOMU', 'PRCR', 'MEAL']
        self.activity_combo.addItems(activities)
        activity_label = QLabel("Select Activity:")
        activity_label.setStyleSheet("color: black;")
        layout.addWidget(activity_label)
        layout.addWidget(self.activity_combo)

        # Description input
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Describe what you did")
        description_label = QLabel("Description:")
        description_label.setStyleSheet("color: black;")
        layout.addWidget(description_label)
        layout.addWidget(self.desc_input)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_log)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_log(self):
        activity = self.activity_combo.currentText()
        description = self.desc_input.text()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} {activity} - {description}\n"
        with open("activity_log.txt", "a") as file:
            file.write(log_message)
        self.accept()
