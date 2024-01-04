from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url="/login")
def home(request):
    return render(request, "main/home.html")

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            login(request, user)

            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})

@login_required(login_url="/login")
def dashboard(request):

    if not request.user.is_authenticated:
        raise Exception("You are not logged in")


    return render(request, "main/dashboard.html")

def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        
        user = authenticate(username=username_or_email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard upon successful login
        else:
            error_message = "Invalid username/email or password."
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')
