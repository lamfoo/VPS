from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from .models import UserProfile

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return '/dashboard/'

class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Basic validation
        if not all([username, email, password1, password2]):
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, self.template_name)
        
        if password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, self.template_name)
        
        if len(password1) < 8:
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
            return render(request, self.template_name)
        
        # Check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, self.template_name)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está em uso.')
            return render(request, self.template_name)
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type='client'
            )
            
            # Login user
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo à CloudHost Pro!')
            return redirect('/dashboard/')
            
        except Exception as e:
            messages.error(request, 'Erro ao criar conta. Tente novamente.')
            return render(request, self.template_name)
    
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
