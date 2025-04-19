from django.shortcuts import render
from .models import Entity, User


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
    return render(request, 'login.html')

def signin_page(request):
    return render(request, 'signin.html')