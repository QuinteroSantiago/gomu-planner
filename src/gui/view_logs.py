from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QDialog
from ..db.models import TaskCategory

class ViewLogsWindow(QDialog):
    def __init__(self, config, style_sheet=None):
        super().__init__()
        self.config = config
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.category_colors = self.fetch_category_colors()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("View Activity Logs")
        self.setGeometry(800, 50, 1600, 1600)

        # Create a QTextEdit for displaying logs
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)  # Make the text area read-only

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.log_text)
        self.setLayout(layout)

        # Load and display the logs
        self.load_logs()

    def fetch_category_colors(self):
        colors = {}
        categories = self.config.session.query(TaskCategory).all()
        for category in categories:
            colors[category.category_name] = category.color
        return colors

    def load_logs(self):
        try:
            with open("activity_log.txt", "r") as file:
                log_contents = file.readlines()

            formatted_text = ""
            for line in log_contents:
                parts = line.split(" - ", 1)  # Split the line into [timestamp and category, description]
                if len(parts) == 2:
                    time_category_part, description = parts
                    time_category_parts = time_category_part.split()
                    timestamp = " ".join(time_category_parts[:2])
                    category = time_category_parts[2]

                    # Use fetched colors or a default if category is not in dictionary
                    category_color = self.category_colors.get(category, 'magenta')

                    # Format the text with HTML
                    formatted_text += f"<span style='color:gray;'>{timestamp}</span> <span style='color:{category_color};'>{category}</span> - <span style='color:white;'>{description}</span><br>"
                else:
                    formatted_text += f"<span style='color:white;'>{line}</span><br>"

            self.log_text.setHtml(formatted_text)
        except FileNotFoundError:
            self.log_text.setPlainText("No logs found.")
        except Exception as e:
            print(f"Error while loading logs: {e}")

    def closeEvent(self, event):
        event.accept()
