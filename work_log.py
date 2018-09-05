import csv
import utils

from task_v2 import Task, TaskSearch


class WorkLog:
    """
    WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them several ways to search through the tasks aswell. It reads and
    save all information in a csv file.
    """

    def __init__(self, *args):
        """
        Initialize the app by reading the csv file and adding all task to a
        list. If there is no file, the app runs with an empty task list.
        """
        self.TASKS = self.get_tasks(*args)
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

    def show_tasks(self, tasks):
        """Takes a list of tasks and shows them on screen one at a time. It
        also displays a set of options to page through tasks, edit and remove
        them.
        """
        index = 0

        while True:
            # Returns to main menu if search return no tasks.
            if tasks is None:
                break
            # If all taks are deleted a message is prompt to advice us.
            elif len(tasks) == 0:
                utils.clear_screen()
                print("There are no more tasks to show.\n")
                input("Press enter to return to search menu.")
                break
            else:
                tasks[index].show_task()
                print("\nResult {} of {}\n".format(index+1, len(tasks)))

                # Menu displayed if only one task is found.
                if index == 0 and len(tasks) == 1:
                    print("[E]dit, [D]elete, [R]eturn to search menu")
                    option = input("\n> ")
                    if option.upper() == 'E':
                        self.edit_entry(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index = 0
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

                # Menu displayed to the first task if there is more than one.
                elif index == 0:
                    print("""
[N]ext, [E]dit, [D]elete, [R]eturn to search menu""")
                    option = input("\n> ")
                    if option.upper() == 'N':
                        index += 1
                    elif option.upper() == 'E':
                        self.edit_entry(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index = 0
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

                # Menu displayed to any task but the first and last one.
                elif index > 0 and index < len(tasks)-1:
                    print("""
[P]revious, [N]ext, [E]dit, [D]elete, [R]eturn to search menu""")
                    option = input("\n> ")
                    if option.upper() == 'P':
                        index -= 1
                    elif option.upper() == 'N':
                        index += 1
                    elif option.upper() == 'E':
                        self.edit_entry(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index -= 1
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

                # Menu displayed for the last tasks if there are more than one.
                elif index == len(tasks)-1:
                    print("""
[P]revious, [E]dit, [D]elete, [R]eturn to search menu""")
                    option = input("\n> ")
                    if option.upper() == 'P':
                        index -= 1
                    elif option.upper() == 'E':
                        self.edit_entry(tasks[index])
                    elif option.upper() == 'D':
                        if self.delete_task(tasks[index]):
                            del tasks[index]
                            index -= 1
                    elif option.upper() == 'R':
                        break
                    else:
                        print("Sorry, you must choose a valid option.")

    def edit_entry(self, entry):
        """
        Edit a task by creating one new and overriding its attributed when
        needed. It replaces the original task and then the tasks are saved
        to file. It returns the task to being able to see it on screen.
        """
        entry.edit()
        self.save_file('log.csv')

    def delete_task(self, entry):
        """Let the user to delete an entry. User must confirm this action
        because it can't be undone. Once the entry is deleted, the file is
        saved with the changes made.
        """
        answer = input("\n Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            del self.TASKS[self.TASKS.index(entry)]
            self.save_file('log.csv')
            return True
        else:
            return False

    def save_file(self, file):
        """Saves the file in a csvfile."""
        with open(file, 'w') as csvfile:
            fieldnames = ["Date", "Title", "Time", "Notes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.TASKS:
                writer.writerow(entry.log)

    def add_entry(self):
        """Let the user to create and save a new task. Once is created, the
        file is saved and the user is prompted with the new task to review
        its content. The tasks are sorted before being saved to file to keep
        them ordered.
        """
        entry = Task.create_new_task()
        self.TASKS.append(entry)
        self.sort_tasks()
        self.save_file('log.csv')
        entry.show_task()
        input("The entry has been add. Press enter to return to the menu")

    def main_menu(self):
        """Displays on screen the main menu of the application and let the user
        to choose an option or quit program.
        """
        while True:
            utils.clear_screen()
            print("""WORK LOG
What would you like to do?
a) Add new entry
b) Search in existing entries
c) Quit program
""")
            option = input("> ")
            if option == 'a':
                self.add_entry()
            elif option == 'b':
                self.search_menu()
            elif option == 'c':
                break
            else:
                print("Sorry, you must choose a valid option.")
                input()

    def search_menu(self):
        """Displays on screen the search menu of the application and let the
        user to choose a search method or return to main menu.
        """
        while True:
            utils.clear_screen()
            print("""Do you want to search by:
a) Exact Date
b) Range of Dates
c) Time Spent
d) Exact Search
e) Regex Pattern
f) Return to menu
""")
            option = input("> ")

            if option == 'a':
                found = TaskSearch.search_date(self.TASKS)
                self.show_tasks(found)
            elif option == 'b':
                found = TaskSearch.search_by_range(self.TASKS)
                self.show_tasks(found)
            elif option == 'c':
                found = TaskSearch.search_time(self.TASKS)
                self.show_tasks(found)
            elif option == 'd':
                found = TaskSearch.search_exact(self.TASKS)
                self.show_tasks(found)
            elif option == 'e':
                found = TaskSearch.search_regex(self.TASKS)
                self.show_tasks(found)
            elif option == 'f':
                break
            else:
                print("Sorry, you must choose a valid option")
                input()


class MenuOption:
    def __init__(self, keys, option):
        self.keys = keys
        self.option = option

    def __str__(self):
        return "[{}]{}".format(self.keys.upper(), self.option[1:])


class TaskMenu:
    options = [
        MenuOption('p', 'previous'),
        MenuOption('n', 'next'),
        MenuOption('e', 'edit'),
        MenuOption('d', 'delete'),
        MenuOption('r', 'return')
    ]

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

    def print_options(self):
        if length == 0:
            print("There are no more tasks to show.\n")
            input("Press enter to return to search menu.")
        elif length == 1 and index == 0:
            print("[E]dit, [D]elete, [R]eturn to search menu")
        elif length > 1 and index == 0:
            print("""[N]ext, [E]dit, [D]elete, [R]eturn to search menu""")
        elif 0 < index < length - 1:
            print("""[P]revious, [N]ext, [E]dit, [D]elete, [R]eturn to search menu""")

        elif index == length - 1:
            print("""[P]revious, [E]dit, [D]elete, [R]eturn to search menu""")

    def get_choice(self):
        while True:
            choice = input("\n> ")
        while not self.options.get(choice, False):
            print("Sorry, you must choose a valid option")
            input()



if __name__ == '__main__':
    WorkLog('log.csv').main_menu()
