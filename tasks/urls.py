from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.home_page,
        name='home'),
    url(r'^categories/$',
        views.CategoryListView.as_view(),
        name='category-list'),
    url(r'^categories/create/$',
        views.CategoryCreateView.as_view(),
        name='category-create'),
    url(r'^categories/edit/(?P<pk>\d+)/$',
        views.CategoryUpdateView.as_view(),
        name='category-update'),
    url(r'^categories/delete/(?P<pk>\d+)/$',
        views.CategoryDeleteView.as_view(),
        name='category-delete'),
    url(r'^todo/create/$',
        views.ToDoEntryCreateView.as_view(),
        name='todo-create'),
    url(r'^todo/edit/(?P<pk>\d+)/$',
        views.ToDoEntryUpdateView.as_view(),
        name='todo-update'),
    url(r'^todo/delete/(?P<pk>\d+)/$',
        views.ToDoEntryDeleteView.as_view(),
        name='todo-delete'),
    url(r'^todo/$',
        views.TodoView.as_view(),
        name='todo'),
]
