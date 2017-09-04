from contextlib import contextmanager

from django.test import TestCase

from .factories import UserFactory


class ScenarioTestCase(TestCase):
    @contextmanager
    def log_user(self, user=None):
        if user is not None:
            self.client.login(username=user.username, password='password')
        try:
            yield
        finally:
            if user is not None:
                self.client.logout()

    @classmethod
    def setUpTestData(cls):
        cls.admin = UserFactory(is_staff=True, is_superuser=True)
        cls.regular_user = UserFactory(is_staff=False, is_superuser=False)

    def setUp(self):
        self.admin_scenario = self.log_user(self.admin)
        self.regular_user_scenario = self.log_user(self.regular_user)
