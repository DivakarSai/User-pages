from django.shortcuts import render, redirect
from .forms import RegisterForm, EmailComposeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate, logout
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from website.settings import MAILCHIMP_API_KEY, MAILCHIMP_SERVER_PREFIX, MAILCHIMP_AUDIENCE_ID
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
@login_required(login_url="/login")
def home(request):
    email_form = EmailComposeForm()

    if request.method == 'POST':
        email_form = EmailComposeForm(request.POST)
        if email_form.is_valid():
            # Process the form data (e.g., send email)
            # You can add your email sending logic here

            # Redirect to the same page after sending email
            return redirect('home')
    return render(request, "main/home.html")



def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Explicitly specify the authentication backend after user creation
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()

            subject = 'Registration Confirmation'
            message = render_to_string('registration/email_confirmation.txt', {'user': user})
            html_message = render_to_string('registration/email_confirmation.html', {'user': user})

            # send_mail(
            #     subject,
            #     strip_tags(message),
            #     'divakarsainukala@gmail.com',  # Sender's email address
            #     [user.email],      # Recipient's email address
            #     html_message=html_message,
            # )


            try:
                client = MailchimpMarketing.Client()
                client.set_config({
                    "api_key": MAILCHIMP_API_KEY,
                    "server": MAILCHIMP_SERVER_PREFIX  
                })
                client.lists.add_list_member(MAILCHIMP_AUDIENCE_ID, {
                    'email_address': user.email,
                    'status': 'subscribed',
                })
            except Exception as e:
                print(f"Error adding user to Mailchimp list: {e}")



            messages.success(request, 'Registration successful. Check your email for confirmation.')

            # Log in the user
            login(request, user)

            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})

@login_required(login_url="/login")
def dashboard(request):

    # any validations here
    if not request.user.is_authenticated:
        raise Exception("You are not logged in")


    return render(request, "main/dashboard.html")

@login_required(login_url="/login")
def profile(request):
    return render(request, "main/profile.html")


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
    



