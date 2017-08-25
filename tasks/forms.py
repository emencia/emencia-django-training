import pytz

from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import ToDoEntry


class ToDoEntryForm(forms.ModelForm):
    class Meta:
        model = ToDoEntry
        fields = ('name', 'description', 'category', )

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk:
            return cleaned_data

        if self.instance.done:
            raise ValidationError(
                'Votre tâche est déjà terminé, vous ne pouvez pas la modifier',
                code='invalid'
            )

        ten_days_ago = pytz.utc.localize(datetime.today() - timedelta(days=10))
        if self.instance.creation_date < ten_days_ago:
            raise ValidationError(
                'Vous ne pouvez plus modifier un élément qui a plus de 10 jours',
                code='invalid')

        return cleaned_data
