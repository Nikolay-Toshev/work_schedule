import sqlalchemy as sa
from sqlalchemy import values, column

engine = sa.create_engine('sqlite:///work_schedule.db')

class Employee(sa.Base):
    __tablename__ = 'employees'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

class WorkingHours(sa.Base):
    __tablename__ = 'working_hours'

    id = sa.Column(sa.Integer, primary_key=True)
    start_hour = sa.Column(sa.Time)
    end_hour = sa.Column(sa.Time)
    working_hours = sa.Column(sa.Float)

class WeekSchedule(sa.Base):
    __tablename__ = 'week_schedule'

    MY_VALUES = [(1, 'Понеделник'), (2, 'Вторник'), (3, 'Сряда'), (4, 'Четвъртък'), (5, 'Петък'), (6, 'Събота'), (7, 'Неделя')]

    id = sa.Column(sa.Integer, primary_key=True)
    week = sa.Column(sa.String)
    weekday = sa.Column(sa.Integer, value_expr = values(column('id', sa.Integer), column('name', sa.String), name="my_values").data(MY_VALUES), nullable=False)
    employee = sa.Column(sa.Integer, sa.ForeignKey('employees.id'), nullable=False)
    working_hours = sa.Column(sa.Integer, sa.ForeignKey('working_hours.id'), nullable=False)