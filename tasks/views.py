from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .models import Category


def home_page(request):
    date = datetime(2000, 1, 1)
    return render(request, 'tasks/home.html', {'date': date})


class CategoryListView(ListView):
    model = Category


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
