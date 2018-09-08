import datetime
import os


def clear_screen():
    """Clear the screen to prepare it to show the menu."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_date(initial=None):
    """
    Gets a valid date from user. If no date provided, it returns
    the initial date or None.
    """
    if not initial:
        clear_screen()
    while True:
        print("Date of the task")
        date = input("Please use DD/MM/YYYY: ")
        if date == '' and initial:
            return initial
        try:
            date = datetime.datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            return date.date()


def get_date_range():
    """
    Gets a valid date from user. If no date provided, it returns
    the initial date or None.
    """
    clear_screen()
    while True:
        print("Enter the start date")
        start_date = input("Please use DD/MM/YYYY: ")
        try:
            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            break

    while True:
        print("Enter the end date")
        end_date = input("Please use DD/MM/YYYY: ")
        try:
            end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            return start_date.date(), end_date.date()


def get_title(initial=None):
    """
    Gets a valid title from user. If no title provided, it returns
    the initial title or None.
    """
    if not initial:
        clear_screen()
    while True:
        title = input("Title of the task: ")
        if title != '':
            return title
        if initial:
            return initial
        print("Sorrry, you must provide a task title")


def get_time(initial=None):
    """
    Gets a valid time spent from user. If no time provided, it returns
    the initial time spent or None.
    """
    if not initial:
        clear_screen()
    while True:
        time = input("Time spent (rounded minutes): ")
        if time == '' and initial:
            return initial
        try:
            time = round(int(time))
            if time <= 0:
                raise ValueError
        except ValueError:
            print("Sorry, you must enter a valid numeric time")
        else:
            return str(time)


def get_notes(initial=None):
    """
    Gets notes from user. If no notes provided, it returns the initial
    notes or None.
    """
    if not initial:
        clear_screen()
    notes = input("Notes (Optional, you can leave this empty): ")
    if notes:
        return notes
    return ''
