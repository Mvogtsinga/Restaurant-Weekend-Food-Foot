"""
URL configuration for weekendfoodfoot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('home/', home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('reserve_table/', views.reserve_table, name='reserve_table'),
    path('contact/', views.contact, name='contact'),
    path('foods/', views.foods, name='foods'),
    path('about/', views.about, name='about'),
    path('account/delete/', views.account_delete, name='account_delete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reservation/cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('reservation/cancel/confirmation/', views.cancel_confirmation, name='cancel_confirmation'),
]
