# Create your views here.
import base64

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import AttendanceForm, RosterForm
from .models import AttendanceRecord, Roster


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            # will define this /success_url in couple of minutes
            return redirect('/success-url/')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


# views.py


def roster_create_view(request):
    if request.method == 'POST':
        form = RosterForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the roster listing page
            return redirect('roster_list_url')
    else:
        form = RosterForm()
    return render(request, 'templates/roster_form.html', {'form': form})


def roster_list_view(request):
    rosters = Roster.objects.all()
    return render(request, 'templates/roster_list.html', {'rosters': rosters})


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
    return render(request, 'templates/roster_form.html', {'form': form})


def roster_delete_view(request, id):
    roster = Roster.objects.get(id=id)
    if request.method == 'POST':
        roster.delete()
        # Redirect to the roster listing page
        return redirect('roster_list_url')
    return render(request, 'templates/roster_confirm_delete.html', {'object': roster})


@csrf_exempt
def capture_attendance(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        timestamp = request.POST.get('timestamp')

        # Decode the image data and save it to a file or directly to a model field
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        # You can save the image file here and/or process it as needed
        # For example, saving the data to AttendanceRecord model
        record = AttendanceRecord(image=imgstr, timestamp=timestamp)
        record.save()

        return JsonResponse({'status': 'success', 'message': 'Attendance captured successfully!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# This view should save the attendance record with the staff member, current timestamp, and uploaded image.


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES)
        if form.is_valid():
            attendance_record = form.save(commit=False)
            attendance_record.staff_member = request.user
            attendance_record.save()
            return redirect('success_url')  # Redirect to a new URL
    else:
        form = AttendanceForm()
    return render(request, 'templates/mark_attendance.html', {'form': form})


# views.py in your Django app


@csrf_exempt
def image_upload(request):
    if request.method == 'POST':
        # Extract the image data
        image_data = request.POST.get('image_data')
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        # Convert base64 to an image file
        image_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        # Here, you can now handle the image file as needed, e.g., saving it to a model

        return JsonResponse({'status': 'success', 'message': 'Image received'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def attendance_system(request):
    return render(request, 'attendance_system.html')
# views.py in your Django app
