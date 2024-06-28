from PyQt5.QtWidgets import (QTextEdit, QVBoxLayout, QDialog)

class ViewLogsWindow(QDialog):
    def __init__(self, style_sheet=None):
        super().__init__()
        if style_sheet:
            self.setStyleSheet(style_sheet)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("View Activity Logs")
        self.setGeometry(800, 100, 1600, 1600)

        # Create a QTextEdit for displaying logs
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)  # Make the text area read-only

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.log_text)
        self.setLayout(layout)

        # Load and display the logs
        self.load_logs()

    def load_logs(self):
        try:
            with open("activity_log.txt", "r") as file:
                log_contents = file.readlines()

            formatted_text = ""
            for line in log_contents:
                # Split once at the first occurrence of " - " to separate the timestamp/category from the description
                parts = line.split(" - ", 1)  # This splits the line into [timestamp and category, description]
                if len(parts) == 2:
                    # Further split the first part to separate the timestamp and category
                    time_category_part, description = parts
                    time_category_parts = time_category_part.split()
                    timestamp = " ".join(time_category_parts[:2])  # Join date and time
                    category = time_category_parts[2]  # Category is the third element

                    # Determine the color based on the category
                    category_color = {
                        'MEAL': 'green',
                        'CORE': 'blue',
                        'GOMU': 'orange',
                        'PRCR': 'red'
                    }.get(category, 'magenta')  # Default color if category doesn't match

                    # Format the text with appropriate HTML for colors
                    formatted_text += f"<span style='color:gray;'>{timestamp}</span> <span style='color:{category_color};'>{category}</span> - <span style='color:white;'>{description}</span><br>"
                else:
                    # If splitting fails, add the line as plain text
                    formatted_text += f"<span style='color:white;'>{line}</span><br>"

            self.log_text.setHtml(formatted_text)
        except FileNotFoundError:
            self.log_text.setPlainText("No logs found.")
        except Exception as e:
            print(f"Error while loading logs: {e}")

    def closeEvent(self, event):
        event.accept()
