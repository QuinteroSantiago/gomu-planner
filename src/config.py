from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from .db.models import Task, Preference, TaskCategory
from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.get_session()
        self.load_data()

    @property
    def database_url(self):
        db_user = os.getenv('db_user')
        db_password = os.getenv('db_pw')
        db_host = os.getenv('db_host')
        db_name = os.getenv('db_name')
        return f'mariadb+mariadbconnector://{db_user}:{db_password}@{db_host}/{db_name}'

    def get_session(self):
        return self.Session()

    def load_data(self):
        with self.get_session() as session:
            self.tasks = session.query(Task).options(joinedload(Task.category)).all()
            self.preferences = {pref.task_name: pref.preferred_time for pref in session.query(Preference).all()}
            self.tasks_data = {
                'preferred_times': self.preferences,
                'tasks': self.tasks,
            }

    def save_data(self):
        with self.get_session() as session:
            for task_name, preferred_time in self.preferences.items():
                preference = session.query(Preference).filter_by(task_name=task_name).first()
                if preference:
                    preference.preferred_time = preferred_time
                else:
                    session.add(Preference(task_name=task_name, preferred_time=preferred_time))
            session.commit()

    def update_preferences(self, task_name, new_time):
        from datetime import datetime
        time_obj = datetime.strptime(new_time, '%H%M').time()
        self.preferences[task_name] = time_obj
        self.save_data()
