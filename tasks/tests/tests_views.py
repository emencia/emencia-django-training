from datetime import datetime

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from ..views import CategoryListView, home_page, TodoView
from .factories import CategoryFactory, ToDoEntryFactory


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


class CategoryListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('category-list')

    def test_url_resolve_to_category_list_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryListView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_list.html' in templates

    def test_content_without_category(self):
        response = self.client.get(self.url)
        empty_sentence = 'Vous n\'avez pas encore créé de catégorie.'
        assert empty_sentence in response.content.decode('utf-8')

    def test_content_with_categories(self):
        category = CategoryFactory()
        category2 = CategoryFactory()
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        assert category.name in content
        assert category2.name in content


class TodoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('todo')

    def test_root_url_resolve_to_home_page_view(self):
        view = resolve(self.url)
        assert view.func.view_class == TodoView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/todo.html' in templates

    def test_content_without_category(self):
        response = self.client.get(self.url)
        empty_sentence = 'Il n\'y a pas encore de catégorie.'
        assert empty_sentence in response.content.decode('utf-8')

    def test_content_with_empty_category(self):
        category = CategoryFactory()
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        assert category.name in content
        empty_category_text = 'Cette catégorie n\'a pas d\'élément.'
        assert empty_category_text in content

    def test_content_with_category_and_entries(self):
        category = CategoryFactory()
        entry = ToDoEntryFactory(category=category)
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')
        assert category.name in content
        assert entry.name in content
