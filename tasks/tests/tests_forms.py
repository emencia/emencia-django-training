import pytz

from datetime import datetime, timedelta

from django.forms.models import model_to_dict
from django.test import TestCase

from ..forms import ToDoEntryForm
from .factories import ToDoEntryFactory


class TestToDoEntryForm(TestCase):
    def test_empty_form_is_invalid(self):
        form = ToDoEntryForm()
        assert not form.is_valid()

    def test_form_with_correct_data_is_valid(self):
        todo = ToDoEntryFactory()
        data = model_to_dict(todo)
        form = ToDoEntryForm(data)
        assert form.is_valid()

    def test_form_with_instance_created_eleven_days_ago_is_invalid(self):
        eleven_days_ago = pytz.utc.localize(
            datetime.today() - timedelta(days=11))
        todo = ToDoEntryFactory()
        todo.creation_date = eleven_days_ago
        todo.save()

        data = model_to_dict(todo)
        form = ToDoEntryForm(data, instance=todo)
        assert not form.is_valid()
        assert '__all__' in form.errors, form.errors

    def test_form_with_instance_with_done_is_invalid(self):
        todo = ToDoEntryFactory(done=True)
        data = model_to_dict(todo)
        form = ToDoEntryForm(data, instance=todo)
        assert not form.is_valid()
        assert '__all__' in form.errors, form.errors
