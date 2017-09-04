from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return self.name


class ToDoEntry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Elément de la todo'
        verbose_name_plural = 'Eléments de la todo'
        ordering = ['creation_date', ]

    def __str__(self):
        return self.name
