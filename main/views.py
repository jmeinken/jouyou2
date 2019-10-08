from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max







def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))  
                return redirect('home')
            else:
                # Return a 'disabled account' error message
                context['login_error'] = 'Your account has a problem.  Please contact the administrator.'
                return render(request, 'login.html', context)
        else:
            # Return an 'invalid login' error message.
            context['login_error'] = 'Login failed.  Please reenter your username and password.'
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return redirect('study:home')

