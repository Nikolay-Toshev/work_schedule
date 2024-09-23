import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

# Define Table Classes
Base = declarative_base()

engine = sa.create_engine('sqlite:///work_schedule.db')

class Employee(Base):
    __tablename__ = 'employees'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

class WorkingHours(Base):
    __tablename__ = 'working_hours'

    id = sa.Column(sa.Integer, primary_key=True)
    start_hour = sa.Column(sa.String)
    end_hour = sa.Column(sa.String)
    working_hours = sa.Column(sa.Float)
    is_sick = sa.Column(sa.Boolean, nullable=True, default=False)
    is_on_vacation = sa.Column(sa.Boolean, nullable=True, default=False)

class WeekSchedule(Base):
    __tablename__ = 'week_schedule'

    id = sa.Column(sa.Integer, primary_key=True)
    week = sa.Column(sa.String)
    weekday = sa.Column(sa.String)
    employee = sa.Column(sa.Integer, sa.ForeignKey('employees.id'), nullable=False, default=1)
    working_hours = sa.Column(sa.Integer, sa.ForeignKey('working_hours.id'), nullable=False)

