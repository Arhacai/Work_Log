import datetime
import io
import sys
import unittest
from unittest import mock

from menu import MenuOption, Menu, SearchMenu, TaskMenu, MainMenu
import utils
from task import Task, TaskSearch
from work_log import WorkLog


#################
#  TASK TESTS   #
#################
class TaskTests(unittest.TestCase):

    def setUp(self):
        log = {
            'Time': '60',
            'Date': '17/03/2018',
            'Notes': 'Do some work at the office.',
            'Title': 'Review some projects'
        }
        self.task = Task(**log)

    @mock.patch('utils.get_title')
    @mock.patch('utils.get_date')
    @mock.patch('utils.get_time')
    @mock.patch('utils.get_notes')
    def test_init(self, fake_notes, fake_time, fake_date, fake_title):
        Task()
        self.assertTrue(fake_title.called)
        self.assertTrue(fake_date.called)
        self.assertTrue(fake_time.called)
        self.assertTrue(fake_notes.called)

    def test_show(self):
        output = io.StringIO()
        sys.stdout = output
        self.task.show()
        sys.stdout = sys.__stdout__
        text = "Date: 17/03/2018\nTitle: Review some projects\n" \
               "Time spent: 60 minutes\nNotes: Do some work at the office.\n\n"
        self.assertEqual(output.getvalue(), text)

    @mock.patch('builtins.input')
    def test_edit_with_no_changes(self, fake_input):
        fake_input.side_effect = ['', '', '', 'Do some work at the office.']
        old_task = Task(**self.task.log())
        self.task.edit()
        self.assertEqual(old_task.log(), self.task.log())

    @mock.patch('builtins.input')
    def test_edit_with_changes(self, fake_input):
        fake_input.side_effect = ['Test title', '07/09/2018', '30', '']
        edited_task = Task(**self.task.log())
        edited_task.edit()
        self.assertNotEqual(edited_task, self.task)
        self.assertEqual(edited_task.title, "Test title")


class TaskSearchTests(unittest.TestCase):

    def setUp(self):
        log1 = {
            'Time': '60',
            'Date': '17/03/2018',
            'Notes': 'Do some work at the office.',
            'Title': 'Review some projects'
        }
        log2 = {
            'Time': '60',
            'Date': '05/11/2017',
            'Notes': 'Nothing relevant',
            'Title': 'Test project'
        }
        self.tasks = [Task(**log1), Task(**log2)]

    @mock.patch('utils.get_date')
    def test_search_date(self, fake_date):
        fake_date.return_value = datetime.date(2018, 3, 17)
        result = TaskSearch.search_date(self.tasks)
        self.assertEqual(len(result), 1)

    @mock.patch('utils.get_date_range')
    def test_search_by_range(self, fake_range):
        fake_range.return_value = (
            datetime.date(2018, 1, 1), datetime.date(2019, 1, 1))
        result = TaskSearch.search_by_range(self.tasks)
        self.assertEqual(len(result), 1)

    @mock.patch('utils.get_time')
    def test_search_time(self, fake_time):
        fake_time.return_value = '60'
        result = TaskSearch.search_time(self.tasks)
        self.assertEqual(len(result), 2)

    @mock.patch('builtins.input')
    def test_search_exact(self, fake_input):
        fake_input.return_value = 'project'
        result = TaskSearch.search_exact(self.tasks)
        self.assertEqual(len(result), 2)

    @mock.patch('builtins.input')
    def test_search_regex_no_exception(self, fake_input):
        fake_input.return_value = '\d+'
        result = TaskSearch.search_regex(self.tasks)
        self.assertEqual(len(result), 0)

    @mock.patch('builtins.input')
    def test_search_regex_exception_first(self, fake_input):
        fake_input.side_effect = ['\w+[[', '\w+']
        result = TaskSearch.search_regex(self.tasks)
        self.assertEqual(len(result), 2)


