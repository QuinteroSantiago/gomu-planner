from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
    QTextEdit, QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
from datetime import datetime, date
from .schedule import create_schedule
import chime
import os
from .gui.adjust_time import AdjustTimeWindow
from .gui.logging import LoggingWindow
from .gui.view_logs import ViewLogsWindow
from .gui.add_new_task import AddTaskWindow

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

        # Top layout for displaying date and schedule
        top_layout = QVBoxLayout()
        today = date.today().strftime("%A, %B %d, %Y")
        self.header_label = QLabel(today)
        top_layout.addWidget(self.header_label)
        self.schedule_display = QTextEdit(self)
        self.schedule_display.setReadOnly(True)
        top_layout.addWidget(self.schedule_display)

        # Main layout for two columns
        main_layout = QHBoxLayout()

        # Left column for tasks
        left_layout = QVBoxLayout()
        task_label = QLabel("Tasks")
        left_layout.addWidget(task_label)

        # Buttons for task management
        self.add_task_button = QPushButton("Add a New Task", self)
        self.add_task_button.clicked.connect(self.add_task_window)
        left_layout.addWidget(self.add_task_button)

        self.adjust_button = QPushButton("Adjust Task Time", self)
        self.adjust_button.clicked.connect(self.adjust_time_window)
        left_layout.addWidget(self.adjust_button)

        # Right column for logs
        right_layout = QVBoxLayout()
        log_label = QLabel("Logs")
        right_layout.addWidget(log_label)

        self.log_button = QPushButton("Log Activity Now", self)
        self.log_button.clicked.connect(self.logging_window)
        right_layout.addWidget(self.log_button)

        self.view_logs_button = QPushButton("View Logs", self)
        self.view_logs_button.clicked.connect(self.view_logs_window)
        right_layout.addWidget(self.view_logs_button)

        # Add columns to the main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Bottom layout for exit button
        bottom_layout = QHBoxLayout()
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        bottom_layout.addWidget(self.exit_button, 0, Qt.AlignCenter)

        # Final layout setup
        final_layout = QVBoxLayout()
        final_layout.addLayout(top_layout)
        final_layout.addLayout(main_layout)
        final_layout.addLayout(bottom_layout)

        # Set the final layout to the central widget
        central_widget.setLayout(final_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_schedule)
        self.timer.start(1000)

        self.logging_timer = QTimer(self)
        self.logging_timer.timeout.connect(self.logging_window)
        self.reset_logging_timer()

        self.update_schedule()

    def reset_logging_timer(self):
        self.logging_timer.start(30 * 60 * 1000)

    def update_schedule(self):
        now = datetime.now()
        if now.second % 2 == 0:
            current_time = now.strftime("%H:%M")
        else:
            current_time = now.strftime("%H %M")

        self.schedule_display.clear()
        self.schedule_display.append(f"<div style='text-align:left;'>{current_time}</div>")

        day_of_week = datetime.today().weekday()
        schedule = create_schedule(self.config.daily_tasks, self.config.variable_tasks,
                day_of_week, self.config.preferences)

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
        dialog = AdjustTimeWindow(self.config, self.styleSheet())
        dialog.exec_()
        self.update_schedule()

    def logging_window(self):
        log_win = LoggingWindow(self.styleSheet())
        log_win.exec_()
        self.reset_logging_timer()

    def view_logs_window(self):
        log_window = ViewLogsWindow(self.styleSheet())
        log_window.exec_()

    def add_task_window(self):
        # task_window = AddTaskWindow(self.styleSheet())
        task_window = AddTaskWindow(self.config)
        task_window.exec_()

def run_gui(config):
    app = QApplication([])
    window = MainApp(config)
    window.show()
    app.exec_()

