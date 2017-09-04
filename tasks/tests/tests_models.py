import pytz

from datetime import datetime

from django.test import TestCase

from ..models import ToDoEntry
from .factories import CategoryFactory, ToDoEntryFactory


class TestCategory(TestCase):
    def setUp(self):
        self.category = CategoryFactory()

    def test_str(self):
        assert self.category.name == str(self.category)


class TestToDoEntry(TestCase):
    def setUp(self):
        self.todo_entry = ToDoEntryFactory()

    def test_str(self):
        assert self.todo_entry.name == str(self.todo_entry), \
            'Wrong implementation of __str__'

    def test_ordering(self):
        bug_year = pytz.utc.localize(datetime(2000, 1, 1))
        few_years_ago = pytz.utc.localize(datetime(2010, 1, 1))
        todo_entry2 = ToDoEntryFactory()
        todo_entry2.creation_date = bug_year
        todo_entry2.save()
        todo_entry3 = ToDoEntryFactory()
        todo_entry3.creation_date = few_years_ago
        todo_entry3.save()

        todos = list(ToDoEntry.objects.all())
        expected = [todo_entry2, todo_entry3, self.todo_entry]
        assert todos == expected, \
            '{todos} différent de {expected}'.format(
                todos=todos, expected=expected)

    def test_verbose_name(self):
        assert 'Elément' in self.todo_entry._meta.verbose_name
        assert 'Eléments' in self.todo_entry._meta.verbose_name_plural
