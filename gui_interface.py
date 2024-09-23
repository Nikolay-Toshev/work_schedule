from tkinter import Button, Label, Entry, Tk, Text, Scrollbar, IntVar, Radiobutton
from tktimepicker import SpinTimePickerOld, constants

from db_queries import add_employee, remove_employee, list_employees, add_working_hours, list_working_hours, \
    remove_working_hours


def refresh_data(text, func):
    text.delete('1.0', 'end')
    text.insert('1.0', str(func))


class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x900")
        self.master.resizable(True, True)
        self.master.title("My GUI")
        self.main_page()

    def winfo_children_destroy(self):
        for i in self.master.winfo_children():
            i.destroy()

    def main_page(self):
        self.winfo_children_destroy()

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.columnconfigure(2, weight=2)
        self.master.columnconfigure(3, weight=1)

        add_employee_btn = Button(self.master, text="Добави/Премахни Работник", font=('Arial', 18), command=self.add_remove_employee)
        add_employee_btn.grid(row=0, column=3, sticky="EW", padx=15, pady=30, columnspan=2)

        add_btn = Button(self.master, text="Добави/Премахни работни часове", font=('Arial', 18), command=self.add_remove_workhours)
        add_btn.grid(row=1, column=3, sticky="EW", padx=15, columnspan=2)

        add_week_schedule_btn = Button(self.master, text="Добави работна седмица", font=('Arial', 18), command=self.add_week_schedule)
        add_week_schedule_btn.grid(row=2, column=3, sticky="EW", padx=15, pady=30, columnspan=2)


    def add_remove_employee(self):
        self.winfo_children_destroy()

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.columnconfigure(2, weight=2)
        self.master.columnconfigure(3, weight=1)

        add_employee_label = Label(self.master, text='Добави нов работник', font=('Arial', 18))
        add_employee_label.grid(row=0, column=0, sticky="E", padx=15, pady=30)

        add_employee_entry = Entry(self.master, font=('Arial', 18))
        add_employee_entry.grid(row=0, column=1, sticky="WE", padx=15, pady=30)

        add_btn = Button(self.master, text='Добави',font=('Arial', 18), command= lambda :(add_employee(add_employee_entry.get()), add_employee_entry.delete(0, 'end')))
        add_btn.grid(row=0, column=2, sticky="WE", padx=15, pady=30)

        remove_employee_label = Label(self.master, text='Премахни работник', font=('Arial', 18))
        remove_employee_label.grid(row=1, column=0, sticky="E", padx=15, pady=10)

        remove_employee_entry = Entry(self.master, font=('Arial', 18))
        remove_employee_entry.grid(row=1, column=1, sticky="EW", padx=15, pady=10)

        remove_btn = Button(self.master, text='Премахни', font=('Arial', 18), command=lambda: (remove_employee(remove_employee_entry.get()), remove_employee_entry.delete(0, 'end')))
        remove_btn.grid(row=1, column=2, sticky="WE", padx=15, pady=10)

        employees_label = Label(self.master, text='Регистрирани работници', font=('Arial', 18), borderwidth=1, relief="solid")
        employees_label.grid(row=2, column=0, padx=15, pady=30, sticky="EW", columnspan=2)

        sc = Scrollbar(self.master, orient='vertical')
        sc.grid(row=3, column=0, sticky='nse', columnspan=2, rowspan=2)
        employee_list_text = Text(self.master, font=('Arial', 18), width=1, height=10, yscrollcommand=sc.set)
        employee_list_text.insert('1.0', str(list_employees()))
        sc.config(command=employee_list_text.yview)
        employee_list_text.grid(row=3, column=0, padx=15, columnspan=2, rowspan=2, sticky="EWNS")

        refresh_btn = Button(self.master, text='Опресни', command=lambda : refresh_data(employee_list_text, list_employees()), font=('Arial', 18))
        refresh_btn.grid(row=2, column=2, padx=15, pady=30, sticky="WE")

        main_page_btn = Button(self.master, text="Назад", command=self.main_page, font=('Arial', 18))
        main_page_btn.grid(row=4, column=2, sticky="EWS", padx=15)


    def add_remove_workhours(self):
        self.winfo_children_destroy()

        start_hour_label = Label(self.master, text='Начален час', font=('Arial', 18))
        start_hour_label.grid(row=0, column=0, sticky="E", padx=15, pady=30)

        start_hour_entry = SpinTimePickerOld(self.master)
        start_hour_entry.addAll(constants.HOURS24)
        start_hour_entry.grid(row=0, column=1, sticky="W", pady=30)

        end_hour_label = Label(self.master, text='Краен час', font=('Arial', 18))
        end_hour_label.grid(row=1, column=0, sticky="E", padx=15)

        end_hour_entry = SpinTimePickerOld(self.master)
        end_hour_entry.addAll(constants.HOURS24)
        end_hour_entry.grid(row=1, column=1, sticky="W")

        radiobutton_var = IntVar(master=self.master, value=0)

        is_on_vacation_radiobtn = Radiobutton(self.master, text='Отпуск', variable=radiobutton_var, value=1, font=('Arial', 18), )
        is_on_vacation_radiobtn.grid(row=2, column=0, sticky="E", pady=30,)

        is_sick_radiobtn = Radiobutton(self.master, text='Болничен', variable=radiobutton_var, value=2, font=('Arial', 18))
        is_sick_radiobtn.grid(row=2, column=1, sticky="W",)

        add_btn = Button(self.master, text='Добави', font=('Arial', 18), command=lambda: (
            add_working_hours(start_hour_entry.time(), end_hour_entry.time(), radiobutton_var.get()),
        ))
        add_btn.grid(row=0, column=2, sticky="WE", padx=15, pady=30)

        remove_btn = Button(self.master, text='Премахни', font=('Arial', 18), command=lambda: (
            remove_working_hours(start_hour_entry.time(), end_hour_entry.time(), radiobutton_var.get()),
        ))
        remove_btn.grid(row=1, column=2, sticky="WE", padx=15)

        sc = Scrollbar(self.master, orient='vertical')
        sc.grid(row=3, column=0, sticky='nse', columnspan=2, rowspan=2)
        work_hours_list_text = Text(self.master, font=('Arial', 18), width=1, height=10, yscrollcommand=sc.set)
        work_hours_list_text.insert('1.0', str(list_working_hours()))
        sc.config(command=work_hours_list_text.yview)
        work_hours_list_text.grid(row=3, column=0, padx=15, columnspan=2, rowspan=2, sticky="EWNS")

        refresh_btn = Button(self.master, text='Опресни', command=lambda: refresh_data(work_hours_list_text, list_working_hours()),
                             font=('Arial', 18))
        refresh_btn.grid(row=2, column=2, padx=15, pady=30, sticky="WE")

        main_page_btn = Button(self.master, text="Назад", command=self.main_page, font=('Arial', 18))
        main_page_btn.grid(row=4, column=2, sticky="EWS", padx=15)


    def add_week_schedule(self):
        self.winfo_children_destroy()

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        main_page_btn = Button(self.master, text="Назад", command=self.main_page)
        main_page_btn.grid(row=0, column=1, sticky="E", padx=15, pady=15)








if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()