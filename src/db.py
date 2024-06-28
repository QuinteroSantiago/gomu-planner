from sqlalchemy import create_engine
from db.models import Base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

db_user = os.getenv('db_user')
db_password = os.getenv('db_pw')
db_host = os.getenv('db_host')
db_name = os.getenv('db_name')

db_url = f'mariadb+mariadbconnector://{db_user}:{db_password}@{db_host}/{db_name}'

engine = create_engine(db_url)
Base.metadata.create_all(engine)

print("Database tables created successfully!")
