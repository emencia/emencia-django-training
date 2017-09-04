import factory
import faker
import pytz

from datetime import datetime, timedelta
from random import randint

from django.template.defaultfilters import slugify

from ..models import Category, ToDoEntry


faker = faker.Factory.create()


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: 'Category ' + faker.first_name())

    class Meta:
        model = Category


class ToDoEntryFactory(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: 'Task ' + faker.first_name())
    category = factory.SubFactory('tasks.tests.factories.CategoryFactory')

    class Meta:
        model = ToDoEntry


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.lazy_attribute(lambda o: faker.first_name())
    last_name = factory.lazy_attribute(lambda o: faker.last_name())
    username = factory.lazy_attribute(
        lambda o: slugify(o.first_name + '.' + o.last_name))
    email = factory.lazy_attribute(
        lambda o: '{}@example.com'.format(o.username))

    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username', )

    @factory.lazy_attribute
    def date_joined(self):
        return datetime.now(pytz.utc) - timedelta(days=randint(5, 50))

    last_login = factory.lazy_attribute(
        lambda o: o.date_joined + timedelta(days=4))

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to set the password."""
        user = super()._generate(create, attrs)
        user.set_password('password')
        user.save()
        return user
