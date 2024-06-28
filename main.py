import os
from src.gui import run_gui
from src.config import Config
from dotenv import load_dotenv

repo_dir = os.path.dirname(os.path.abspath(__file__))
tasks_file_path = os.path.join(repo_dir, 'tasks_data.json')

load_dotenv()
db_user = os.getenv('db_user')
db_password = os.getenv('db_pw')
db_host = os.getenv('db_host')
db_name = os.getenv('db_name')
db_url = f'mariadb+mariadbconnector://{db_user}:{db_password}@{db_host}/{db_name}'

config = Config(db_url=db_url)

run_gui(config)
