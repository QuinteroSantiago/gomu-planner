import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from src.db.models import Base, DailyTask, VariableTask, Preference, TaskCategory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_user = os.getenv('db_user')
db_password = os.getenv('db_pw')
db_host = os.getenv('db_host')
db_name = os.getenv('db_name')

db_url = f'mariadb+mariadbconnector://{db_user}:{db_password}@{db_host}/{db_name}'

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# Path to tasks_data.json
repo_dir = os.path.dirname(os.path.abspath(__file__))
tasks_file_path = os.path.join(repo_dir, 'tasks_data.json')

# Insert task categories
categories = {
    'MEAL': '#00FF00',  # green
    'CORE': '#0000FF',  # blue
    'GOMU': '#FFA500',  # orange
    'LAZY': '#FF0000',  # red
    'MEDS': '#FFFF00',   # yellow
    'FOOD': '#00FF00'  # green
}

for category_name, color in categories.items():
    category = TaskCategory(category_name=category_name, color=color)
    session.add(category)

session.commit()

# Load JSON data
with open(tasks_file_path, 'r') as file:
    data = json.load(file)

# Insert daily tasks
for start_time, duration, task_name, category_name in data['daily_tasks']:
    start_time_obj = datetime.strptime(start_time, '%H%M').time()
    category = session.query(TaskCategory).filter_by(category_name=category_name).first()
    daily_task = DailyTask(start_time=start_time_obj, duration=duration, task_name=task_name, category=category)
    session.add(daily_task)

# Insert variable tasks
for duration, task_name, category_name in data['variable_tasks']:
    category = session.query(TaskCategory).filter_by(category_name=category_name).first()
    variable_task = VariableTask(duration=duration, task_name=task_name, category=category)
    session.add(variable_task)

# Insert preferences
for task_name, preferred_time in data['preferred_times'].items():
    preferred_time_obj = datetime.strptime(preferred_time, '%H%M').time()
    preference = Preference(task_name=task_name, preferred_time=preferred_time_obj)
    session.add(preference)

# Commit the session to save data into the database
session.commit()
session.close()

print("Data loaded successfully!")
