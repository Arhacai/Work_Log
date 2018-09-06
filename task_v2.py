import datetime
import re
import utils


class Task:
    """
    Contains relevant info about a task. This info is: Date, Title,
    Time spent and Notes (which are optional). An object of this type can
    show its info properly on screen and can be created on the fly by asking
    the user to fill its attributes.
    """
    def __init__(self, **kwargs):
        """Initialize an instance of Task with needed attributes"""
        if kwargs:
            self.title = kwargs.get('Title')
            self.date = datetime.datetime.strptime(
                kwargs.get('Date'), '%d/%m/%Y').date()
            self.time = kwargs.get('Time')
            self.notes = kwargs.get('Notes')
        else:
            self.title = utils.get_title()
            self.date = utils.get_date()
            self.time = utils.get_time()
            self.notes = utils.get_notes()

    def show(self):
        """Prompts on screen the info about the task"""
        utils.clear_screen()
        print("Date: {}".format(self.date.strftime('%d/%m/%Y')))
        print("Title: {}".format(self.title))
        print("Time spent: {}".format(self.time))
        if self.notes:
            print("Notes: {}".format(self.notes))
        print()

    def edit(self):
        """
        Let the user to edit a task by being asked to edit any of the
        fields that set their attributes. If any field is left blank the task
        won't change it.
        """
        self.show()
        print("EDIT entry (Leave fields blank for no changes)")
        self.title = utils.get_title(self.title)
        self.date = utils.get_date(self.date)
        self.time = utils.get_time(self.time)
        self.notes = utils.get_notes(self.notes)

    def get_log(self):
        return self.__dict__


class TaskSearch:
    """
    This class provides all different methods to search through a list of
    tasks, to return the ones that meet the requirements
    """

    def search_date(self, tasks):
        """Returns a list of tasks that match the exact date the user gives."""
        utils.clear_screen()
        found = []

        # Asks the user to provide a date with the valid format
        search_date = utils.get_date()

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if task.date == search_date:
                found.append(task)
        return found

    def search_by_range(self, tasks):
        """
        Returns a list of tasks that are included between the two dates
        provided by the user.
        """
        utils.clear_screen()
        found = []

        # Asks the user to provide a valid range of dates
        start_date, end_date = utils.get_date_range()

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if start_date <= task.date <= end_date:
                found.append(task)
        return found

    @classmethod
    def search_time(cls, tasks):
        """
        Returns a list of tasks that match the same time spent provided by
        the user.
        """
        utils.clear_screen()
        found = []

        # Asks the user to provide a valid time spent
        time = utils.get_time()

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if task.time == time:
                found.append(task)
        return found

    def search_exact(self, tasks):
        """
        Returns a list of tasks that match the same text given by the user
        both within the Title or Notes (if task have it).
        """
        utils.clear_screen()
        found = []

        # Asks the user to provide a string to search
        text = input("Enter a string to search on Title/Notes: ").lower()

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if text in task.title.lower() or text in task.notes.lower():
                found.append(task)
        return found

    @classmethod
    def search_regex(cls, tasks):
        """Returns a list of tasks that match the regular expression given by
        the user. Only valid regex expression are allow to be used.
        """
        utils.clear_screen()
        found = []

        # Ask the user to provide a regular expresion
        while True:
            text = (input("Enter a regular expression to search: "))
            try:
                regex = re.compile(r'{}'.format(text))
            except re.error:
                print("Sorry, you must enter a valid regular expression\n")
            else:
                break

        # Fills a list with the tasks found (if any)
        for task in tasks:
            if re.search(regex, task.title) or re.search(regex, task.notes):
                found.append(task)
        return found
