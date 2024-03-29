
import base64,uuid
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, StaffMemberForm,RosterForm,LoginForm,AttendanceForm
from .models import StaffMember,Roster,AttendanceRecord

def homepage(request):
    access=check_user_access(request)
    str=""
    if(access):
        str="1"
    else:
        str="0"
    context = {
        'role': str
    }
    return render(request,'homepage.html',context)

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
            staff_member = StaffMember.objects.get(user__username=username)
            print("the primary key of the object"+str(staff_member.pk))
            request.session['user_id'] = staff_member.pk
            request.session['user_name'] = staff_member.user.username 
            request.session['user_type']=staff_member.role
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
def create_roster(request):
    access=check_user_access(request)
    if(access):
        return redirect('no_access')
    if request.method == 'POST':
        form = RosterForm(request.POST)
        username = request.POST.get('username')
        if form.is_valid():
            try:
                staff_member = StaffMember.objects.get(user__username=username)
            except StaffMember.DoesNotExist:
                # Handle the case where the staff member is not found
                return render(request, 'manager/roster_form.html', {'form': form, 'error_message': 'Staff member not found'})
            roster = form.save(commit=False)
            roster.staff_member=staff_member
            try:
                roster.save()
            except:
                return render(request, 'roster_exists.html')
            return redirect('register_success')
    else:
        form = RosterForm()
    temp = StaffMember.objects.filter()
    staff_list=[]
    for i in temp:
        if(i.role=="Staff"):
            staff_list.append(i.user.username)
    return render(request, 'manager/roster_form.html', {'form': form,'staff_list':staff_list})
def roster_list(request):
    access=check_user_access(request)
    if(access):
        username = request.session.get('user_name')
        rosters = Roster.objects.filter(staff_member__user__username=username)
    else:
        rosters = Roster.objects.all()
    return render(request, 'manager/roster_list.html', {'rosters': rosters})

def roster_update_view(request, id):
    access=check_user_access(request)
    if(access):
        return redirect('no_access')
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
    access=check_user_access(request)
    if(access):
        return redirect('no_access')
    roster = Roster.objects.get(id=id)
    if request.method == 'POST':
        roster.delete()
        # Redirect to the roster listing page
        return redirect('roster_list_url')
    return render(request, 'manager/roster_confirm_delete.html', {'object': roster})

@login_required
def mark_attendance(request):
    if request.method == 'POST':

        image_data = request.POST.get('image_data')
        selected_time = request.POST.get('selected_time')
        parts = selected_time.split(":")
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
            return render(request, 'login.html')
        image_instance.staff_member = staff_member
        image_instance.role=parts[0]
        image_instance.shift=parts[1]
        image_instance.save()
        return redirect('register_success')  # Redirect to a new URL
    else:
        form = AttendanceForm()
    username = request.session.get('user_name')
    rosters = Roster.objects.filter(staff_member__user__username=username)
    temp=[]
    for roster in rosters:
        temp.append((roster.working_days,roster.shifts))
    context = {
        'roster_list': temp
    }
    return render(request, 'manager/mark_attendance.html',context)

def roster_attendance_display(request,id,working_days,shift):
    access=check_user_access(request)
    roster = Roster.objects.get(id=id)
    staff_member = roster.staff_member
    attendance_records = AttendanceRecord.objects.filter(staff_member=staff_member)
    context = {
        'attendance_records': attendance_records
    }
    return render(request, 'attendance.html', context) 


def register_success_view(request):
    return render(request, 'success.html') 

def no_access(request):
    return render(request, 'no_access.html') 


def check_user_access(request):
    type_of_user = request.session.get('user_type')
    if(type_of_user=="Manager"):
        return False
    return True