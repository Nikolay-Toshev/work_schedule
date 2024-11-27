import os
import db_setup
from db_queries import session
from gui_interface import App
from tkinter import Tk


if not os.path.exists('work_schedule.db'):
    db_setup.Base.metadata.create_all(db_setup.engine)
    add_default_working_hour = db_setup.WorkingHours(
        is_resting = True,
        start_hour = '24:00',
        end_hour = '24:00',
        working_hours = 0,
    )
    session.add(add_default_working_hour)
    session.commit()

root = Tk()
App(root)
root.mainloop()