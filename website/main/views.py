from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse

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

    print("request.user : " + request.user.username)

    # any validations here
    if not request.user.is_authenticated:
        raise Exception("You are not logged in")


    return render(request, "main/dashboard.html")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a specific URL after successful login
                print("user.username : " + user.username)
                return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})
            else:
                # Handle invalid login credentials
                error_message = "Invalid username/email or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

