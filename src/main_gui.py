from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
        QTextEdit, QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QSpacerItem, QSizePolicy
from datetime import datetime, date
from .schedule import create_schedule
import chime
import os
from .gui.adjust_time import EditTaskWindow
from .gui.add_log import LoggingWindow
from .gui.view_logs import ViewLogsWindow
from .gui.add_new_task import AddTaskWindow
from .gui.delete_task import DeleteTaskWindow
from .gui.add_category import AddCategoryWindow
from .gui.delete_category import DeleteCategoryWindow
from .gui.edit_category import EditCategoryWindow
from .gui.view_tasks_by_category import ViewTasksByCategoryWindow
from .db.models import TaskCategory

class MainApp(QMainWindow):
    def __init__(self, config):
        super().__init__()
        chime.theme('pokemon')
        self.config = config
        self.setWindowTitle("Gomu Planner")
        self.setGeometry(0, 0, 800, 1600)
        self.load_styles()
        QApplication.setFont(QFont("Courier New", 12))
        self.category_colors = self.fetch_category_colors()
        self.current_active_task = None
        self.chime_enabled = True

        self.write_log_entry("GOMU", "OPEN APP")

        self.init_ui()

    def load_styles(self):
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(repo_dir)
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

        # First horizontal layout for Tasks and Logs
        first_row_layout = QHBoxLayout()

        # Left column for tasks
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop)
        task_label = QLabel("Tasks")
        left_layout.addWidget(task_label)

        self.add_task_button = QPushButton("Add a New Task", self)
        self.add_task_button.clicked.connect(self.add_task_window)
        left_layout.addWidget(self.add_task_button)

        self.delete_task_button = QPushButton("Delete Task", self)
        self.delete_task_button.clicked.connect(self.delete_task_window)
        left_layout.addWidget(self.delete_task_button)

        self.adjust_button = QPushButton("Adjust Task Time", self)
        self.adjust_button.clicked.connect(self.adjust_time_window)
        left_layout.addWidget(self.adjust_button)

        # Second column for logs
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)
        log_label = QLabel("Logs")
        right_layout.addWidget(log_label)

        self.log_button = QPushButton("Log Activity Now", self)
        self.log_button.clicked.connect(self.logging_window)
        right_layout.addWidget(self.log_button)

        self.view_logs_button = QPushButton("View Logs", self)
        self.view_logs_button.clicked.connect(self.view_logs_window)
        right_layout.addWidget(self.view_logs_button)

        # Add the task and log layouts to the first row
        first_row_layout.addLayout(left_layout)
        first_row_layout.addLayout(right_layout)

        # Second horizontal layout for Categories and Other
        second_row_layout = QHBoxLayout()

        # Third column for categories
        categories_layout = QVBoxLayout()
        categories_layout.setAlignment(Qt.AlignTop)
        category_label = QLabel("Categories")
        categories_layout.addWidget(category_label)

        self.add_category_button = QPushButton("Add Category", self)
        self.add_category_button.clicked.connect(self.add_category_window)
        categories_layout.addWidget(self.add_category_button)

        self.edit_category_button = QPushButton("Edit Category", self)
        self.edit_category_button.clicked.connect(self.edit_category_window)
        categories_layout.addWidget(self.edit_category_button)

        self.delete_category_button = QPushButton("Delete Category", self)
        self.delete_category_button.clicked.connect(self.delete_category_window)
        categories_layout.addWidget(self.delete_category_button)

        # Fourth column for other options
        other_layout = QVBoxLayout()
        other_layout.setAlignment(Qt.AlignTop)
        other_label = QLabel("Other")
        other_layout.addWidget(other_label)

        self.silencer_button = QPushButton("STFU", self)
        self.silencer_button.clicked.connect(self.toggle_chimes)
        other_layout.addWidget(self.silencer_button)

        self.view_tasks_button = QPushButton("View Tasks By Category", self)
        self.view_tasks_button.clicked.connect(self.view_tasks_by_category_window)
        other_layout.addWidget(self.view_tasks_button)

        # Add the categories and other layouts to the second row
        second_row_layout.addLayout(categories_layout)
        second_row_layout.addLayout(other_layout)

        # Bottom layout for exit button
        bottom_layout = QHBoxLayout()
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        bottom_layout.addWidget(self.exit_button, 0, Qt.AlignCenter)

        # Final layout setup
        final_layout = QVBoxLayout()
        final_layout.addLayout(top_layout)
        final_layout.addLayout(first_row_layout)
        final_layout.addLayout(second_row_layout)
        final_layout.addLayout(bottom_layout)

        central_widget.setLayout(final_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_schedule)
        self.timer.start(1000)

        self.logging_timer = QTimer(self)
        self.logging_timer.timeout.connect(self.logging_window)
        self.reset_logging_timer()

        self.update_schedule()

    def toggle_chimes(self):
        self.chime_enabled = not self.chime_enabled
        btn_text = "Enable Sounds" if not self.chime_enabled else "STFU"
        self.silencer_button.setText(btn_text)

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
        schedule = create_schedule(self.config.tasks, day_of_week, self.config.preferences)

        new_current_task = None
        for start_dt, end_dt, task_name, category_name, task_duration in schedule:
            start_time_str = start_dt.strftime('%H:%M')
            if start_dt <= now < end_dt:
                color = "lightgreen"  # Current task
                category_color = "lightgreen"
                new_current_task = task_name
            elif end_dt < now:
                color = "red"    # Past task
                category_color = "red"
            else:
                color = "white"   # Future task
                # Get the category color for future tasks
                category_color = self.category_colors.get(category_name, 'magenta')
            # Convert task_duration to string for length checking
            task_duration_str = str(task_duration)

            # Determine the number of non-breaking spaces based on the length of task_duration
            if len(task_duration_str) == 1:
                task_duration_str = f"&nbsp;&nbsp;&nbsp;{task_duration_str}"  # Three non-breaking spaces
            elif len(task_duration_str) == 2:
                task_duration_str = f"&nbsp;&nbsp;{task_duration_str}"   # Two non-breaking spaces
            elif len(task_duration_str) == 3:
                task_duration_str = f"&nbsp;{task_duration_str}"    # One non-breaking space

            # Insert the formatted task_duration into the display
            self.schedule_display.append(
                f"<div style='color:{color};'>{start_time_str} "
                f"<span style='color:{category_color};'>[{category_name}]</span>"
                f"{task_duration_str}: {task_name}</div>"
            )

        # Check if the active task has changed and play a chime if it has
        if new_current_task != self.current_active_task and new_current_task is not None:
            if self.chime_enabled:
                chime.success()
            self.current_active_task = new_current_task

    def adjust_time_window(self):
        dialog = EditTaskWindow(self.config, self.styleSheet())
        dialog.exec_()
        self.update_schedule()

    def logging_window(self):
        if self.chime_enabled:
            chime.info()
        log_win = LoggingWindow(self.config, self.styleSheet())
        log_win.exec_()
        self.reset_logging_timer()

    def view_logs_window(self):
        log_window = ViewLogsWindow(self.config, self.styleSheet())
        log_window.exec_()

    def add_task_window(self):
        add_task_window = AddTaskWindow(self.config, self.styleSheet())
        add_task_window.task_added.connect(self.config.load_data)
        add_task_window.exec_()

    def delete_task_window(self):
        delete_task_window = DeleteTaskWindow(self.config, self.styleSheet())
        delete_task_window.task_deleted.connect(self.config.load_data) # Refresh UI
        delete_task_window.exec_()

    def add_category_window(self):
        dialog = AddCategoryWindow(self.config, self.styleSheet())
        dialog.category_added.connect(self.config.load_data)
        dialog.exec_()

    def edit_category_window(self):
        dialog = EditCategoryWindow(self.config, self.styleSheet())
        dialog.category_edited.connect(self.config.load_data)
        dialog.exec_()

    def delete_category_window(self):
        dialog = DeleteCategoryWindow(self.config, self.styleSheet())
        dialog.category_deleted.connect(self.config.load_data)
        dialog.exec_()

    def view_tasks_by_category_window(self):
        dialog = ViewTasksByCategoryWindow(self.config, self.styleSheet())
        dialog.exec_()

    def fetch_category_colors(self):
        colors = {}
        categories = self.config.session.query(TaskCategory).all()
        for category in categories:
            colors[category.category_name] = category.color
        return colors

    def write_log_entry(self, activity, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} {activity} - {description}\n"
        with open(self.config.log_file_path, "a") as file:
            file.write(log_message)

    def closeEvent(self, event):
        self.write_log_entry("GOMU", "CLOSE APP")
        super().closeEvent(event)

def run_gui(config):
    app = QApplication([])
    window = MainApp(config)
    window.show()
    app.exec_()

