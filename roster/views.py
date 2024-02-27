# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import RosterForm
from .models import Roster


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
    return render(request, 'roster/roster_form.html', {'form': form})


def roster_list_view(request):
    rosters = Roster.objects.all()
    return render(request, 'roster/roster_list.html', {'rosters': rosters})


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
    return render(request, 'roster/roster_form.html', {'form': form})


def roster_delete_view(request, id):
    roster = Roster.objects.get(id=id)
    if request.method == 'POST':
        roster.delete()
        # Redirect to the roster listing page
        return redirect('roster_list_url')
    return render(request, 'roster/roster_confirm_delete.html', {'object': roster})
