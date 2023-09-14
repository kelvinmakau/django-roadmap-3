# custom_auth/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        designation = request.POST['designation']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']  # Get the confirm password

        if password != password2: ## Display error message and redirect the same page if passwords don't match
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'registration.html')

        try:
            # Create the fields you want in the custom form
            user = CustomUser.objects.create_user(
                username=username,
                phone_number=phone_number,
                designation=designation,
                first_name=first_name,
                last_name=last_name,
                password=password,
                
            )
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            logout(request) # Ensure the users must login after registration
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')

    return render(request, 'registration.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, 'Logged in successfully')  # Display success message
            login(request, user)
            return redirect('profile')
        
        else:
            messages.error(request, 'Account does not exist.')  # Display error message and redirect the same page
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')

@login_required # must login to access this
def user_profile(request):
    return render(request, 'profile.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# To display error messsage and redirect to login when you try to access profile before loging in
def login_required_message(request):
    messages.error(request, 'You must be logged in to access this page.')
    return render(request, 'login.html')



