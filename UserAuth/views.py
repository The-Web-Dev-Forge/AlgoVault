from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import PasswordResetToken

def login_view(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.POST.get('username')  # Form field name is 'username' but contains email
            password = request.POST.get('password')
        
        # Authenticate using email instead of username
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            if request.content_type == 'application/json':
                return JsonResponse({'success': True, 'message': 'Login successful'})
            else:
                messages.success(request, 'Login successful!')
                return redirect('/')  # Redirect to home page
        else:
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
            else:
                messages.error(request, 'Invalid email or password')
    
    return render(request, 'UserAuth/login.html')

def signup_view(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
        else:
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password1', '')
            confirm_password = request.POST.get('password2', '')
        
        # Validate required fields
        if not all([first_name, last_name, email, password, confirm_password]):
            message = 'All fields are required'
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'message': message})
            else:
                messages.error(request, message)
                return render(request, 'UserAuth/signup.html')
        
        if password != confirm_password:
            message = 'Passwords do not match'
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'message': message})
            else:
                messages.error(request, message)
                return render(request, 'UserAuth/signup.html')
        
        # Use email as username
        username = email
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            message = 'Email already exists'
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'message': message})
            else:
                messages.error(request, message)
                return render(request, 'UserAuth/signup.html')
        
        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            
            if request.content_type == 'application/json':
                return JsonResponse({'success': True, 'message': 'Account created successfully'})
            else:
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('UserAuth:login')
        except Exception as e:
            message = f'Error creating account: {str(e)}'
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'message': message})
            else:
                messages.error(request, message)
                return render(request, 'UserAuth/signup.html')
    
    return render(request, 'UserAuth/signup.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('UserAuth:login')

def forgot_password_view(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email')
        else:
            email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            # Create password reset token
            token = PasswordResetToken.objects.create(user=user)
            
            # Send password reset email
            reset_url = request.build_absolute_uri(
                reverse('UserAuth:reset_password', kwargs={'token': str(token.token)})
            )
            
            # Email subject and message
            subject = 'Password Reset Request - AlgoVault'
            message = f"""
Hi {user.first_name or user.username},

You requested a password reset for your AlgoVault account. Click the link below to reset your password:

{reset_url}

This link will expire in 1 hour for security reasons.

If you didn't request this password reset, please ignore this email.

Best regards,
AlgoVault Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                if request.content_type == 'application/json':
                    return JsonResponse({'success': True, 'message': 'Password reset email sent successfully!'})
                else:
                    messages.success(request, 'Password reset email sent! Please check your inbox.')
                    return render(request, 'UserAuth/forgot_password.html')
                    
            except Exception as e:
                # If email sending fails, show the link as fallback
                message = f'Email sending failed. Here is your reset link: {reset_url}'
                
                if request.content_type == 'application/json':
                    return JsonResponse({'success': True, 'message': message, 'reset_url': reset_url})
                else:
                    messages.warning(request, f'Email could not be sent. Click here to reset: {reset_url}')
                    return render(request, 'UserAuth/forgot_password.html', {'reset_url': reset_url})
                
        except User.DoesNotExist:
            message = 'No user found with this email address'
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'message': message})
            else:
                messages.error(request, message)
    
    return render(request, 'UserAuth/forgot_password.html')

def reset_password_view(request, token):
    try:
        reset_token = get_object_or_404(PasswordResetToken, token=token)
        
        if reset_token.is_expired() or reset_token.is_used:
            messages.error(request, 'Invalid or expired reset token')
            return redirect('UserAuth:forgot_password')
        
        if request.method == 'POST':
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                password = data.get('password')
                confirm_password = data.get('confirm_password')
            else:
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                message = 'Passwords do not match'
                if request.content_type == 'application/json':
                    return JsonResponse({'success': False, 'message': message})
                else:
                    messages.error(request, message)
                    return render(request, 'UserAuth/reset_password.html', {'token': token})
            
            # Update password
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            if request.content_type == 'application/json':
                return JsonResponse({'success': True, 'message': 'Password reset successful'})
            else:
                messages.success(request, 'Password reset successfully! Please login.')
                return redirect('UserAuth:login')
        
        return render(request, 'UserAuth/reset_password.html', {'token': token})
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset token')
        return redirect('UserAuth:forgot_password')
