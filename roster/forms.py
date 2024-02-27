
from django import forms

from .models import AttendanceRecord, Roster


class RosterForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['staff_member', 'working_days', 'shifts']


# This form is linked to the AttendanceRecord model and
# will only display an input for the image, as the other
# fields (staff_member and timestamp) will be automatically filled.
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['image']
