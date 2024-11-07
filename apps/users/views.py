from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from apps.users.forms import LoginForm, RegistrationForm, PersonalInformationForm, CustomPasswordChangeForm


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email', None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_name}.")
                return redirect('main:home')
            else:
                messages.error(request, "An error occurred. Kindly try again with correct credentials, reset password if you have forgotten or contact us.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
            messages.error(request, f"Invalid credentials. Please try again.")
    return render(request, 'users/login.html', {
        'page': 'login',
        'form': form,
    })

def register_user(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password1')
            # account = authenticate(email=email, password=raw_password)
            messages.success(request, f"You have successfully registered. Go ahead and now login.")
            # login(request, account)
            return redirect('users:login')
        else:
            messages.error(request, "Error creating account. Please correct the highlighted errors")
    return render(request, 'users/register.html', {
        'page': 'register',
        'form': form,
    })

def logout_user(request):
	if request.user.is_authenticated:
		username = request.user.name
		logout(request)
		messages.info(request, f"{username} has been logged out.")
	else:
		messages.warning(request, "No user is currently logged in.")
	return redirect('main:home')

# Create your views here.
def home(request):
    return HttpResponse("Users App")