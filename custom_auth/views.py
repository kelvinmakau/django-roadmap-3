# custom_auth/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control, never_cache # pevent caching of the login
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserForm
import re #regex for confirming password special characters

# Create your views here.

# Custom user tests
def is_admin(user):
    return user.designation == 'Admin'

def is_supervisor(user):
    return user.designation == 'Supervisor'

def is_employee(user):
    return user.designation == 'Employee'


#Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        designation = request.POST['designation']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
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
                email = email,
                password=password,
                
            )
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful! Kindly login to continue')
            # logout(request) # Ensure the users must login after registration
            return redirect('soon')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')

    return render(request, 'registration.html')

@never_cache #Ensure you cant go back to login with the browser back button
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_authenticated:
            messages.success(request, 'Logged in successfully')  # Display success message
            login(request, user)
            return redirect('soon')
        # Handling authentication failure
        else:
            messages.error(request, 'Account does not exist or password is wrong')  # Display error message and redirect the same page
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')

@login_required # must login to access this
def user_profile(request):
    return render(request, 'profile.html')

def user_logout(request):
    logout(request)
    # messages.info(request,'You logged out successfully, please login to access more features')
    return redirect('login')

@login_required
def coming_soon(request):
    return render (request,"comingsoon.html")

# Update your personal profile when logged in
@login_required
def update_profile(request):
    if request.method == 'POST':
        # Retrieve and update user profile data based on the submitted form
        user = request.user
        user.phone_number = request.POST.get('phone_number')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        # Redirect to the user profile page or any other desired page
        messages.success(request, f'Update successful')
        return redirect('soon')

# View all registered users view
#  add a decorator to display an error message if the user is not an admin
@login_required
def view_users(request):
    if not (is_admin(request.user) or is_supervisor(request.user)):
        # Display an error message if the user is not an admin
        messages.error(request, "You are not allowed to access this page.")
        return redirect('soon')

    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render(request, "view_users.html", context)

# Edit user as admin view
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            # Redirect to the user profile page or any other desired page
            messages.success(request, f'Update successful')
            return redirect('view_users')

    else:
        form = CustomUserForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'edit_user.html', context)

# delete user view
@login_required
def delete_user(request, user_id):
    if not (is_admin(request.user)):
        # Display an error message if the user is not an admin
        messages.error(request, "You are not allowed to perform this action")
        return redirect('view_users')
    # Get the user and the unique identifier
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        # Delete the user
        user.delete()
        messages.success(request, "User deleted successfully") # Show a success message
        return redirect('view_users') # Redirect to the list of users
    return render(request, 'delete_user_confirm.html') # Confirm deletion