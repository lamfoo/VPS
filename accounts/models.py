from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from cryptography.fernet import Fernet
import uuid

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('client', 'Client'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Account settings
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        
    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'
    
    @property
    def is_client(self):
        return self.user_type == 'client'
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

class APIKey(models.Model):
    """Model to store encrypted API keys and credentials for users"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100, help_text="Friendly name for this API key")
    service = models.CharField(max_length=50, help_text="Service name (e.g., 'contabo', 'paypal')")
    
    # Encrypted fields
    encrypted_key = models.TextField()
    encrypted_secret = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
        unique_together = ['user_profile', 'service']
        
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.service}"
    
    def set_credentials(self, key, secret='', encryption_key=None):
        """Encrypt and store credentials"""
        if not encryption_key:
            encryption_key = Fernet.generate_key()
        
        fernet = Fernet(encryption_key)
        self.encrypted_key = fernet.encrypt(key.encode()).decode()
        if secret:
            self.encrypted_secret = fernet.encrypt(secret.encode()).decode()
        
        return encryption_key
    
    def get_credentials(self, encryption_key):
        """Decrypt and return credentials"""
        try:
            fernet = Fernet(encryption_key)
            key = fernet.decrypt(self.encrypted_key.encode()).decode()
            secret = ''
            if self.encrypted_secret:
                secret = fernet.decrypt(self.encrypted_secret.encode()).decode()
            return key, secret
        except Exception:
            return None, None

class ActivityLog(models.Model):
    """Model to track user activities and system events"""
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('vps_create', 'VPS Created'),
        ('vps_delete', 'VPS Deleted'),
        ('vps_start', 'VPS Started'),
        ('vps_stop', 'VPS Stopped'),
        ('vps_restart', 'VPS Restarted'),
        ('payment_success', 'Payment Successful'),
        ('payment_failed', 'Payment Failed'),
        ('profile_update', 'Profile Updated'),
        ('password_change', 'Password Changed'),
        ('api_call', 'API Call Made'),
        ('error', 'System Error'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Additional context data
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-created_at']
        
    def __str__(self):
        user = self.user_profile.user.username if self.user_profile else 'System'
        return f"{user} - {self.get_action_display()} at {self.created_at}"
