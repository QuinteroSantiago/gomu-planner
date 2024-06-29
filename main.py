from src.config import Config
from src.main_gui import run_gui
from src.main_db import setup_database

config = Config()
setup_database(config)
run_gui(config)
