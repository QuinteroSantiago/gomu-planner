import os
from src.gui import run_gui
from src.config import Config

repo_dir = os.path.dirname(os.path.abspath(__file__))
tasks_file_path = os.path.join(repo_dir, 'tasks_data.json')

config = Config(tasks_file=tasks_file_path)

run_gui(config)
