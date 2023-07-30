from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('success/', views.success_page, name='success_url'),
    # path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    # Add other URL patterns for your app if needed
]
