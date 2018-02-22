import datetime
import re
import utils

from task import Task


class TaskSearch(Task):
    """This class extends the Task class and provides all different methods to
    search through a list of tasks, to return the ones that meet the
    requirements
    """

    @classmethod
    def search_date(cls, tasks):
        """Returns a list of tasks that match the exact date the user gives."""
        utils.clear_screen()
        found = []

        # Asks the user to provide a date with the valid format
        while True:
            print("Enter the date")
            date = input("Please use DD/MM/YYYY: ")
            try:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            except ValueError:
                print("Sorry, you must enter a valid date.\n")
            else:
                break

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if task.date == date:
                found.append(task)

        if len(found) > 0:
            return found
        else:
            print("Sorry, we haven't found a task for that day")
            input("\nPress enter to return to menu")
            return None

    @classmethod
    def search_by_range(cls, tasks):
        """Returns a list of tasks that are included between the two dates
        provided by the user.
        """
        utils.clear_screen()
        found = []

        # Asks the user to provide a start date with the valid format.
        while True:
            print("Enter the start date")
            start_date = input("Please use DD/MM/YYYY: ")
            try:
                start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
            except ValueError:
                print("Sorry, you must enter a valid date.\n")
            else:
                break

        # Asks the user to provide an end date with the valid format.
        while True:
            print("\nEnter the end date")
            end_date = input("Please use DD/MM/YYYY: ")
            try:
                end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
            except ValueError:
                print("Sorry, you must enter a valid date.\n")
            else:
                break

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if task.date >= start_date and task.date <= end_date:
                found.append(task)

        if len(found) > 0:
            return found
        else:
            print("Sorry, we haven't found a task for that range")
            input("\nPress enter to return to menu")
            return None

    @classmethod
    def search_time(cls, tasks):
        """Returns a list of tasks that match the same time spent provided by
        the user.
        """
        utils.clear_screen()
        found = []

        # Asks the user to provide a valid numeric integer time.
        while True:
            try:
                time = round(int(input("Enter time spent(rounded minutes): ")))
                if time <= 0:
                    raise ValueError
            except ValueError:
                print("Sorry, you must enter a valid numeric time.\n")
            else:
                time = str(time)
                break

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if task.time == time:
                found.append(task)

        if len(found) > 0:
            return found
        else:
            print("Sorry, we haven't found a task for that time spent")
            input("\nPress enter to return to menu")
            return None

    @classmethod
    def search_exact(cls, tasks):
        """Returns a list of tasks that match the same text given by the user
        both within the Title or Notes (if task have it).
        """
        utils.clear_screen()
        found = []

        # Ask the user to provide a string or character. Can't leave it blank.
        while True:
            text = input("Enter a string to search on Title/Notes: ").lower()
            if text != '':
                # Fills a list with the tasks found (if any)
                for t in tasks:
                    # Checks if notes is empty
                    if t.notes:
                        if text in t.title.lower() or text in t.notes.lower():
                            found.append(t)
                    else:
                        if text in t.title.lower():
                            found.append(t)

                if len(found) > 0:
                    return found
                else:
                    print("Sorry, there's no tasks containing that text")
                    input("\nPress enter to return to menu")
                    return None
            else:
                print("Sorry, you can't leave this blank.\n")

    @classmethod
    def search_regex(cls, tasks):
        """Returns a list of tasks that match the regular expression given by
        the user. Only valid regex expression are allow to be used.
        """
        utils.clear_screen()
        found = []

        # Ask the user to provide a regular expresion
        while True:
            try:
                text = (input("Enter a regular expression to search: "))
                if text == '':
                    raise ValueError
                reg = re.compile(r'{}'.format(text))
            except re.error:
                print("Sorry, you must enter a valid regular expression\n")
            except ValueError:
                print("Sorry, you can't leave this blank.\n")
            else:
                break

        # Fills a list with the tasks found (if any)
        for task in tasks:
            # Checks if notes is empty
            if task.notes:
                if re.search(reg, task.title) or re.search(reg, task.notes):
                    found.append(task)
            else:
                if re.search(reg, task.title):
                    found.append(task)

        if len(found) > 0:
            return found
        else:
            print("Sorry, no tasks match that regular expression.")
            input("\nPress enter to return to menu")
            return None
