# Create your views here.
import base64
import uuid  

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import AttendanceForm
from .forms import UserRegistrationForm, StaffMemberForm,RosterForm,LoginForm
from .models import StaffMember,Roster,AttendanceRecord
def homepage(request):
    return render(request,'homepage.html')
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        member_form = StaffMemberForm(request.POST)
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()  # Creates the User object
            member = member_form.save(commit=False) 
            member.user = user 
            member.save() 
            return redirect('register_success') 
    else:
        user_form = UserRegistrationForm()
        member_form = StaffMemberForm()
    return render(request, 'manager/register.html', {'user_form': user_form, 'member_form': member_form})

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("user is logged in")
            # Redirect to a success page.
            # will define this /success_url in couple of minutes
            staff_member = StaffMember.objects.get(user__username=username)
            print("the primary key of the object"+str(staff_member.pk))
            request.session['user_id'] = staff_member.pk
            request.session['user_name'] = staff_member.user.username 
            return redirect('register_success')
        else:
            print("user is not registered or the password is incorrect")
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error': 'Invalid username or password','form':LoginForm})
    else:
        return render(request, 'login.html',{'form':LoginForm})

def custom_logout(request):
    logout(request)  # Log the user out
    request.session.flush()
    return redirect('custom_login')
# views.py

def roster_create_view(request):
    if request.method == 'POST':
        form = RosterForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the roster listing page
            return redirect('manager/roster_list_url')
    else:
        form = RosterForm()
    return render(request, 'manager/roster_form.html', {'form': form})
def register_success_view(request):
    return render(request, 'success.html') 
@login_required
def create_roster(request):
    if request.method == 'POST':
        form = RosterForm(request.POST)
        if form.is_valid():
            staff_member_id = request.session.get('user_id')
            try:
                staff_member = StaffMember.objects.get(pk=staff_member_id)
            except StaffMember.DoesNotExist:
                # Handle the case where the staff member is not found
                print("something unwanted happened")
                return render(request, 'manager/roster_form.html', {'form': form, 'error_message': 'Staff member not found'})
            
            roster = form.save(commit=False)
            roster.staff_member = staff_member
            roster.save()
            return redirect('register_success')
    else:
        form = RosterForm()
    return render(request, 'manager/roster_form.html', {'form': form})
def roster_list(request):
    rosters = Roster.objects.all()
    print(rosters)
    return render(request, 'manager/roster_list.html', {'rosters': rosters})


def roster_update_view(request, id):
    roster = Roster.objects.get(id=id)
    if request.method == 'POST':
        form = RosterForm(request.POST, instance=roster)
        if form.is_valid():
            form.save()
            # Redirect to the roster listing page
            return redirect('roster_list_url')
    else:
        form = RosterForm(instance=roster)
    return render(request, 'manager/roster_form.html', {'form': form})


def roster_delete_view(request, id):
    roster = Roster.objects.get(id=id)
    if request.method == 'POST':
        roster.delete()
        # Redirect to the roster listing page
        return redirect('roster_list_url')
    return render(request, 'manager/roster_confirm_delete.html', {'object': roster})

def mark_attendance(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        # Decode base64 data
        format, imgstr = image_data.split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr), name=uuid.uuid4().hex + '.' + ext)

        # Save to model
        image_instance = AttendanceRecord(image=data)
        staff_member_id = request.session.get('user_id')
        try:
            staff_member = StaffMember.objects.get(pk=staff_member_id)
        except StaffMember.DoesNotExist:
            print("something unwanted happened")
            return render(request, 'login.html')
        image_instance.staff_member = staff_member
        image_instance.save()
        return redirect('register_success')  # Redirect to a new URL
    else:
        form = AttendanceForm()
    return render(request, 'manager/mark_attendance.html')