from django.urls import path
from .views import login_view, logout_view, register_view, verify_email_view, verification_sent_view, temporary_setup_admin

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('verification-sent/', verification_sent_view, name='verification_sent'),
    path('verify-email/<uidb64>/<token>/', verify_email_view, name='verify_email'),
    path('setup-admin-secret/', temporary_setup_admin, name='setup_admin'),
]
