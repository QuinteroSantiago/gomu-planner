from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey, Table, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from enum import Enum as PyEnum

Base = declarative_base()

# Association Table for tasks and preferences
task_preferences = Table('task_preferences', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('preference_id', Integer, ForeignKey('preferences.id'))
)

class Frequency(PyEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    ONCE = "once"

class TaskCategory(Base):
    __tablename__ = 'task_categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False, unique=True)
    color = Column(String(7), nullable=False)  # Store color as a string (e.g., '#00FF00')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)
    task_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('task_categories.id'))
    category = relationship('TaskCategory')
    preferences = relationship('Preference', secondary=task_preferences, back_populates='tasks')

    frequency = Column(Enum(Frequency), default=Frequency.DAILY.value)
    day_of_week = Column(Integer, nullable=True)  # For weekly tasks
    day_of_month = Column(Integer, nullable=True)  # Day of the month for monthly tasks
    specific_date = Column(Date, nullable=True)  # Month for yearly tasks

    @classmethod
    def create(cls, session, duration, task_name, category_id, frequency, day_of_week=None, day_of_month=None, specific_date=None):
        new_task = cls(
            duration=duration, 
            task_name=task_name, 
            category_id=category_id, 
            frequency=frequency,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            specific_date=specific_date
        )
        session.add(new_task)
        session.commit()
        return new_task

class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    preferred_time = Column(Time, nullable=False)
    tasks = relationship('Task', secondary=task_preferences, back_populates='preferences')
