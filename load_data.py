import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from src.db.models import Base, DailyTask, VariableTask, ConditionalTask, Preference
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

# Load JSON data
with open(tasks_file_path, 'r') as file:
    data = json.load(file)

# Insert daily tasks
for start_time, duration, task_name in data['daily_tasks']:
    start_time_obj = datetime.strptime(start_time, '%H%M').time()
    daily_task = DailyTask(start_time=start_time_obj, duration=duration, task_name=task_name)
    session.add(daily_task)

# Insert variable tasks
for duration, task_name in data['variable_tasks']:
    variable_task = VariableTask(duration=duration, task_name=task_name)
    session.add(variable_task)

# Insert conditional tasks
for day_of_week, tasks in data['conditional_tasks'].items():
    for start_time, duration, task_name in tasks:
        start_time_obj = datetime.strptime(start_time, '%H%M').time()
        conditional_task = ConditionalTask(day_of_week=int(day_of_week), start_time=start_time_obj, duration=duration, task_name=task_name)
        session.add(conditional_task)

# Insert preferences
for task_name, preferred_time in data['preferred_times'].items():
    preferred_time_obj = datetime.strptime(preferred_time, '%H%M').time()
    preference = Preference(task_name=task_name, preferred_time=preferred_time_obj)
    session.add(preference)

# Commit the session to save data into the database
session.commit()
session.close()

print("Data loaded successfully!")
