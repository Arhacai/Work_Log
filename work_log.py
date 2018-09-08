import csv
import utils

from task import Task, TaskSearch


class WorkLog:
    """
    WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them several ways to search through the tasks aswell. It reads and
    save all information in a csv file.
    """

    def __init__(self, file):
        """
        Initialize the app by reading the csv file and adding all task to a
        list. If there is no file, the app runs with an empty task list.
        """
        self.file = file
        self.TASKS = self.get_tasks(file)
        self.sort_tasks()

    def get_tasks(self, file=None):
        """
        Imports a list of tasks from a csvfile if provided. It returns that
        lists sorted by date.
        """
        tasks = []
        if file:
            try:
                with open(file) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for log in reader:
                        tasks.append(Task(**log))
            except FileNotFoundError:
                pass
        return tasks

    def sort_tasks(self):
        """
        Takes the list of tasks imported from csv file and sort them by date,
        from the oldest to the newest one.
        """
        for i in range(1, len(self.TASKS)):
            j = i-1
            key = self.TASKS[i]
            while (self.TASKS[j].date > key.date) and (j >= 0):
                self.TASKS[j+1] = self.TASKS[j]
                j -= 1
            self.TASKS[j+1] = key

    def edit(self, index, tasks):
        """
        Edit a task by creating one new and overriding its attributed when
        needed. It replaces the original task and then the tasks are saved
        to file. It returns the task to being able to see it on screen.
        """
        tasks[index].edit()
        self.save_file()
        return index

    def delete(self, index, tasks):
        """Let the user to delete an entry. User must confirm this action
        because it can't be undone. Once the entry is deleted, the file is
        saved with the changes made.
        """
        answer = input("Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            del self.TASKS[self.TASKS.index(tasks[index])]
            del tasks[index]
            self.save_file()
            if index > 1:
                return index - 1
            return 0
        return index

    def save_file(self):
        """Saves the file in a csvfile."""
        with open(self.file, 'w') as csvfile:
            fieldnames = ["date", "title", "time", "notes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.TASKS:
                writer.writerow(entry.log())

    def add_entry(self):
        """Let the user to create and save a new task. Once is created, the
        file is saved and the user is prompted with the new task to review
        its content. The tasks are sorted before being saved to file to keep
        them ordered.
        """
        entry = Task()
        self.TASKS.append(entry)
        self.sort_tasks()
        self.save_file()
        entry.show()
        input("The entry has been added. Press enter to return to the menu")


class MenuOption:
    def __init__(self, key, name, obj, func, *params):
        self.key = key
        self.name = name
        self.obj = obj
        self.func = func
        self.params = params

    def __str__(self):
        return "{}) {}".format(self.key, self.name)


class Menu:
    options = []

    def print_title(self):
        raise NotImplementedError()

    def print_options(self):
        for option in self.options:
            print(option)

    def print_menu(self):
        utils.clear_screen()
        self.print_title()
        self.print_options()

    def get_option(self):
        while True:
            choice = input("> ")
            for option in self.options:
                if choice == option.key:
                    return option
            print("Sorry, you must choose a valid option")

    def get_function(self, option):
        return getattr(option.obj, option.func, False)

    def run(self):
        while True:
            self.print_menu()
            option = self.get_option()
            func = self.get_function(option)
            if not func:
                break
            else:
                func(*option.params)


class MainMenu(Menu):

    def __init__(self, log):
        self.log = log
        self.options = [
            MenuOption('a', 'Add new entry', log, 'add_entry'),
            MenuOption('b', 'Search in existing entries', SearchMenu(log), 'run'),
            MenuOption('c', 'Quit program', log, 'quit'),
        ]

    def print_title(self):
        print("WORK LOG")
        print("What would you like to do?")


class SearchMenu(Menu, TaskSearch):

    def __init__(self, log):
        self.log = log
        self.options = [
            MenuOption('a', 'Exact Date', self, 'search_date', log.TASKS),
            MenuOption('b', 'Range of Dates', self, 'search_by_range', log.TASKS),
            MenuOption('c', 'Time Spent', self, 'search_time', log.TASKS),
            MenuOption('d', 'Exact Search', self, 'search_exact', log.TASKS),
            MenuOption('e', 'Regex Pattern', self, 'search_regex', log.TASKS),
            MenuOption('f', 'Return to menu', self, 'quit'),
        ]

    def print_title(self):
        print("Do you want to search by:")

    def run(self):
        while True:
            self.print_menu()
            option = self.get_option()
            func = self.get_function(option)
            if not func:
                break
            else:
                tasks = func(*option.params)
                TaskMenu(self.log, 0, tasks).run()


class TaskMenu(Menu):

    def __init__(self, log, index=0, tasks=None):
        self.log = log
        self.index = index
        if tasks is None:
            self.tasks = log.TASKS
        else:
            self.tasks = tasks
        self.options = [
            MenuOption('p', '[P]revious', self, 'previous'),
            MenuOption('n', '[N]ext', self, 'next'),
            MenuOption('e', '[E]dit', log, 'edit', index, self.tasks),
            MenuOption('d', '[D]elete', log, 'delete', index, self.tasks),
            MenuOption('r', '[R]eturn', log, 'return')
        ]
        self.options = self.get_options(index, len(self.tasks))

    def get_options(self, index, length):
        if length == 0:
            return [self.options[-1]]
        if index == 0:
            if length == 1:
                return self.options[2:]
            return self.options[1:]
        if index == length - 1:
            return [self.options[0]] + self.options[2:]
        if index >= length:
            raise IndexError("list index out of range")
        return self.options

    def print_title(self):
        if self.tasks:
            self.tasks[self.index].show()
            print("Result {} of {}\n".format(self.index + 1, len(self.tasks)))
        else:
            print("There are no tasks to show.\n")

    def print_options(self):
        print(', '.join([option.name for option in self.options]))

    def run(self):
        while True:
            self.print_menu()
            option = self.get_option()
            func = self.get_function(option)
            if not func:
                break
            else:
                self.index = func(*option.params)
                self.__init__(self.log, self.index, self.tasks)

    def previous(self):
        return self.index - 1

    def next(self):
        return self.index + 1


if __name__ == '__main__':
    MainMenu(WorkLog('log.csv')).run()
