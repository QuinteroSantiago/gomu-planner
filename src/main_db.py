from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from .db.models import Base
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def setup_database(config):
    try:
        db_url = config.database_url
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        logging.info("Database tables created successfully!")
    except SQLAlchemyError as e:
        logging.error(f"An error occurred while setting up the database: {e}")
