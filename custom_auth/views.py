# custom_auth/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control, never_cache # pevent caching of the login
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib import messages
from .models import CustomUser
import re #regex for confirming password special characters

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

        if password != password2: 
            ## Display error message and redirect the same page if passwords don't match
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'registration.html')
        
        elif len(password) < 8: 
            ## Ensure password is more that 8 characters long
            messages.error(request, 'Password is too short, it must be 8 characters or more')
            return render(request, 'registration.html')
        
        elif not any(char.isupper() for char in password):
            ## Check to see if there are uppercase letters in the password
            messages.error(request, 'Password must have at least one uppercase letter')
            return render(request, 'registration.html')
        
        elif not any(char.islower() for char in password):
            ## Check to see if there are lowercase letters in the password
            messages.error(request, 'Password must have at least one lowercase letter')
            return render(request, 'registration.html')
        
        elif not any(char.isdigit() for char in password):
            ## Check to see if there are numbers in the password
            messages.error(request, 'Password must have at least one digit e.g 1')
            return render(request, 'registration.html')
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            ## Check to make sure no special character was used as a part of the password
            messages.error(request, 'Password must have at least one special character')
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
            messages.success(request, 'Registration successful! Kindly login to continue')
            logout(request) # Ensure the users must login after registration
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')

    return render(request, 'registration.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True) #Ensure you cant go back to login with the browser back button
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, 'Logged in successfully')  # Display success message
            login(request, user)
            # timestamp_query_param = int(timezone.now().timestamp())
            return redirect(f'profile')
        # Handling authentication failure
        else:
            messages.error(request, 'Account does not exist or password is wrong')  # Display error message and redirect the same page
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')

# @login_required # must login to access this
def user_profile(request):
    if not request.user.is_authenticated: # show error message when a user tries to access the profile without logging in
        messages.error(request,'You are not logged-in!')
        return render(request, 'login.html')
    return render(request, 'profile.html')

def user_logout(request):
    logout(request)
    messages.info(request,'You logged out successfully, please login to access more features')
    return redirect('login')


