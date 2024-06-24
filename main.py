from src.data_management import load_data
import src.config as config
import os

repo_dir = os.path.dirname(os.path.abspath(__file__))

config.tasks_file = os.path.join(repo_dir, config.tasks_file)
config.tasks_data = load_data(config.tasks_file)

# Load tasks when application starts
config.daily_tasks = config.tasks_data.get('daily_tasks', [])
config.variable_tasks = config.tasks_data.get('variable_tasks', [])
config.conditional_tasks = config.tasks_data.get('conditional_tasks', {})
config.preferences = config.tasks_data.get('preferred_times', {})

from src.gui import run_gui
run_gui()
