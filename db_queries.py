
import db_setup as db
from sqlalchemy.orm import sessionmaker, joinedload
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


def get_employees():
    return session.query(db.Employee).all()


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

    working_hours_to_delete = None

    if radio_var == 0:
        working_hours_to_delete = (session
                                   .query(db.WorkingHours)
                                   .filter(
                                        db.WorkingHours.start_hour == db_start_hour,
                                        db.WorkingHours.end_hour == db_end_hour,
                                        db.WorkingHours.is_on_vacation == 0,
                                        db.WorkingHours.is_sick == 0, db.WorkingHours.is_resting == 0,)
                                   .first())

    if radio_var == 1:
        working_hours_to_delete = (session
                                   .query(db.WorkingHours)
                                   .filter(db.WorkingHours.is_on_vacation == 1,)
                                   .first())

    if radio_var == 2:
        working_hours_to_delete = (session
                                   .query(db.WorkingHours)
                                   .filter(db.WorkingHours.is_sick == 1,)
                                   .first())

    if radio_var == 3:
        working_hours_to_delete = (session
                                   .query(db.WorkingHours)
                                   .filter(db.WorkingHours.is_resting == 1,)
                                   .first())

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
                f'{"  Отпуск," if work_hour.is_on_vacation == 1 else ""}'
                f'{"  Болничен," if work_hour.is_sick == 1 else ""}'
                f'{"  Почива," if work_hour.is_resting == 1 else ""}'
                f' Отработени часове: {work_hour.working_hours}'
            )

        else:
            all_working_hours.append(
                f'  {work_hour.start_hour} - {work_hour.end_hour}, '
                f'Отработени часове: {work_hour.working_hours}'
            )

    all_working_hours_str = '\n'.join(all_working_hours)

    return all_working_hours_str


def get_work_hours():
    all_working_hours = []
    working_hours = session.query(db.WorkingHours).all()

    for work_hour in working_hours:
        if work_hour.is_on_vacation == 1 or work_hour.is_sick == 1 or work_hour.is_resting == 1:
            all_working_hours.append(
                f'{"Отпуск" if work_hour.is_on_vacation == 1 else ""}'
                f'{"Болничен" if work_hour.is_sick == 1 else ""}'
                f'{"Почива" if work_hour.is_resting == 1 else ""}'
            )

        else:
            all_working_hours.append(
                f'{work_hour.start_hour} - {work_hour.end_hour}'
            )

    return all_working_hours


def add_week_schedule(add_remove_week_schedule_entry, drop_down_var, option_menus, employees):

    schedule_name = add_remove_week_schedule_entry.get()
    if schedule_name == '':
        # print('1')  # for debug
        return

    week_day = drop_down_var.get()
    if week_day == 'Избери':
        # print('2')  # for debug
        return

    employees_list = [employee.cget('text') for employee in employees]
    work_hours = [option.get() for option in option_menus]

    if 'Избери' in work_hours:
        # print('3')  # for debug
        return

    for i in range(len(employees_list)):

        empl = (session
                .query(db.Employee)
                .filter(db.Employee.name == employees_list[i])
                .first())

        if not (session
                .query(db.WeekSchedule)
                .filter(
                    db.WeekSchedule.week == schedule_name,
                    db.WeekSchedule.weekday == week_day,
                    db.WeekSchedule.employee == empl.id)
                .first()):

            try:
                start_hour, end_hour = work_hours[i].split(' - ')
                # print(start_hour, end_hour)  # for debug
                work_hour = (session
                             .query(db.WorkingHours)
                             .filter(
                                db.WorkingHours.start_hour == start_hour,
                                db.WorkingHours.end_hour == end_hour)
                             .first())

                line = db.WeekSchedule(
                    week=schedule_name,
                    weekday=week_day,
                    employee=empl.id,
                    working_hours=work_hour.id,
                )

                # print(line.working_hours)  # for debug
            except ValueError:

                non_working_days = {
                    'Болничен' : db.WorkingHours.is_sick == 1,
                    'Отпуск' : db.WorkingHours.is_on_vacation == 1,
                    'Почива' : db.WorkingHours.is_resting == 1,
                }

                work_hour = (session
                             .query(db.WorkingHours)
                             .filter(non_working_days[work_hours[i]])
                             .first())

                line = db.WeekSchedule(
                    week=schedule_name,
                    weekday=week_day,
                    employee=empl.id,
                    working_hours=work_hour.id
                )
                # print(line.working_hours) # for debug

            session.add(line)
            session.commit()

        else:
            line = (session
                    .query(db.WeekSchedule)
                    .filter(
                        db.WeekSchedule.week == schedule_name,
                        db.WeekSchedule.weekday == week_day,
                        db.WeekSchedule.employee == empl.id)
                    .first())
            try:
                start_hour, end_hour = work_hours[i].split(' - ')
                work_hour = (session
                             .query(db.WorkingHours)
                             .filter(
                                db.WorkingHours.start_hour == start_hour,
                                db.WorkingHours.end_hour == end_hour)
                             .first())

                line.working_hours=work_hour.id

            except ValueError:

                non_working_days = {
                    'Болничен': db.WorkingHours.is_sick == 1,
                    'Отпуск': db.WorkingHours.is_on_vacation == 1,
                    'Почива': db.WorkingHours.is_resting == 1,
                }

                work_hour = (session
                             .query(db.WorkingHours)
                             .filter(non_working_days[work_hours[i]])
                             .first())

                line.working_hours=work_hour.id

            session.commit()
    return



def remove_week_schedule(week_schedule):
    lines_to_remove = (session
                       .query(db.WeekSchedule)
                       .filter(db.WeekSchedule.week == week_schedule)
                       .all())

    for line in lines_to_remove:
        session.delete(line)

    session.commit()


def list_week_schedule(week_schedule):
    filled_days = []
    lines_to_display = (session
                        .query(db.WeekSchedule)
                        .filter(db.WeekSchedule.week == week_schedule)
                        .order_by(db.WeekSchedule.id)
                        .group_by(db.WeekSchedule.weekday)
                        .all())

    for line in lines_to_display:
        filled_days.append(f'{line.weekday} е попълнен.')

    return '\n'.join(filled_days)


def list_week_schedule_name():
    week_schedules = (session
                          .query(db.WeekSchedule)
                          .group_by(db.WeekSchedule.week)
                          .all())

    week_schedules_names = [week.week for week in week_schedules]

    return week_schedules_names


def check_week_schedule(week_schedule, weekday):

    if week_schedule == 'Избери' or weekday == 'Избери':
        return

    weekday_schedule_employees = (session
                                  .query(db.WeekSchedule)
                                  .filter(db.WeekSchedule.weekday == weekday, db.WeekSchedule.week == week_schedule))

    for employee_schedule in weekday_schedule_employees:
        employee = session.query(db.Employee).filter(db.Employee.id == employee_schedule.employee).first()
        work_hours = session.query(db.WorkingHours).filter(db.WorkingHours.id == employee_schedule.working_hours).first()

        # need to be returned in format {employee.name} : {work_hours.start_hour} - {work_hours.end_hour} or {not working options like 'is_sick'}
    return


if __name__ == '__main__':
    pass