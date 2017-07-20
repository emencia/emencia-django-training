import factory
import faker

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
