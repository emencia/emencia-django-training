from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.home_page,
        name='home'),
    url(r'^categories/',
        views.CategoryListView.as_view(),
        name='category-list'),
    url(r'^todo/$',
        views.TodoView.as_view(),
        name='todo'),
]
