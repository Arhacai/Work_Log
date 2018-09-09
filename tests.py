import datetime
import io
import sys
import unittest
from unittest import mock

from task import Task, TaskSearch
import utils


#################
#  TASK TESTS   #
#################
from work_log import WorkLog


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
        fake_range.return_value = (datetime.date(2018, 1, 1), datetime.date(2019, 1, 1))
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
    def test_delete_task_index_0(self, fake_save, fake_input):
        fake_input.return_value = 'y'

        tasks = [task for task in self.log.TASKS]
        len_tasks = len(tasks)
        len_TASKS = len(self.log.TASKS)

        entry = tasks[0]
        index = self.log.delete_task(0, tasks)

        self.assertEqual(index, 0)
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
    def test_add_task_save_log_and_sort_tasks(self, fake_print, fake_input):
        fake_input.side_effect = [
            'Test title', '08/10/2018', '60', 'Test notes', ''
        ]
        self.log.add_task()
        self.assertEqual(fake_input.call_count, 5)
        self.assertEqual(fake_print.call_count, 6)


if __name__ == '__main__':
    unittest.main()
