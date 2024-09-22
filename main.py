import os
import db_setup
from gui_interface import App
from tkinter import Tk


if not os.path.exists('work_schedule.db'):
    db_setup.Base.metadata.create_all(db_setup.engine)

root = Tk()
App(root)
root.mainloop()