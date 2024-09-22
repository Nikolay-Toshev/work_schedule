import db_setup as db
from sqlalchemy.orm import sessionmaker

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


def remove_employee(employee):

    employee_to_delete = session.query(db.Employee).filter(db.Employee.name == employee).first()

    if employee_to_delete is not None:
        session.delete(employee_to_delete)
        session.commit()


def list_employees():
    all_employees = []
    employees = session.query(db.Employee).all()

    for employee in employees:
        all_employees.append(employee.name)

    all_employees_str = '\n'.join(all_employees)

    return all_employees_str


if __name__ == '__main__':
    list_employees()