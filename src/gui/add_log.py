from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QComboBox, QLabel, QLineEdit, QDialog)
from datetime import datetime
from ..db.models import TaskCategory

class LoggingWindow(QDialog):
    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Log Activity")

        # Activity dropdown
        self.activity_combo = QComboBox()
        self.populate_activities()
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

    def populate_activities(self):
        activities = self.config.session.query(TaskCategory).all()
        for activity in activities:
            self.activity_combo.addItem(activity.category_name)

    def save_log(self):
        activity = self.activity_combo.currentText()
        description = self.desc_input.text()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} {activity} - {description}\n"
        with open("activity_log.txt", "a") as file:
            file.write(log_message)
        self.accept()
