from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .models import Category, ToDoEntry


def home_page(request):
    date = datetime(2000, 1, 1)
    return render(request, 'tasks/home.html', {'date': date})


class CategoryListView(ListView):
    model = Category


class CategoryCreateView(CreateView):
    model = Category
    fields = ('name', )
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name', )
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')


class ToDoEntryCreateView(CreateView):
    model = ToDoEntry
    fields = ('name', 'description', 'category', )
    success_url = reverse_lazy('todo')


class ToDoEntryUpdateView(UpdateView):
    model = ToDoEntry
    fields = ('name', 'description', 'category', )
    success_url = reverse_lazy('todo')


class ToDoEntryDeleteView(DeleteView):
    model = ToDoEntry
    success_url = reverse_lazy('todo')


class TodoView(TemplateView):
    template_name = 'tasks/todo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = (
            Category.objects
            .all()
            .prefetch_related('todoentry_set')
        )
        return context


class ToDoMarkAsDoneView(View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        status = 200
        messages = {
            200: 'Ok',
            404: 'Object does not exist',
            401: 'Entry is already mark as done',
        }

        try:
            todo = ToDoEntry.objects.get(pk=kwargs['pk'])
            assert not todo.done
            todo.done = True
            todo.save()
        except ToDoEntry.DoesNotExist:
            status = 404
        except AssertionError:
            status = 401

        return JsonResponse({'msg': messages[status]}, status=status)