#################
#  UTILS TESTS  #
#################
class UtilsTests(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_get_date_exception_first(self, fake_input, fake_print):
        fake_input.side_effect = ['05/34/20', '05/03/2018']
        result = utils.get_date()
        self.assertEqual(result, datetime.date(2018, 3, 5))
        self.assertEqual(fake_print.call_count, 3)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_get_range_exception_first(self, fake_input, fake_print):
        fake_input.side_effect = [
            '05/34/20', '05/03/2018', 'bad_date', '12/05/2019']
        start_date, end_date = utils.get_date_range()
        self.assertEqual(start_date, datetime.date(2018, 3, 5))
        self.assertEqual(end_date, datetime.date(2019, 5, 12))
        self.assertEqual(fake_print.call_count, 6)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_get_title_exception_first(self, fake_input, fake_print):
        fake_input.side_effect = ['', 'Test title']
        result = utils.get_title()
        self.assertEqual(result, 'Test title')
        self.assertEqual(fake_print.call_count, 1)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_get_time_exception_first(self, fake_input, fake_print):
        fake_input.side_effect = [-10, 10]
        result = utils.get_time()
        self.assertEqual(result, '10')
        self.assertEqual(fake_print.call_count, 1)

    @mock.patch('builtins.input')
    def test_get_notes(self, fake_input):
        fake_input.return_value = 'Test notes'
        result = utils.get_notes()
        self.assertEqual(result, 'Test notes')


###################
#  WORKLOG TESTS  #
###################
class WorkLogTests(unittest.TestCase):

    def setUp(self):
        self.log = WorkLog('log.csv')

    def test_init_no_file(self):
        log = WorkLog()
        self.assertEqual(log.TASKS, [])

    def test_init_file_not_found(self):
        log = WorkLog('nofile')
        self.assertEqual(log.TASKS, [])

    @mock.patch('task.Task.edit')
    @mock.patch('work_log.WorkLog.save_log')
    def test_edit_task(self, fake_save, fake_edit):
        index = self.log.edit_task(4, self.log.TASKS)
        self.assertEqual(index, 4)
        self.assertEqual(fake_edit.call_count, 1)
        self.assertEqual(fake_save.call_count, 1)

    @mock.patch('builtins.input')
    @mock.patch('work_log.WorkLog.save_log')
    def test_delete_task(self, fake_save, fake_input):
        fake_input.return_value = 'y'

        tasks = [task for task in self.log.TASKS]
        len_tasks = len(tasks)
        len_TASKS = len(self.log.TASKS)

        entry = tasks[4]
        index = self.log.delete_task(4, tasks)

        self.assertEqual(index, 3)
        self.assertEqual(len(tasks), len_tasks - 1)
        self.assertEqual(len(self.log.TASKS), len_TASKS - 1)
        self.assertNotIn(entry, tasks)
        self.assertNotIn(entry, self.log.TASKS)
        self.assertEqual(fake_save.call_count, 1)

    @mock.patch('builtins.input')
    @mock.patch('work_log.WorkLog.save_log')
    def test_delete_no_deletion(self, fake_save, fake_input):
        fake_input.return_value = 'n'
        index = self.log.delete_task(6, self.log.TASKS)
        self.assertEqual(index, 6)
        self.assertFalse(fake_save.called)

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    def test_add_task_and_sort_tasks(self, fake_print, fake_input):
        fake_input.side_effect = [
            'Test WorkLog class', '08/10/1000', '3141592', 'Test notes', ''
        ]
        self.log.add_task()
        self.assertEqual(fake_input.call_count, 5)
        self.assertEqual(fake_print.call_count, 6)

    @mock.patch('builtins.input')
    def test_delete_task_index_0(self, fake_input):
        fake_input.return_value = 'y'

        tasks = [task for task in self.log.TASKS]
        len_tasks = len(tasks)
        len_TASKS = len(self.log.TASKS)

        index = self.log.delete_task(0, tasks)
        self.assertEqual(index, 0)
        self.assertEqual(len(tasks), len_tasks - 1)
        self.assertEqual(len(self.log.TASKS), len_TASKS - 1)


################
#  MENU TESTS  #
################
class MenuOptionTests(unittest.TestCase):

    def test_init_and_str(self):
        option = MenuOption('a', 'First Option', WorkLog(), 'add_task')
        self.assertEqual(str(option), "a) First Option")


class MenuTests(unittest.TestCase):

    def setUp(self):
        option = MenuOption('a', 'First Option', WorkLog(), 'add_task')
        self.menu = Menu()
        self.menu.options.append(option)

    def test_print_title(self):
        with self.assertRaises(NotImplementedError):
            self.menu.print_title()

    @mock.patch('builtins.input')
    def test_print_options(self, fake_input):
        self.menu.print_options()
        self.assertTrue(fake_input.called_once)

    @mock.patch('utils.clear_screen')
    @mock.patch('menu.Menu.print_title')
    @mock.patch('menu.Menu.print_options')
    def test_print_menu(self, fake_options, fake_title, fake_clear):
        self.menu.print_menu()
        self.assertTrue(fake_clear.called_once)
        self.assertTrue(fake_title.called_once)
        self.assertTrue(fake_options.called_once)

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    def test_get_option_exception_and_good(self, fake_print, fake_input):
        fake_input.side_effect = ['x', 'a']
        option = self.menu.get_option()
        self.assertTrue(fake_print.called_once)
        self.assertIn(option, self.menu.options)
        self.assertEqual(option.name, 'First Option')

    def test_get_function(self):
        option = MenuOption('q', 'Quit', self.menu, 'quit')
        result = self.menu.get_function(option)
        self.assertEqual(result, 'quit')

    @mock.patch('menu.Menu.print_menu')
    @mock.patch('menu.Menu.get_function')
    @mock.patch('menu.Menu.get_option')
    def test_run_and_side_run(self, fake_option, fake_function, fake_menu):
        fake_function.side_effect = [True, 'quit']
        self.menu.run()
        self.assertEqual(fake_menu.call_count, 2)
        self.assertEqual(fake_function.call_count, 2)
        self.assertTrue(fake_option.called_twice)


class MainMenuTests(unittest.TestCase):

    def setUp(self):
        self.menu = MainMenu(WorkLog())

    def test_init(self):
        self.assertEqual(len(self.menu.options), 3)
        self.assertIsInstance(self.menu.options[1], MenuOption)

    def test_print_title(self):
        output = io.StringIO()
        sys.stdout = output
        self.menu.print_title()
        sys.stdout = sys.__stdout__
        text = "WORK LOG\nWhat would you like to do?\n"
        self.assertEqual(output.getvalue(), text)


class SearchMenuTests(unittest.TestCase):

    def setUp(self):
        self.menu = SearchMenu(WorkLog())

    def test_init(self):
        self.assertEqual(len(self.menu.options), 6)
        self.assertIsInstance(self.menu.options[1], MenuOption)

    def test_print_title(self):
        output = io.StringIO()
        sys.stdout = output
        self.menu.print_title()
        sys.stdout = sys.__stdout__
        text = "Do you want to search by:\n"
        self.assertEqual(output.getvalue(), text)

    @mock.patch('menu.TaskMenu.run')
    def test_side_run(self, fake_run):
        self.menu.side_run(result=[])
        self.assertTrue(fake_run.called)
        self.assertTrue(fake_run.called_with(WorkLog(), 0, []))


class TaskMenuTests(unittest.TestCase):

    def setUp(self):
        self.log = WorkLog('log.csv')
        self.tasks = self.log.TASKS

    def test_get_options(self):
        result0 = TaskMenu(self.log, 0, []).options
        result1 = TaskMenu(self.log, 0, [self.tasks[0]]).options
        result2 = TaskMenu(self.log, 0, self.tasks).options
        result3 = TaskMenu(self.log, 2, self.tasks[:3]).options
        result4 = TaskMenu(self.log, 5).options
        self.assertEqual(len(result0), 1)
        self.assertEqual(len(result1), 3)
        self.assertEqual(len(result2), 4)
        self.assertEqual(len(result3), 4)
        self.assertEqual(len(result4), 5)
        with self.assertRaises(IndexError):
            TaskMenu(self.log, 4, self.tasks[:2])

    @mock.patch('task.Task.show')
    def test_print_title(self, fake_show):
        output = io.StringIO()
        sys.stdout = output
        TaskMenu(self.log, 0, self.tasks).print_title()
        sys.stdout = sys.__stdout__
        text = "Result 1 of {}\n\n".format(len(self.tasks))
        self.assertEqual(output.getvalue(), text)
        self.assertTrue(fake_show.called)

    def test_print_title_no_tasks(self):
        output = io.StringIO()
        sys.stdout = output
        TaskMenu(self.log, 0, []).print_title()
        sys.stdout = sys.__stdout__
        text = "There are no tasks to show.\n\n"
        self.assertEqual(output.getvalue(), text)

    def test_print_options(self):
        output = io.StringIO()
        sys.stdout = output
        TaskMenu(self.log, 0, self.tasks).print_options()
        sys.stdout = sys.__stdout__
        text = "[N]ext, [E]dit, [D]elete, [R]eturn\n"
        self.assertEqual(output.getvalue(), text)

    def test_side_run(self):
        menu = TaskMenu(self.log, 0, self.tasks)
        options = menu.options
        menu.side_run(1)
        new_options = menu.options
        self.assertLess(len(options), len(new_options))

    def test_previous_task(self):
        menu = TaskMenu(self.log, 5, self.tasks)
        index = menu.previous_task()
        self.assertLess(index, menu.index)

    def test_next_task(self):
        menu = TaskMenu(self.log, 5, self.tasks)
        index = menu.next_task()
        self.assertGreater(index, menu.index)


if __name__ == '__main__':
    unittest.main()
