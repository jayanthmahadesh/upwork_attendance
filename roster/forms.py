
from django import forms

from .models import Roster


class RosterForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['staff_member', 'working_days', 'shifts']
