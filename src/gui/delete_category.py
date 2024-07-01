from PyQt5.QtWidgets import QComboBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ..db.models import TaskCategory

class DeleteCategoryWindow(QDialog):
    category_deleted = pyqtSignal()

    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        self.no_categories = self.check_no_categories()  # Initial check for tasks
        layout = QVBoxLayout()
        if self.no_categories:
            # Display the error message and set up a basic layout for the message
            self.setWindowTitle("No Categories to delete")
            task_label = QLabel("No categories to delete.")
            task_label.setStyleSheet("color: black;")
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.close)  # Connect the Close button to close the dialog
            layout.addWidget(task_label)
            layout.addWidget(close_button)
            self.setLayout(layout)
            return
        self.setWindowTitle("Delete Category")

        # Category selection
        self.category_combo = QComboBox()
        categories = self.config.session.query(TaskCategory).all()
        for cat in categories:
            self.category_combo.addItem(cat.category_name, userData=cat)
        category_label = QLabel("Select Category:")
        category_label.setStyleSheet("color: black;")
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)

        # Delete button
        delete_button = QPushButton("Delete Category", self)
        delete_button.clicked.connect(self.delete_category)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def check_no_categories(self):
        tasks = self.config.session.query(TaskCategory).all()
        return len(tasks) == 0

    def delete_category(self):
        category = self.category_combo.currentData()
        self.config.session.delete(category)
        self.config.session.commit()
        self.category_deleted.emit()
        self.accept()
