from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .db.models import DailyTask, VariableTask, ConditionalTask, Preference
from datetime import datetime

class Config:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.load_data()

    def load_data(self):
        self.daily_tasks = self.session.query(DailyTask).all()
        self.variable_tasks = self.session.query(VariableTask).all()
        self.conditional_tasks = self.session.query(ConditionalTask).all()
        self.preferences = {pref.task_name: pref.preferred_time for pref in self.session.query(Preference).all()}
        # Ensure tasks_data has preferred_times initialized
        self.tasks_data = {
            'preferred_times': self.preferences,
            'daily_tasks': self.daily_tasks,
            'variable_tasks': self.variable_tasks,
            'conditional_tasks': self.conditional_tasks
        }

    def save_data(self):
        # Save preferences to the database
        for task_name, preferred_time in self.preferences.items():
            preference = self.session.query(Preference).filter_by(task_name=task_name).first()
            if preference:
                preference.preferred_time = preferred_time
            else:
                new_preference = Preference(task_name=task_name, preferred_time=preferred_time)
                self.session.add(new_preference)
        self.session.commit()

    def update_preferences(self, task_name, new_time):
        time_obj = datetime.strptime(new_time, '%H%M').time()
        self.preferences[task_name] = time_obj
        self.save_data()
