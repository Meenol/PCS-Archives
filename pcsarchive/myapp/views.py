from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .models import User, Class, Site, Entity, Personnel, SecurityClearance
from django.contrib.auth import get_user_model, authenticate, login, logout


# Create your views here.
def home_page(request):
    entity = Entity.objects.all()
    return render(request, 'homepage.html', {'entity' : entity})

def about_page(request):
    return render(request, 'about.html')


@login_required
def upload_entity(request):
    classes = Class.objects.all()
    sites = Site.objects.all()

    context = {
        'classes': classes,
        'sites': sites
    }

    if request.method == 'POST':
        eImage = request.FILES.get('image')
        if not eImage:
            eImage = 'entitypfp/default_image.png'

        eName = request.POST['name']

        eClass = request.POST['eclass']
        selected_class = Class.objects.get(class_id=eClass)

        eSite = request.POST['esite']
        selected_site = Site.objects.get(siteid=eSite)

        eDesc = request.POST['desc']
        if not eDesc:
            eDesc = "No description provided."

        try:
            insert = Entity.objects.create(
                name=eName,
                location=selected_site,
                image=eImage,
                class_ref=selected_class,
                description=eDesc,
                created_by=request.user  # ✅ this assigns the logged-in user
            )
            messages.success(request, "Entity successfully uploaded.")

            request.user.entities_documented += 1
            request.user.save()

        except Exception as e:
            messages.error(request, f"Error. Unable to upload Entity: {str(e)}")

    return render(request, 'upload.html', context)



def minigames(request):
    return render(request, 'Minigames.html')

def escape(request):
    return render(request, 'Escape.html')

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
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # If anyone is logged in, log them out first
            if request.user.is_authenticated:
                logout(request)

            # Create the new user
            new_user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )

            # Authenticate and log them in immediately
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Signed in and logged in successfully.')
                return redirect('profile')

        except IntegrityError:
            messages.error(request, 'Username or email already in use.')

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
            if new_quote is not None:
                target_user.quote = new_quote[:100]

        if 'bio' in request.POST:
            new_bio = request.POST.get('bio')
            if new_bio is not None:
                words = new_bio.split()
                trimmed = ' '.join(words[:250])
                target_user.bio = trimmed

        if 'image' in request.FILES:
            target_user.image = request.FILES['image']

        target_user.save()
        messages.success(request, "Profile updated.")

    return render(request, 'profile.html', {'user': target_user})


@login_required
def profile_page(request):
    user = request.user

    if request.method == 'POST':
        # Update quote
        if 'quote' in request.POST:
            new_quote = request.POST.get('quote')
            if new_quote is not None:
                user.quote = new_quote[:100]

        # Update bio
        if 'bio' in request.POST:
            new_bio = request.POST.get('bio')
            if new_bio is not None:
                words = new_bio.split()
                trimmed = ' '.join(words[:250])  # limit to 250 words
                user.bio = trimmed


        # Update profile picture
        if 'image' in request.FILES:
            user.image = request.FILES['image']

        user.save()
        messages.success(request, "Profile updated.")

    return render(request, 'profile.html', {'user': user})



@login_required
def user_library(request, uid):
    target_user = get_object_or_404(User, uid=uid)
    user_entities = Entity.objects.filter(created_by=target_user)
    return render(request, 'userLibrary.html', {'user': target_user, 'entities': user_entities})
