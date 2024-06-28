from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
    QTextEdit, QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from datetime import datetime, date
from .schedule import create_schedule
import chime
import os
from .gui.adjust_time import AdjustTimeWindow
from .gui.logging import LoggingWindow
from .gui.view_logs import ViewLogsWindow

class MainApp(QMainWindow):
    def __init__(self, config):
        super().__init__()
        chime.theme('pokemon')
        self.config = config
        self.setWindowTitle("Gomu Planner")
        self.setGeometry(100, 100, 800, 600)
        self.load_styles()
        QApplication.setFont(QFont("Courier New", 12))
        self.current_active_task = None
        self.init_ui()

    def load_styles(self):
        # Navigate to the root directory where styles.css is located
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(repo_dir)  # Navigate one directory up if gui.py is not in the root
        style_sheet_path = os.path.join(root_dir, 'styles.css')

        try:
            with open(style_sheet_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Stylesheet not found. Using default styles.")

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Date display
        today = date.today().strftime("%A, %B %d, %Y")
        self.header_label = QLabel(today)
        layout.addWidget(self.header_label)

        # Schedule display area
        self.schedule_display = QTextEdit(self)
        self.schedule_display.setReadOnly(True)
        layout.addWidget(self.schedule_display)

        # Buttons
        self.adjust_button = QPushButton("Adjust Task Time", self)
        self.adjust_button.clicked.connect(self.adjust_time_window)
        layout.addWidget(self.adjust_button)

        self.log_button = QPushButton("Log Activity Now", self)
        self.log_button.clicked.connect(self.logging_window)
        layout.addWidget(self.log_button)

        self.view_logs_button = QPushButton("View Logs", self)
        self.view_logs_button.clicked.connect(self.view_logs)
        layout.addWidget(self.view_logs_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        central_widget.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_schedule)
        self.timer.start(1000)  # Update every second

        self.update_schedule()

    def update_schedule(self):
        now = datetime.now()
        if now.second % 2 == 0:
            current_time = now.strftime("%H:%M")
        else:
            current_time = now.strftime("%H %M")

        self.schedule_display.clear()
        self.schedule_display.append(f"<div style='text-align:left;'>{current_time}\n\n</div>\n\n")

        day_of_week = datetime.today().weekday()
        schedule = create_schedule(self.config.daily_tasks, self.config.variable_tasks,
                                self.config.conditional_tasks, day_of_week, self.config.preferences)

        new_current_task = None
        for start_dt, end_dt, task_name in schedule:
            start_time_str = start_dt.strftime('%H:%M')
            if start_dt <= now < end_dt:
                color = "green"  # Current task
                new_current_task = task_name
            elif end_dt < now:
                color = "red"    # Past task
            else:
                color = "white"   # Future task
            self.schedule_display.append(f"<div style='color:{color};'>{start_time_str} - {task_name}</div>")

        # Check if the active task has changed and play a chime if it has
        if new_current_task != self.current_active_task and new_current_task is not None:
            chime.success()
            self.current_active_task = new_current_task

    def adjust_time_window(self):
        dialog = AdjustTimeWindow(self.config)
        dialog.exec_()
        self.update_schedule()

    def logging_window(self):
        log_win = LoggingWindow()
        log_win.exec_()

    def view_logs(self):
        log_window = ViewLogsWindow(self.styleSheet())
        log_window.exec_()

def run_gui(config):
    app = QApplication([])
    window = MainApp(config)
    window.show()
    app.exec_()


# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton

# class AdjustTimeWindow(QDialog):
#     def __init__(self, config):
#         super().__init__()
#         self.config = config
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()
#         self.setWindowTitle("Adjust Task Time")

#         # Task selection dropdown
#         self.task_combo = QComboBox()
#         task_names = [task.task_name for task in self.config.variable_tasks]
#         self.task_combo.addItems(task_names)
#         layout.addWidget(QLabel("Select Task:"))
#         layout.addWidget(self.task_combo)

#         # Time input
#         self.time_input = QLineEdit()
#         self.time_input.setPlaceholderText("Enter new time (HHMM)")
#         layout.addWidget(QLabel("New Time:"))
#         layout.addWidget(self.time_input)

#         # Save button
#         save_button = QPushButton("Save")
#         save_button.clicked.connect(self.save_new_time)
#         layout.addWidget(save_button)

#         self.setLayout(layout)

#     def save_new_time(self):
#         task_name = self.task_combo.currentText()
#         new_time = self.time_input.text()
#         try:
#             # Ensure input is exactly 4 digits and digits only
#             if len(new_time) != 4 or not new_time.isdigit():
#                 raise ValueError("Please enter time in HHMM format, where HH is hour and MM is minute.")
#             datetime.strptime(new_time, '%H%M')
#             self.config.update_preferences(task_name, new_time)
#             self.accept()
#         except ValueError as e:
#             QMessageBox.critical(self, "Invalid Time", f"Invalid time format: {str(e)}")

# class LoggingWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()

#     def init_ui(self):
#         chime.info()
#         layout = QVBoxLayout()
#         self.setWindowTitle("Log Activity")

#         # Activity dropdown
#         self.activity_combo = QComboBox()
#         activities = ['READ', 'WRKT', 'CORE', 'GOMU', 'PRCR', 'MEAL']
#         self.activity_combo.addItems(activities)
#         layout.addWidget(QLabel("Select Activity:"))
#         layout.addWidget(self.activity_combo)

#         # Description input
#         self.desc_input = QLineEdit()
#         self.desc_input.setPlaceholderText("Describe what you did")
#         layout.addWidget(QLabel("Description:"))
#         layout.addWidget(self.desc_input)

#         # Save button
#         save_button = QPushButton("Save")
#         save_button.clicked.connect(self.save_log)
#         layout.addWidget(save_button)

#         self.setLayout(layout)

#     def save_log(self):
#         activity = self.activity_combo.currentText()
#         description = self.desc_input.text()
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         log_message = f"{timestamp} {activity} - {description}\n"
#         with open("activity_log.txt", "a") as file:
#             file.write(log_message)
#         self.accept()

