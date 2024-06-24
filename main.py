from src.data_management import load_data
import src.config as config

config.preferences = load_data(config.preferences_file)
config.tasks_data = load_data('tasks_data.json')
# Load tasks when application starts
config.daily_tasks = config.tasks_data.get('daily_tasks', [])
config.variable_tasks = config.tasks_data.get('variable_tasks', [])
config.conditional_tasks = config.tasks_data.get('conditional_tasks', {})

from src.gui import run_gui
run_gui()
