from django.shortcuts import render,redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Class, Site, Entity, Personnel, SecurityClearance



# Create your views here.
def home_page(request):
    entity = Entity.objects.all()
    return render(request, 'homepage.html', {'entity' : entity})

def base(request):
    user = User.objects.all()

def login_page(request):
    """
    Handles the 'Login' form
    from login.html
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

        # Check the hashed password
        if check_password(password, user.password):
            # Store user in session so they stay logged in
            request.session['user_id'] = user.uid
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')



def signin_page(request):
    
    """
    Handles the 'Sign in' (registration) form
    from signin.html
    """
    if request.method == 'POST':
        # Grab the form data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Hash the password for security
        hashed_password = make_password(password)

        try:
            # Create a new user record in the database
            new_user = User.objects.create(
                username=username,
                email=email,
                password=hashed_password
            )
            messages.success(request, 'Sign in successful!')

            # Optionally, log them in right away
            request.session['user_id'] = new_user.uid
            return redirect('home')  # or wherever you want
        except IntegrityError:
            # This occurs if the username or email is already taken
            messages.error(request, 'Username or email already in use.')

    # If GET (or an error occurred), just show the form again  
    
    return render(request, 'signin.html')