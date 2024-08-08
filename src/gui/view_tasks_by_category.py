from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLabel, QTextEdit
from ..db.models import TaskCategory, Task

class ViewTasksByCategoryWindow(QDialog):
    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("View Tasks")
        self.setGeometry(800, 50, 1600, 1600)

        # Category selection
        self.category_combo = QComboBox()
        categories = self.config.session.query(TaskCategory).all()
        for category in categories:
            self.category_combo.addItem(category.category_name, userData=category.id)
        self.category_combo.currentIndexChanged.connect(self.update_task_display)
        select_category_widget = QLabel("Select Category:")
        select_category_widget.setStyleSheet("color: black;")
        layout.addWidget(select_category_widget)
        layout.addWidget(self.category_combo)

        # Task display area
        self.task_display = QTextEdit()
        self.task_display.setReadOnly(True)
        layout.addWidget(self.task_display)

        self.setLayout(layout)
        self.update_task_display(0)  # Initial update to show tasks for the first category

    def update_task_display(self, index):
        category_id = self.category_combo.itemData(index)
        tasks = self.config.session.query(Task).filter_by(category_id=category_id).all()
        display_text = "\n".join([f"[{task.frequency.value}] {task.task_name} - Duration: {task.duration} mins" for task in tasks])
        self.task_display.setPlainText(display_text if display_text else "No tasks found in this category.")
