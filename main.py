from src.config import Config
from src.main_gui import run_gui
from src.main_db import setup_database

setup_database()
config = Config()
run_gui(config)
