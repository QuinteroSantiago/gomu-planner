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
        layout = QVBoxLayout()
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

    def delete_category(self):
        category = self.category_combo.currentData()
        self.config.session.delete(category)
        self.config.session.commit()
        self.category_deleted.emit()
        self.accept()
