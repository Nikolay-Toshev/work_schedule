import time

import db_setup as db
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind = db.engine)
session = Session()


def add_employee(employee):
    if not employee:
        return

    if session.query(db.Employee).filter(db.Employee.name == employee).first():
        return

    new_employee = db.Employee(name = employee)

    session.add(new_employee)
    session.commit()

    return


def remove_employee(employee):
    employee_to_delete = session.query(db.Employee).filter(db.Employee.name == employee).first()

    if employee_to_delete is not None:
        session.delete(employee_to_delete)
        session.commit()

    return


def list_employees():
    all_employees = []
    employees = session.query(db.Employee).all()

    for employee in employees:
        all_employees.append(f'  {employee.name}')

    all_employees_str = '\n'.join(all_employees)

    return all_employees_str


def add_working_hours(start_hour, end_hour, radio_var):
    db_start_hour = f'{start_hour[0]}:{start_hour[1]:02d}'
    db_end_hour = f'{end_hour[0]}:{end_hour[1]:02d}'

    start_hour_obj = datetime.strptime(db_start_hour, '%H:%M')
    end_hour_obj = datetime.strptime(db_end_hour, '%H:%M')

    working_hours = end_hour_obj - start_hour_obj
    db_working_hours =  working_hours.total_seconds() / 3600

    new_working_hours = db.WorkingHours(
        start_hour = db_start_hour,
        end_hour = db_end_hour,
        working_hours = db_working_hours
    )

    if radio_var == 1:
        if session.query(db.WorkingHours).filter(db.WorkingHours.is_on_vacation == 1).first():
            return
        new_working_hours.is_on_vacation = True
        new_working_hours.start_hour = '0:00'
        new_working_hours.end_hour = '8:00'
        new_working_hours.working_hours = 8

    if radio_var == 2:
        if session.query(db.WorkingHours).filter(db.WorkingHours.is_sick == 1).first():
            return
        new_working_hours.is_sick = True
        new_working_hours.start_hour = '0:00'
        new_working_hours.end_hour = '8:00'
        new_working_hours.working_hours = 8

    if radio_var == 3:
        if session.query(db.WorkingHours).filter(db.WorkingHours.is_resting == 1).first():
            return
        new_working_hours.is_resting = True
        new_working_hours.start_hour = '0:00'
        new_working_hours.end_hour = '0:00'
        new_working_hours.working_hours = 0

    if session.query(db.WorkingHours).filter(
            db.WorkingHours.start_hour == db_start_hour,
            db.WorkingHours.end_hour == db_end_hour,
            db.WorkingHours.is_sick == 0,
            db.WorkingHours.is_on_vacation == 0,
            db.WorkingHours.is_resting ==0,
        ).first() and radio_var == 0:
        return


    session.add(new_working_hours)
    session.commit()

    return


def remove_working_hours(start_hour, end_hour, radio_var):

    db_start_hour = f'{start_hour[0]}:{start_hour[1]:02d}'
    db_end_hour = f'{end_hour[0]}:{end_hour[1]:02d}'

    if radio_var == 0:
        working_hours_to_delete = session.query(db.WorkingHours).filter(
            db.WorkingHours.start_hour == db_start_hour,
            db.WorkingHours.end_hour == db_end_hour,
            db.WorkingHours.is_on_vacation == 0,
            db.WorkingHours.is_sick == 0,
            db.WorkingHours.is_resting == 0,
        ).first()

    if radio_var == 1:
        working_hours_to_delete = session.query(db.WorkingHours).filter(
            db.WorkingHours.is_on_vacation == 1,
        ).first()

    if radio_var == 2:
        working_hours_to_delete = session.query(db.WorkingHours).filter(
            db.WorkingHours.is_sick == 1,
        ).first()

    if radio_var == 3:
        working_hours_to_delete = session.query(db.WorkingHours).filter(
            db.WorkingHours.is_resting == 1,
        ).first()

    if working_hours_to_delete is not None:
        session.delete(working_hours_to_delete)
        session.commit()

    return


def list_working_hours():
    all_working_hours= []
    working_hours = session.query(db.WorkingHours).all()

    for work_hour in working_hours:
        if work_hour.is_on_vacation == 1 or work_hour.is_sick == 1 or work_hour.is_resting == 1:
            all_working_hours.append(
                f'{"  Отпуск" if work_hour.is_on_vacation == 1 else ""}'
                f'{"  Болничен" if work_hour.is_sick == 1 else ""}'
                f'{"  Почива" if work_hour.is_resting == 1 else ""}'
            )

        else:
            all_working_hours.append(
                f'  {work_hour.start_hour} - {work_hour.end_hour}, '
                f'Отработени часове: {work_hour.working_hours}'
            )

    all_working_hours_str = '\n'.join(all_working_hours)

    return all_working_hours_str

if __name__ == '__main__':
    pass