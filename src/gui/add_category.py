from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ..db.models import TaskCategory

class AddCategoryWindow(QDialog):
    category_added = pyqtSignal()

    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Add New Category")

        # Category name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter category name")
        category_label = QLabel("Category Name:")
        category_label.setStyleSheet("color: black;")
        layout.addWidget(category_label)
        layout.addWidget(self.name_input)

        # Color picker button
        self.color_button = QPushButton("Pick Color", self)
        self.color_button.clicked.connect(self.pick_color)
        self.color = None  # This will store the chosen color
        layout.addWidget(self.color_button)

        # Save button
        save_button = QPushButton("Save Category", self)
        save_button.clicked.connect(self.save_category)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()

    def save_category(self):
        name = self.name_input.text().strip()
        if not name or not self.color:
            QMessageBox.warning(self, "Warning", "Please enter a name and pick a color.")
            return

        # Check if category already exists
        existing_category = self.config.session.query(TaskCategory).filter_by(category_name=name).first()
        if existing_category:
            QMessageBox.warning(self, "Warning", "Category already exists.")
            return

        new_category = TaskCategory(category_name=name, color=self.color)
        self.config.session.add(new_category)
        self.config.session.commit()
        self.category_added.emit()
        self.accept()
