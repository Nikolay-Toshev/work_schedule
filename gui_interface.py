import tkinter as tk
from tkinter import Button, Label, Entry, Tk, Text, Scrollbar, IntVar, Radiobutton, StringVar, OptionMenu

from PIL.ImageOps import expand
from tktimepicker import SpinTimePickerOld, constants

from db_queries import add_employee, remove_employee, list_employees, add_working_hours, list_working_hours, \
    remove_working_hours, add_week_schedule, remove_week_schedule, list_week_schedule, get_employees, get_work_hours, \
    list_week_schedule_name, check_week_schedule, update_week_schedule, add_month, list_employee_names, list_week_names
from xls_table_create_and_modify import create_table, wb


def refresh_data(text, func):
    text.delete('1.0', 'end')
    text.insert('1.0', str(func))


class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x800")
        self.master.resizable(True, True)
        self.master.title("Седмичен график")
        self.main_page()

    drop_down_vars_weeks = {}
    option_menu_weeks = {}
    week_labels = {}

    def create_canvas(self):

        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=1)

        my_canvas = tk.Canvas(main_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        my_scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda event: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

        secondary_frame = tk.Frame(my_canvas)

        my_canvas.create_window((0, 0), window=secondary_frame, anchor=tk.NW)
        secondary_frame.bind('<Configure>', lambda event: my_canvas.configure(scrollregion=my_canvas.bbox("all")), )

        secondary_frame.columnconfigure(0, weight=1)
        secondary_frame.columnconfigure(1, weight=3)
        secondary_frame.columnconfigure(2, weight=3)
        secondary_frame.columnconfigure(3, weight=3)

        return secondary_frame
    
    def delete_labels_and_option_menus_weeks(self):
        self.drop_down_vars_weeks = {}
        for key in self.option_menu_weeks:
            self.option_menu_weeks[key].destroy()
        for key in self.week_labels:
            self.week_labels[key].destroy()

    def winfo_children_destroy(self):
        for i in self.master.winfo_children():
            i.destroy()

    @staticmethod
    def create_labels(row, col, window):
        grid_row = row
        grid_col = col
        all_employees = get_employees()

        employees_labels = {}

        for i in range(len(all_employees)):

            employees_labels[i] = Label(window, text=all_employees[i].name, font=('Arial', 18))
            employees_labels[i].grid(row=grid_row, column=grid_col, sticky="E", padx=15, pady=15)
            grid_row += 1

        return employees_labels.values()

    @staticmethod
    def create_option_menu(row, col, window):

        grid_row = row
        grid_col = col
        all_employees = get_employees()

        drop_down_vars = {}
        option_menu = {}

        options = get_work_hours()

        for i in range(len(all_employees)):

            drop_down_vars[i] = StringVar(window)
            drop_down_vars[i].set('Избери')

            option_menu[i] = OptionMenu(window, drop_down_vars[i], *options)
            option_menu[i].config(font=('Arial', 18))
            option_menu[i].grid(row=grid_row, column=grid_col, sticky="WE")
            grid_row += 1

        return drop_down_vars.values()

    def create_labels_and_option_menu_weeks(self, row, col, month, window):

        if month == None:
            return

        self.delete_labels_and_option_menus_weeks()

        grid_row = row
        grid_col = col

        options = list_week_schedule_name()

        week_number = 1

        for i in range(len(month)):
            if month[i][1] == "Понеделник" or month[i][0] == 1:

                self.drop_down_vars_weeks[week_number] = StringVar(window)
                self.drop_down_vars_weeks[week_number].set('Избери')

                self.option_menu_weeks[week_number] = OptionMenu(window, self.drop_down_vars_weeks[week_number], *options)
                self.option_menu_weeks[week_number].config(font=('Arial', 18))
                self.option_menu_weeks[week_number].grid(row=grid_row, column=grid_col + 1, sticky="WE")

                self.week_labels[week_number] = Label(window, text=f'week {week_number}', font=('Arial', 18))
                self.week_labels[week_number].grid(row=grid_row, column=grid_col, sticky="E", padx=15, pady=30)

                week_number += 1
                grid_row += 1

        return self.drop_down_vars_weeks.values()

    @staticmethod
    def refresh_options(var, option, choices):
        var.set('')
        option['menu'].delete(0, 'end')
        for choice in choices:
            option['menu'].add_command(label=choice, command=tk._setit(var, choice))

    def main_page(self):
        self.winfo_children_destroy()

        window = self.create_canvas()

        add_employee_btn = Button(window, text="Добави/Премахни Работник", font=('Arial', 18), command=self.add_remove_employee)
        add_employee_btn.grid(row=0, column=3, sticky="EW", padx=15, pady=30, columnspan=2)

        add_btn = Button(window, text="Добави/Премахни работни часове", font=('Arial', 18), command=self.add_remove_workhours)
        add_btn.grid(row=1, column=3, sticky="EW", padx=15, columnspan=2)

        add_week_schedule_btn = Button(window, text="Добави/Премахни седмичен график", font=('Arial', 18), command=self.add_remove_week_schedule)
        add_week_schedule_btn.grid(row=2, column=3, sticky="EW", padx=15, pady=30, columnspan=2)

        check_week_schedule_btn = Button(window, text="Прегледай/Промени седмичен график", font=('Arial', 18), command=self.check_edit_week_schedule)
        check_week_schedule_btn.grid(row=3, column=3, sticky="EW", padx=15, columnspan=2)

        create_week_schedule_btn = Button(window, text="Създай месечен график", font=('Arial', 18),
                                         command=self.create_month_schedule)
        create_week_schedule_btn.grid(row=4, column=3, sticky="EW", padx=15, pady= 30, columnspan=2)

    def add_remove_employee(self):
        self.winfo_children_destroy()

        window = self.create_canvas()

        all_employees = ['Избери']
        all_employees += list_employee_names()

        add_employee_label = Label(window, text='Добави нов работник', font=('Arial', 18))
        add_employee_label.grid(row=0, column=0, sticky="E", padx=15, pady=30)

        add_employee_entry = Entry(window, font=('Arial', 18))
        add_employee_entry.grid(row=0, column=1, sticky="WE", padx=15, pady=30)

        add_btn = Button(window, text='Добави',font=('Arial', 18), command= lambda :(
            add_employee(add_employee_entry.get()),
            all_employees.append(add_employee_entry.get()),
            add_employee_entry.delete(0, 'end'),
            refresh_data(employee_list_text, list_employees()),
            self.refresh_options(drop_down_employee_name, employee_name_option, all_employees),
            drop_down_employee_name.set(all_employees[0]),
        ))

        add_btn.grid(row=0, column=3, sticky="WE", padx=15, pady=30)

        remove_employee_label = Label(window, text='Премахни работник', font=('Arial', 18))
        remove_employee_label.grid(row=1, column=0, sticky="E", padx=15, pady=10)

        drop_down_employee_name = StringVar(window)
        drop_down_employee_name.set(all_employees[0])

        employee_name_option = OptionMenu(window, drop_down_employee_name, *all_employees)
        employee_name_option.config(font=('Arial', 18))
        employee_name_option.grid(row=1, column=1, sticky="WE")

        remove_btn = Button(window, text='Премахни', font=('Arial', 18), command=lambda: (
            remove_employee(drop_down_employee_name.get()),
            (all_employees.remove(drop_down_employee_name.get()) if drop_down_employee_name.get() != 'Избери' else None),
            self.refresh_options(drop_down_employee_name, employee_name_option, all_employees),
            drop_down_employee_name.set(all_employees[0]),
            refresh_data(employee_list_text, list_employees()),
        ))
        remove_btn.grid(row=1, column=3, sticky="WE", padx=15, pady=10)

        employees_label = Label(window, text='Регистрирани работници', font=('Arial', 18), borderwidth=1, relief="solid")
        employees_label.grid(row=2, column=0, padx=15, pady=30, sticky="EW", columnspan=2)

        sc = Scrollbar(window, orient='vertical')
        sc.grid(row=3, column=0, sticky='nse', columnspan=2, rowspan=2)
        employee_list_text = Text(window, font=('Arial', 18), width=1, height=10, yscrollcommand=sc.set)
        employee_list_text.insert('1.0', str(list_employees()))
        sc.config(command=employee_list_text.yview)
        employee_list_text.grid(row=3, column=0, padx=15, columnspan=2, rowspan=2, sticky="EWNS")

        main_page_btn = Button(window, text="Назад", command=self.main_page, font=('Arial', 18))
        main_page_btn.grid(row=4, column=3, sticky="EWS", padx=15)

    def add_remove_workhours(self):
        self.winfo_children_destroy()

        window = self.create_canvas()

        start_hour_label = Label(window, text='Начален час', font=('Arial', 18))
        start_hour_label.grid(row=0, column=0, sticky="E", padx=15, pady=30)

        start_hour_entry = SpinTimePickerOld(window)
        start_hour_entry.addAll(constants.HOURS24)
        start_hour_entry.grid(row=0, column=1, sticky="W", pady=30, columnspan=2)

        end_hour_label = Label(window, text='Краен час', font=('Arial', 18))
        end_hour_label.grid(row=1, column=0, sticky="E", padx=15)

        end_hour_entry = SpinTimePickerOld(window)
        end_hour_entry.addAll(constants.HOURS24)
        end_hour_entry.grid(row=1, column=1, sticky="W", columnspan=2)

        radiobutton_var = IntVar(master=window, value=0)

        is_working_radiobutton = Radiobutton(window, text='Работи', variable=radiobutton_var, value=0, font=('Arial', 18), )
        is_working_radiobutton.grid(row=2, column=0, sticky="W", padx=15)

        is_on_vacation_radiobtn = Radiobutton(window, text='Отпуск', variable=radiobutton_var, value=1, font=('Arial', 18), )
        is_on_vacation_radiobtn.grid(row=2, column=1, sticky="W", pady=30,)

        is_sick_radiobtn = Radiobutton(window, text='Болничен', variable=radiobutton_var, value=2, font=('Arial', 18))
        is_sick_radiobtn.grid(row=2, column=2, sticky="W",)

        add_btn = Button(window, text='Добави', font=('Arial', 18), command=lambda: (
            add_working_hours(start_hour_entry.time(), end_hour_entry.time(), radiobutton_var.get()),
            refresh_data(work_hours_list_text, list_working_hours()),
        ))
        add_btn.grid(row=0, column=3, sticky="WE", padx=15, pady=30)

        remove_btn = Button(window, text='Премахни', font=('Arial', 18), command=lambda: (
            remove_working_hours(start_hour_entry.time(), end_hour_entry.time(), radiobutton_var.get()),
            refresh_data(work_hours_list_text, list_working_hours()),
        ))
        remove_btn.grid(row=1, column=3, sticky="WE", padx=15)

        sc = Scrollbar(window, orient='vertical')
        sc.grid(row=3, column=0, sticky='nse', columnspan=4, rowspan=2)

        work_hours_list_text = Text(window, font=('Arial', 18), width=30, height=10, yscrollcommand=sc.set)
        work_hours_list_text.insert('1.0', str(list_working_hours()))

        sc.config(command=work_hours_list_text.yview)
        work_hours_list_text.grid(row=3, column=0, padx=15, columnspan=4, rowspan=2, sticky="EWNS")

        main_page_btn = Button(window, text="Назад", command=self.main_page, font=('Arial', 18))
        main_page_btn.grid(row=5, column=3, sticky="EWS", padx=15, pady=15)

    def add_remove_week_schedule(self):

        week_names = ['Избери']
        week_names += list_week_names()

        self.winfo_children_destroy()

        window = self.create_canvas()

        add_remove_week_schedule_label = Label(window, text='Добави\nседмичен график', font=('Arial', 18))
        add_remove_week_schedule_label.grid(row=0, column=0, sticky="E", padx=15, pady=30)

        add_week_schedule_entry = Entry(window, font=('Arial', 18))
        add_week_schedule_entry.grid(row=0, column=1, sticky="WE", pady=30)

        add_btn = Button(window, text='Добави', font=('Arial', 18), command=lambda: (
            add_week_schedule(add_week_schedule_entry),
            (week_names.append(add_week_schedule_entry.get()) if add_week_schedule_entry.get() != '' else None),
            self.refresh_options(drop_down_schedule_name, schedule_name_option, week_names),
            drop_down_schedule_name.set(week_names[0]),
            add_week_schedule_entry.delete(0, 'end'),
            refresh_data(week_schedule_list_text, str('\n'.join(list_week_names())))
        ))
        add_btn.grid(row=0, column=3, sticky="WE", padx=15, pady=30)

        drop_down_schedule_name = StringVar(window)
        drop_down_schedule_name.set(week_names[0])

        schedule_name_label = Label(window, text='Премахни\nседмичен график', font=('Arial', 18))
        schedule_name_label.grid(row=1, column=0, sticky="E", padx=15)

        schedule_name_option = OptionMenu(window, drop_down_schedule_name, *week_names)
        schedule_name_option.config(font=('Arial', 18))
        schedule_name_option.grid(row=1, column=1, sticky="WE")

        remove_btn = Button(window, text='Премахни', font=('Arial', 18), command=lambda: (
            (remove_week_schedule(drop_down_schedule_name.get()) if drop_down_schedule_name.get() != 'Избери' else None),
            (week_names.remove(drop_down_schedule_name.get()) if drop_down_schedule_name.get() != 'Избери' else None),
            self.refresh_options(drop_down_schedule_name, schedule_name_option, week_names),
            drop_down_schedule_name.set(week_names[0]),
            refresh_data(week_schedule_list_text, str('\n'.join(list_week_names())))
        ))
        remove_btn.grid(row=1, column=3, sticky="WE", padx=15, pady=10)

        sc = Scrollbar(window, orient='vertical')
        sc.grid(row=3, column=0, sticky='nse', pady=15, columnspan=4, rowspan=2)

        week_schedule_list_text = Text(window, font=('Arial', 18), width=1, height=10, yscrollcommand=sc.set)
        week_schedule_list_text.insert('1.0', str('\n'.join(list_week_names())))

        sc.config(command=week_schedule_list_text.yview)
        week_schedule_list_text.grid(row=3, column=0, pady=15, padx=15 , columnspan=4, rowspan=2, sticky="EWNS")

        main_page_btn = Button(window, text="Назад", command=self.main_page, font=('Arial', 18))
        main_page_btn.grid(row=5, column=3, sticky="EWS", padx=15, pady=15)

    def check_edit_week_schedule(self):

        WEEK_DAYS = [
            'Понеделник',
            'Вторник',
            'Сряда',
            'Четвъртък',
            'Петък',
            'Събота',
            'Неделя',
        ]
        self.winfo_children_destroy()

        window = self.create_canvas()

        week_names = list_week_schedule_name()
        if week_names:
            employees = [employee.name for employee in get_employees()]

            drop_down_schedule_name = StringVar(window)
            drop_down_schedule_name.set('Избери')

            schedule_name_label = Label(window, text='Седмичен график', font=('Arial', 18))
            schedule_name_label.grid(row=0, column=0, sticky="E", padx=15, pady=15)

            schedule_name_option = OptionMenu(window, drop_down_schedule_name, *week_names)
            schedule_name_option.config(font=('Arial', 18))
            schedule_name_option.grid(row=0, column=1, sticky="WE")

            drop_down_days = StringVar(window)
            drop_down_days.set('Избери')

            days_label = Label(window, text='Избери ден', font=('Arial', 18))
            days_label.grid(row=1, column=0, sticky="E", padx=15)

            days_option = OptionMenu(window, drop_down_days, *WEEK_DAYS)
            days_option.config(font=('Arial', 18))
            days_option.grid(row=1, column=1, sticky="WE", pady=15)

            employees = self.create_labels(3, 0, window)

            option_menus = self.create_option_menu(3, 1, window)


            check_label = Button(window, text='Провери', font=('Arial', 18), command=lambda: (
                refresh_data(week_schedule_list_text, str(check_week_schedule(drop_down_schedule_name.get(), drop_down_days.get())))
            ))
            check_label.grid(row=0, column=3, sticky="EW", padx=15, columnspan=2)

            update_label = Button(window, text='Промени', font=('Arial', 18), command=lambda: (update_week_schedule(drop_down_schedule_name.get(), drop_down_days.get(), employees, option_menus)))
            update_label.grid(row=3, column=3, sticky="EW", padx=15, columnspan=2)

            sc = Scrollbar(window, orient='vertical')
            sc.grid(row=4, column=3, sticky='nse', pady=30, columnspan=2, rowspan=10)

            week_schedule_list_text = Text(window, font=('Arial', 18), width=30, height=16, yscrollcommand=sc.set)
            week_schedule_list_text.insert('1.0', str(check_week_schedule(drop_down_schedule_name.get(), drop_down_days.get()) or ''))

            sc.config(command=week_schedule_list_text.yview)
            week_schedule_list_text.grid(row=4, column=2, padx=15, pady=30, columnspan=3, rowspan=10, sticky="EWNS")

        else:
            schedule_name_label = Label(window, text='Нямате създадени седмични графици', font=('Arial', 18))
            schedule_name_label.grid(row=0, column=0, sticky="E", padx=15, pady=15)

        main_page_btn = Button(window, text="Назад", command=self.main_page, font=('Arial', 18))
        main_page_btn.grid(row=16, column=3, sticky="EWS", padx=15, columnspan=2)

    def create_month_schedule(self):

        self.winfo_children_destroy()

        window = self.create_canvas()

        months = [
            'Януари',
            'Февруари',
            'Март',
            "Април",
            'Май',
            'Юни',
            'Юли',
            'Август',
            'Септември',
            'Октомври',
            'Ноември',
            'Декември',
        ]

        years = [
            2024,
            2025,
            2026,
            2027,
            2028,
            2029,
            2030,
            2031,
            2032,
            2033,
            2034,
            2035,
            2036,
            2037,
        ]
        week_names = list_week_schedule_name()
        if week_names:
            drop_down_months = StringVar(window)
            drop_down_months.set('Избери')

            months_label = Label(window, text='Избери месец', font=('Arial', 18))
            months_label.grid(row=0, column=0, sticky="E", padx=15, pady=30)

            months_option = OptionMenu(window, drop_down_months, *months)
            months_option.config(font=('Arial', 18))
            months_option.grid(row=0, column=1, sticky="WE")

            drop_down_years = StringVar(window)
            drop_down_years.set('Избери')

            year_label = Label(window, text='Избери година', font=('Arial', 18))
            year_label.grid(row=1, column=0, sticky="E", padx=15, pady=30)

            years_option = OptionMenu(window, drop_down_years, *years)
            years_option.config(font=('Arial', 18))
            years_option.grid(row=1, column=1, sticky="WE")

            work_days_label = Label(window, text='Брой работни дни', font=('Arial', 18))
            work_days_label.grid(row=2, column=0, sticky="E", padx=15, pady=30)

            work_days_entry = Entry(window, font=('Arial', 18))
            work_days_entry.grid(row=2, column=1, sticky="WE")

            add_label = Button(window, text='Добави месец', font=('Arial', 18), command=lambda: (
                self.create_labels_and_option_menu_weeks(3, 0, add_month(drop_down_months.get(), drop_down_years.get()), window)
            ))
            add_label.grid(row=0, column=4, sticky="EW", padx=15, columnspan=2)

            generate_xls = Button(window, text='Генерирай график', font=('Arial', 18), command=lambda: (
                create_table(drop_down_years.get(), drop_down_months.get(), work_days_entry.get(), self.option_menu_weeks),
                wb.save(f"{drop_down_months.get()}_{drop_down_years.get()}.xlsx")
            ))
            generate_xls.grid(row=1, column=4, sticky="EW", padx=15, columnspan=2)

        else:
            months_label = Label(window, text='Създайте седмичен график и добавете работници\nза да използвате тази функционалност!', font=('Arial', 18))
            months_label.grid(row=0, column=0, sticky="E", padx=15, pady=30)

        main_page_btn = Button(window, text="Назад", command=self.main_page, font=('Arial', 18))
        main_page_btn.grid(row=12, column=4, sticky="EW", padx=15, columnspan=2)
