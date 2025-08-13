from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
class RegisterView(TemplateView):
    template_name = 'accounts/register.html'
    
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
class ProfileEditView(TemplateView):
    template_name = 'accounts/profile_edit.html'
    
class SettingsView(TemplateView):
    template_name = 'accounts/settings.html'
    
class PasswordChangeView(TemplateView):
    template_name = 'accounts/password_change.html'
    
class VerifyEmailView(TemplateView):
    template_name = 'accounts/verify_email.html'
    
class ResendVerificationView(TemplateView):
    template_name = 'accounts/resend_verification.html'
    
class APIKeysView(TemplateView):
    template_name = 'accounts/api_keys.html'
    
class CreateAPIKeyView(TemplateView):
    template_name = 'accounts/create_api_key.html'
    
class DeleteAPIKeyView(TemplateView):
    template_name = 'accounts/delete_api_key.html'
    
class ActivityLogView(TemplateView):
    template_name = 'accounts/activity_log.html'
