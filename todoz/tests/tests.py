from django.test import SimpleTestCase
from django.conf import settings


class TestInstalledApps(SimpleTestCase):
    def test_installed_apps(self):
        apps = settings.INSTALLED_APPS
        assert 'tasks' in apps, \
            'Les applications installées sont {}'.format(' ,'.join(apps))
