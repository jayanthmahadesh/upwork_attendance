
from django import forms

from .models import AttendanceRecord, Roster

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StaffMember

class RosterForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['working_days', 'shifts']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# This form is linked to the AttendanceRecord model and
# will only display an input for the image, as the other
# fields (staff_member and timestamp) will be automatically filled.

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['image']
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 

class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ['email', 'role']  