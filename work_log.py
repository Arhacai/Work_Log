import csv

from menu import MainMenu
from task import Task


class WorkLog:
    """
    WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them and several ways to search through the tasks aswell. It reads
    and save all information in a csv file.
    """

    def __init__(self, file=None):
        """
        Initialize the app by reading the csv file and adding all tasks to a
        list. If there is no file, the app runs with an empty task list.
        """
        self.file = file
        self.TASKS = self.get_tasks(file)

    def get_tasks(self, file=None):
        """
        Imports a list of tasks from a .csv file, if provided. It returns that
        list sorted by date.
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
        return self.sort_tasks(tasks)

    def sort_tasks(self, tasks):
        """
        Takes a list of tasks and sort them by date, from the oldest to the
        newest one.
        """
        for i in range(1, len(tasks)):
            j = i-1
            key = tasks[i]
            while (tasks[j].date > key.date) and (j >= 0):
                tasks[j+1] = tasks[j]
                j -= 1
            tasks[j+1] = key
        return tasks

    def edit_task(self, index, tasks):
        """
        Edit a task using its index to locate it within the list of tasks
        provided. It returns the index to keep displaying it on the menu.
        """
        tasks[index].edit()
        self.save_log()
        return index

    def delete_task(self, index, tasks):
        """
        Let the user to delete an entry. User must confirm this action
        because it can't be undone. Once the entry is deleted, the file is
        saved with the changes made. The index of the previous entry is
        returned, or the index 0 if it was the first entry displayed.
        """
        answer = input("Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            self.TASKS.remove(tasks[index])
            tasks.remove(tasks[index])
            self.save_log()
            if index > 1:
                return index - 1
            return 0
        return index

    def save_log(self):
        """Saves all tasks in a csvfile."""
        with open(self.file, 'w') as csvfile:
            fieldnames = ["Date", "Title", "Time", "Notes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.TASKS:
                writer.writerow(entry.log())

    def add_task(self):
        """
        Let the user to create and add a new task to the log. Once is created,
        the file is saved and the user is prompted with the new task to review
        its content. Tasks are sorted before being saved to file to keep them
        ordered.
        """
        task = Task()
        self.TASKS.append(task)
        self.sort_tasks(self.TASKS)
        self.save_log()
        task.show()
        input("The entry has been added. Press enter to return to the menu")


if __name__ == '__main__':
    MainMenu(WorkLog('log.csv')).run()
