from PyQt5.QtWidgets import QComboBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ..db.models import TaskCategory

class EditCategoryWindow(QDialog):
    category_edited = pyqtSignal()

    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setWindowTitle("Edit Category")

        # Category selection
        self.category_combo = QComboBox()
        categories = self.config.session.query(TaskCategory).all()
        for cat in categories:
            self.category_combo.addItem(cat.category_name, userData=cat)
        category_label = QLabel("Select Category:")
        category_label.setStyleSheet("color: black;")
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)

        # New name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("New category name")
        category_name_label = QLabel("New Category Name:")
        category_name_label.setStyleSheet("color: black;")
        layout.addWidget(category_name_label)
        layout.addWidget(self.name_input)

        # Color picker button
        self.color_button = QPushButton("Pick New Color", self)
        self.color_button.clicked.connect(self.pick_color)
        self.color = None
        layout.addWidget(self.color_button)

        # Save button
        save_button = QPushButton("Save Changes", self)
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()

    def save_changes(self):
        category = self.category_combo.currentData()
        new_name = self.name_input.text().strip()
        new_color = self.color if self.color else category.color

        if new_name:
            category.category_name = new_name
        if new_color:
            category.color = new_color

        self.config.session.commit()
        self.category_edited.emit()
        self.accept()
