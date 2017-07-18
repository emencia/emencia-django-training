from datetime import datetime

from django.shortcuts import render


def home_page(request):
    date = datetime(2000, 1, 1)
    return render(request, 'tasks/home.html', {'date': date})
