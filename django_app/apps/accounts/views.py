from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomLoginForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f"You are now logged in as {user.username}.")
            return redirect('items:index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {"login_form": form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account until it is confirmed
            user.save()
            
            # Email verification setup
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verification_link = f"{request.scheme}://{current_site.domain}{reverse('accounts:verify_email', kwargs={'uidb64': uid, 'token': token})}"
            
            subject = "Verify your Lost & Found Portal account"
            message = f"Hi {user.username},\n\nPlease click the link below to verify your email address and activate your account:\n\n{verification_link}\n\nThank you!"
            
            try:
                send_mail(
                    subject,
                    message,
                    None, # Uses DEFAULT_FROM_EMAIL
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error to the console (will appear in Render logs)
                print(f"EMAIL SENDING ERROR: {str(e)}")
                # Notify the user that email failed, but account exists
                messages.warning(request, "Your account was created, but we had trouble sending the verification email. Please contact the administrator or check your credentials.")
            
            return redirect('accounts:verification_sent')
        # form is invalid — fall through with errors attached
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {"register_form": form})

def verification_sent_view(request):
    return render(request, 'accounts/verification_sent.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('items:index')

def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been successfully verified! You may now log in.")
        return redirect('accounts:login')
    else:
        messages.error(request, "The verification link was invalid or has expired. Please try registering again.")
        return redirect('accounts:login')

def test_email_view(request):
    from django.http import HttpResponse
    from django.core.mail import send_mail
    import traceback
    
    try:
        send_mail(
            "Test Email from Lost & Found",
            "If you can see this, your email configuration is working perfectly!",
            None,
            [settings.EMAIL_HOST_USER], # Send to yourself
            fail_silently=False,
        )
        return HttpResponse("<h1>Email Sent Successfully!</h1><p>Check your inbox (and spam folder) for the test email.</p>")
    except Exception as e:
        error_details = traceback.format_exc()
        return HttpResponse(f"""
            <h1>Email Failed!</h1>
            <p><b>Configuration being used:</b></p>
            <ul>
                <li>HOST: <code>{settings.EMAIL_HOST}</code></li>
                <li>PORT: <code>{settings.EMAIL_PORT}</code></li>
                <li>USER: <code>{settings.EMAIL_HOST_USER}</code></li>
            </ul>
            <p><b>Error:</b> {str(e)}</p>
            <pre>{error_details}</pre>
            <p><b>Tip:</b> If the HOST looks wrong (e.g. a typo or extra space), fix it in your Render Environment variables.</p>
        """)
