from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from .db.models import Base
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def setup_database():
    load_dotenv()
    db_user = os.getenv('db_user')
    db_password = os.getenv('db_pw')
    db_host = os.getenv('db_host')
    db_name = os.getenv('db_name')
    db_url = f'mariadb+mariadbconnector://{db_user}:{db_password}@{db_host}/{db_name}'

    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        logging.info("Database tables created successfully!")
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while setting up the database: {e}")
