from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QDialog
from ..db.models import TaskCategory
import datetime
from collections import defaultdict

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

            # Determine the start and end of the current week (Monday to Sunday)
            today = datetime.date.today()
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=7)

            # Dictionary to hold logs grouped by date
            logs_by_date = defaultdict(list)

            for line in log_contents:
                parts = line.strip().split(" - ", 1)  # Split into [timestamp and category, description]
                if len(parts) == 2:
                    time_category_part, description = parts
                    time_category_parts = time_category_part.strip().split()
                    if len(time_category_parts) >= 3:
                        date_str = time_category_parts[0]
                        time_str = time_category_parts[1]
                        category = time_category_parts[2]

                        # Parse the datetime
                        log_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

                        # Check if the log date is in the current week
                        if start_of_week <= log_datetime.date() < end_of_week:
                            # Group logs by date
                            logs_by_date[log_datetime.date()].append({
                                'time': log_datetime.time(),
                                'category': category,
                                'description': description
                            })
                    else:
                        # Handle lines that do not have the expected format
                        continue

            # Sort the dates and format the logs
            formatted_text = ""
            for date in sorted(logs_by_date.keys()):
                # Display the date
                formatted_text += f"<span style='color:white; font-weight:bold;'>{date}</span><br>"
                for log in logs_by_date[date]:
                    timestamp = log['time'].strftime("%H:%M:%S")
                    category = log['category']
                    description = log['description']

                    # Use fetched colors or a default color
                    category_color = self.category_colors.get(category, 'magenta')

                    # Format the log entry
                    formatted_text += (
                        f"<span style='color:gray;'>{timestamp}</span> "
                        f"<span style='color:{category_color};'>{category}</span> - "
                        f"<span style='color:white;'>{description}</span><br>"
                    )
                formatted_text += "<br>"  # Add a line break after each date

            if formatted_text:
                self.log_text.setHtml(formatted_text)
            else:
                self.log_text.setPlainText("No logs found for the current week.")
        except FileNotFoundError:
            self.log_text.setPlainText("No logs found.")
        except Exception as e:
            print(f"Error while loading logs: {e}")

    def closeEvent(self, event):
        event.accept()
