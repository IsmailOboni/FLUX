from django.urls import path
from .views import CustomPasswordResetView  # Import the custom view
from django.contrib.auth import views as auth_views
from . import views
from .views import register
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomPasswordResetConfirmView

urlpatterns = [
    path('', views.home, name='home'),
   
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('intructors/', views.intructors, name='intructors'),
    path('learners/', views.learners, name='learners'),

    path('forget/', views.forget, name='forget'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Custom Password Reset URL
    path('custom-password-reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),

    # Handle the custom password reset confirmation URL
    path('custom-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView, name='password_reset_confirm'),

    # Confirmation and completion views
    path('custom-reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/custom_password_reset_complete.html"
    ), name='password_reset_complete'),
]