from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Association Table for variable tasks and preferences
variable_task_preferences = Table('variable_task_preferences', Base.metadata,
    Column('variable_task_id', Integer, ForeignKey('variable_tasks.id')),
    Column('preference_id', Integer, ForeignKey('preferences.id'))
)

class DailyTask(Base):
    __tablename__ = 'daily_tasks'
    id = Column(Integer, primary_key=True)
    start_time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)
    task_name = Column(String(255), nullable=False)

class VariableTask(Base):
    __tablename__ = 'variable_tasks'
    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)
    task_name = Column(String(255), nullable=False)
    preferences = relationship('Preference', secondary=variable_task_preferences, back_populates='tasks')

class ConditionalTask(Base):
    __tablename__ = 'conditional_tasks'
    id = Column(Integer, primary_key=True)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)
    task_name = Column(String(255), nullable=False)

class Preference(Base):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    preferred_time = Column(Time, nullable=False)
    tasks = relationship('VariableTask', secondary=variable_task_preferences, back_populates='preferences')
