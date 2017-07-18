from datetime import datetime

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from tasks.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        root_view = resolve('/')
        assert root_view.func == home_page

    def test_home_page_html(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content
        assert content.startswith(b'<html>'), 'Le contenu ne commence pas par <html>'
        assert b'<title>ToDoz</title>' in content, 'Le contenu ne contient pas Todoz en title'
        assert content.endswith(b'</html>'), 'Le contenu ne se termine pas par </html>'

    def test_date_in_context(self):
        response = self.client.get('/')
        assert 'date' in response.context, 'Le contexte ne contient pas la variable "date"'

    def test_date_in_content(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content.decode('utf-8')
        date = datetime(2000, 1, 1).strftime('%b. %-d, %Y')
        assert date in content, '{date} n\'est pas dans {content}'.format(
            date=date, content=content)

    def test_copyright_date(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content.decode('utf-8')
        this_year = datetime.today().year
        assert 'Copyright: 2000 - {year}'.format(year=this_year) in content

    def test_base_template_is_used(self):
        response = self.client.get('/')
        templates_used = [t.name for t in response.templates]
        assert ['tasks/home.html', 'tasks/base.html'] == templates_used, templates_used
