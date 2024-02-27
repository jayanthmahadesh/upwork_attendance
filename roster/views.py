# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import RosterForm


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
