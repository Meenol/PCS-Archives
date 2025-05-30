"""
URL configuration for pcsarchive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import home_page, login_page, signin_page, entity_detail, profile_page, user_profile, upload_entity, minigames, escape, about_page, user_library, delete_entity, delete_account, logout
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('login/', login_page, name='login'),
    path('signin/', signin_page, name='signin'),
    path('admin/', admin.site.urls),
    path('entity/<int:eid>/', entity_detail, name='entity_detail'),
    path('profile/', profile_page, name='profile'),
    path('user/<int:uid>/', user_profile, name='user_profile'),
    path('upload/', upload_entity, name='upload'),
    path('Minigames/', minigames, name='minigames'),
    path('Escape/', escape, name='escape'),
    path('user/<int:uid>/library/', user_library, name='user_library'),
    path('entity/delete/<int:eid>/', delete_entity, name='delete_entity'),
    path('delete-account/', delete_account, name='delete_account'),
    path('logout/', logout, name='logout'),

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
