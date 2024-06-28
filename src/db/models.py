from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Association Table for variable tasks and preferences
variable_task_preferences = Table('variable_task_preferences', Base.metadata,
    Column('variable_task_id', Integer, ForeignKey('variable_tasks.id')),
    Column('preference_id', Integer, ForeignKey('preferences.id'))
)

class TaskCategory(Base):
    __tablename__ = 'task_categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False, unique=True)
    color = Column(String(7), nullable=False)  # Store color as a string (e.g., '#00FF00')

class DailyTask(Base):
    __tablename__ = 'daily_tasks'
    id = Column(Integer, primary_key=True)
    start_time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)
    task_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('task_categories.id'))
    category = relationship('TaskCategory')

class VariableTask(Base):
    __tablename__ = 'variable_tasks'
    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)
    task_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('task_categories.id'))
    category = relationship('TaskCategory')
    preferences = relationship('Preference', secondary=variable_task_preferences, back_populates='tasks')

class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    preferred_time = Column(Time, nullable=False)
    tasks = relationship('VariableTask', secondary=variable_task_preferences, back_populates='preferences')
