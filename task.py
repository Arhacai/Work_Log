import datetime
import utils


class Task:
    """Contains relevant info about a task. This info is: Date, Title,
    Time spent and Notes (which are optional). An object of this type can
    show its info properly on screen and can be created on the fly by asking
    the user to fill its attributes.
    """
    def __init__(self, log):
        """Initialize an instance of Task with needed attributes"""
        self.log = log
        self.date = datetime.datetime.strptime(log["Date"], '%d/%m/%Y')
        self.title = log["Title"]
        self.time = log["Time"]
        if log["Notes"] == '':
            self.notes = None
        else:
            self.notes = log["Notes"]

    def show_task(self):
        """Prompts on screen the info about the task"""
        utils.clear_screen()
        print("Date: {}".format(self.date.strftime('%d/%m/%Y')))
        print("Title: {}".format(self.title))
        print("Time spent: {}".format(self.time))
        if self.notes:
            print("Notes: {}".format(self.notes))
        print()

    @classmethod
    def create_new_task(cls):
        """Let the user to create a new task by being asked to fill all the
        required attributes and returns an object o class Task with this
        attributes set.
        """
        log = {}

        # Gets a valid date from user
        utils.clear_screen()
        while True:
            print("Date of the task")
            date = input("Please use DD/MM/YYYY: ")
            try:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            except ValueError:
                print("Sorry, you must enter a valid date.\n")
            else:
                log["Date"] = date.strftime('%d/%m/%Y')
                break

        # Gets the title of the task
        utils.clear_screen()
        while True:
            title = input("Title of the task: ")
            if title != '':
                log["Title"] = title
                break
            else:
                print("Sorry, you must provide a task title.")

        # Gets a valid time spent
        utils.clear_screen()
        while True:
            try:
                time = round(int(input("Time spent (rounded minutes): ")))
                if time <= 0:
                    raise ValueError
            except ValueError:
                print("Sorry, you must enter a valid numeric time")
            else:
                log["Time"] = str(time)
                break

        # Gets notes for the task (optional)
        utils.clear_screen()
        notes = input("Notes (Optional, you can leave this empty): ")
        if notes == '':
            log["Notes"] = None
        else:
            log["Notes"] = notes

        return cls(log)

    @classmethod
    def edit_task(cls, entry):
        """Let the user to edit a task by being asked to edit any of the
        fields that set their attributes. If any field is left blank the task
        won't change it.
        """
        log = {}

        # Prompts on screen the task that is going to be edited.
        entry.show_task()

        print("EDIT entry (Leave fields blank for no changes)")

        # Let the user edit the task's date
        while True:
            print("New date:")
            date = input("Please use DD/MM/YYY: ")
            if date == '':
                log["Date"] = entry.date.strftime('%d/%m/%Y')
                break
            else:
                try:
                    date = datetime.datetime.strptime(date, '%d/%m/%Y')
                except ValueError:
                    print("Sorry, you must enter a valid date.\n")
                else:
                    log["Date"] = date.strftime('%d/%m/%Y')
                    break

        # Let the user edit the task's title
        title = input("New title: ")
        if title != '':
            log["Title"] = title
        else:
            log["Title"] = entry.title

        # Let the user edit the time spent on the task
        while True:
            time = input("New time spent (rounded minutes): ")
            if time == '':
                log["Time"] = entry.time
                break
            else:
                try:
                    time = round(int(time))
                    if time <= 0:
                        raise ValueError
                except ValueError:
                    print("Sorry, you must enter a valid numeric time")
                else:
                    log["Time"] = str(time)
                    break

        # Let the user edit the task's notes
        notes = input("New notes (Optional, you can leave this empty): ")
        if notes != '':
            log["Notes"] = notes
        else:
            log["Notes"] = entry.notes

        return cls(log)
