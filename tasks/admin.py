from django.contrib import admin

from .models import Category, ToDoEntry


class ToDoEntryAdmin(admin.ModelAdmin):
    def mark_as_done(modeladmin, request, queryset):
        queryset.update(done=True)
    mark_as_done.short_description = 'Mark items as done'

    list_display = ('__str__', 'done', 'category', 'creation_date', )
    list_filter = ('creation_date', 'category__name', 'done', )
    search_fields = ('name', 'category__name', )
    actions = ['mark_as_done']


admin.site.register(Category)
admin.site.register(ToDoEntry, ToDoEntryAdmin)
