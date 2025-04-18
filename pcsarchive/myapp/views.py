
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .models import User, Class, Site, Entity, Personnel, SecurityClearance
from django.contrib.auth import get_user_model, authenticate, login


# Create your views here.
def home_page(request):
    entity = Entity.objects.all()

    user_id = request.session.get('user_id')

    context = {
        'entity': entity,
        'user_id': user_id
    }
    return render(request, 'homepage.html', context)

def base(request):
    user = User.objects.all()
    user_id = request.session.get('user_id')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Logs in the user and stores full session
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

def entity_detail(request, eid):
    entity = get_object_or_404(Entity, eid=eid)
    return render(request, 'entitypage.html', {'entity': entity})

User = get_user_model()

@login_required
def user_profile(request, uid):
    target_user = get_object_or_404(User, uid=uid)

    if request.user == target_user and request.method == 'POST':
        if 'quote' in request.POST:
            new_quote = request.POST.get('quote')
            if new_quote:
                target_user.quote = new_quote[:100]

        if 'image' in request.FILES:
            target_user.image = request.FILES['image']

        target_user.save()
        messages.success(request, "Profile updated.")

    return render(request, 'profile.html', {'user': target_user})


@login_required
def profile_page(request):
    user = request.user

    if request.method == 'POST':
        if 'quote' in request.POST:
            new_quote = request.POST.get('quote')
            if new_quote:
                user.quote = new_quote[:100]

        if 'image' in request.FILES:
            user.image = request.FILES['image']

        user.save()
        messages.success(request, "Profile updated.")

    return render(request, 'profile.html', {'user': user})




