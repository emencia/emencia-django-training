from django.urls import reverse

from ..models import Category, ToDoEntry
from .common import ScenarioTestCase


class TestRegisterModelInAdmin(ScenarioTestCase):
    def test_models_are_registered(self):
        with self.admin_scenario:
            resp = self.client.get(reverse('admin:index'))
            content = resp.content.decode('utf-8')
            models = {
                Category,
                ToDoEntry,
            }
            for model in models:
                assert str(model._meta.verbose_name_plural) in content


class TestAddModel(ScenarioTestCase):
    def test_can_access_add_page(self):
        with self.admin_scenario:
            models = {
                Category,
                ToDoEntry,
            }
            for model in models:
                name = model.__name__.lower()
                url = reverse('admin:tasks_{}_add'.format(name))
                resp = self.client.get(url)
                assert resp.status_code == 200


class TestAdminAccess(ScenarioTestCase):
    def test_cant_access_admin_if_regular_user(self):
        with self.regular_user_scenario:
            resp = self.client.get(reverse('admin:index'))
            assert resp.status_code == 302

            resp = self.client.get(reverse('admin:index'), follow=True)
            assert resp.status_code == 200
            error_msg = (
                'You are authenticated as {}, but are not authorized'
                ' to access this page. Would you like to login to a different '
                'account?'
            ).format(self.regular_user.username)
            assert error_msg in resp.content.decode('utf-8')

    def test_can_access_if_admin(self):
        with self.admin_scenario:
            resp = self.client.get(reverse('admin:index'))
            assert resp.status_code == 200
