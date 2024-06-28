import os
from src.config import Config
from dotenv import load_dotenv
from src.main_gui import run_gui

load_dotenv()
db_user = os.getenv('db_user')
db_password = os.getenv('db_pw')
db_host = os.getenv('db_host')
db_name = os.getenv('db_name')
db_url = f'mariadb+mariadbconnector://{db_user}:{db_password}@{db_host}/{db_name}'

config = Config(db_url=db_url)

run_gui(config)
