from django.urls import path
from .views import login_view, logout_view, register_view, verify_email_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('verify-email/<uidb64>/<token>/', verify_email_view, name='verify_email'),
]
