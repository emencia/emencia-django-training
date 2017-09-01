from datetime import datetime

from django.core.urlresolvers import resolve
from django.forms.models import model_to_dict
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from ..models import Category, ToDoEntry
from ..views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    home_page,
    ToDoEntryCreateView,
    ToDoEntryDeleteView,
    ToDoEntryUpdateView,
    ToDoMarkAsDoneView,
    TodoView,
)
from .factories import CategoryFactory, ToDoEntryFactory


class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        root_view = resolve('/')
        assert root_view.func == home_page

    def test_home_page_html(self):
        request = HttpRequest()
        response = home_page(request)
        content = response.content
        assert content.startswith(
            b'<!DOCTYPE html>\n<html lang=\'fr\'>'
        ), 'Mauvais contenu : ' + str(content)[:100]

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


class CategoryCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('category-create')

    def test_url_resolve_to_category_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryCreateView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_form.html' in templates

    def test_post_empty(self):
        response = self.client.post(self.url)
        assert response.status_code == 200, response.status_code
        assert 'name' in response.context['form'].errors

    def test_post(self):
        response = self.client.post(self.url, {'name': 'foo'})
        assert response.status_code == 302, response.status_code
        assert Category.objects.all().count() == 1


class CategoryUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.url = reverse('category-update', kwargs={'pk': cls.category.pk})

    def test_url_resolve_to_category_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryUpdateView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_form.html' in templates

    def test_post_empty(self):
        response = self.client.post(self.url)
        assert response.status_code == 200, response.status_code
        assert 'name' in response.context['form'].errors

    def test_post(self):
        response = self.client.post(self.url, {'name': 'foo2'})
        assert response.status_code == 302, response.status_code
        assert Category.objects.get(pk=self.category.pk).name == 'foo2'


class CategoryDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.url = reverse('category-delete', kwargs={'pk': cls.category.pk})

    def test_url_resolve_to_category_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == CategoryDeleteView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/category_confirm_delete.html' in templates

    def test_post(self):
        self.client.post(self.url)
        assert Category.objects.all().count() == 0


class ToDoEntryCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('todo-create')

    def test_url_resolve_to_todo_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == ToDoEntryCreateView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/todoentry_form.html' in templates

    def test_post_empty(self):
        response = self.client.post(self.url)
        assert response.status_code == 200, response.status_code
        assert 'name' in response.context['form'].errors

    def test_post(self):
        todo = ToDoEntryFactory()
        todo.pk = None
        data = model_to_dict(todo)
        response = self.client.post(self.url, data)
        assert response.status_code == 302, response.status_code
        assert ToDoEntry.objects.all().count() == 2


class ToDoEntryUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.todo = ToDoEntryFactory()
        cls.url = reverse('todo-update', kwargs={'pk': cls.todo.pk})

    def test_url_resolve_to_category_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == ToDoEntryUpdateView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/todoentry_form.html' in templates

    def test_post_empty(self):
        response = self.client.post(self.url)
        assert response.status_code == 200, response.status_code
        assert 'name' in response.context['form'].errors

    def test_post(self):
        data = model_to_dict(self.todo)
        data['name'] = 'foo2'
        response = self.client.post(self.url, data)
        assert response.status_code == 302, response.status_code
        assert ToDoEntry.objects.get(pk=self.todo.pk).name == 'foo2'


class ToDoEntryDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.todo = ToDoEntryFactory()
        cls.url = reverse('todo-delete', kwargs={'pk': cls.todo.pk})

    def test_url_resolve_to_todo_create_view(self):
        view = resolve(self.url)
        assert view.func.view_class == ToDoEntryDeleteView

    def test_status_code_is_200(self):
        response = self.client.get(self.url)
        assert response.status_code == 200, response.status_code

    def test_template(self):
        response = self.client.get(self.url)
        templates = [t.name for t in response.templates]
        assert 'tasks/todoentry_confirm_delete.html' in templates

    def test_post(self):
        self.client.post(self.url)
        assert ToDoEntry.objects.all().count() == 0


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


class TodoMarkAsDoneViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.todo = ToDoEntryFactory()
        cls.url = reverse('todo_mark_as_done', kwargs={'pk': cls.todo.pk})

    def test_root_url_resolve_to_home_page_view(self):
        view = resolve(self.url)
        assert view.func.view_class == ToDoMarkAsDoneView

    def test_status_code_for_get_is_405(self):
        response = self.client.get(self.url)
        assert response.status_code == 405, response.status_code

    def test_status_code_for_post_is_200(self):
        response = self.client.post(self.url)
        assert response.status_code == 200, response.status_code

    def test_content_type_for_post_is_json(self):
        response = self.client.post(self.url)
        assert response['Content-Type'] == 'application/json'

    def test_done_attribute_is_updated_with_post(self):
        assert not self.todo.done
        self.client.post(self.url)
        todo = ToDoEntry.objects.get(pk=self.todo.pk)
        assert todo.done

    def test_post_with_done_entry(self):
        todo_done = ToDoEntryFactory(done=True)
        url = reverse('todo_mark_as_done', kwargs={'pk': todo_done.pk})
        response = self.client.post(url)
        assert response.status_code == 401

    def test_status_code_with_wrong_pk(self):
        url = reverse('todo_mark_as_done', kwargs={'pk': '999999999999999999'})
        response = self.client.post(url)
        assert response.status_code == 404
