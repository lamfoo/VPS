from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile
import uuid
import json

class VPSPackage(models.Model):
    """VPS hosting packages available for purchase"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Hardware specifications
    cpu_cores = models.IntegerField()
    ram_gb = models.IntegerField()
    storage_gb = models.IntegerField()
    bandwidth_gb = models.IntegerField(help_text="Monthly bandwidth in GB")
    
    # Pricing
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Contabo configuration
    contabo_image_id = models.CharField(max_length=100, help_text="Contabo image ID")
    contabo_product_id = models.CharField(max_length=100, help_text="Contabo product ID")
    
    # Package settings
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    max_instances_per_user = models.IntegerField(default=10)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'VPS Package'
        verbose_name_plural = 'VPS Packages'
        ordering = ['monthly_price']
        
    def __str__(self):
        return f"{self.name} - ${self.monthly_price}/month"

class VPSInstance(models.Model):
    """Individual VPS instances owned by users"""
    STATUS_CHOICES = [
        ('pending', 'Pending Creation'),
        ('creating', 'Being Created'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('stopped', 'Stopped'),
        ('error', 'Error'),
        ('terminated', 'Terminated'),
    ]
    
    # Basic information
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='vps_instances')
    package = models.ForeignKey(VPSPackage, on_delete=models.PROTECT)
    
    # Instance identifiers
    instance_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    contabo_instance_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    # Instance details
    hostname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Authentication
    root_password = models.CharField(max_length=255, help_text="Encrypted root password")
    ssh_keys = models.TextField(blank=True, help_text="SSH public keys (JSON array)")
    
    # Billing
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2)
    next_billing_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    # Metadata and configuration
    metadata = models.JSONField(default=dict, blank=True)
    auto_renewal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'VPS Instance'
        verbose_name_plural = 'VPS Instances'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.hostname} ({self.user_profile.user.username})"
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def days_until_expiry(self):
        if self.expires_at:
            delta = self.expires_at.date() - timezone.now().date()
            return delta.days
        return None
    
    def get_ssh_keys_list(self):
        """Return SSH keys as a Python list"""
        try:
            return json.loads(self.ssh_keys) if self.ssh_keys else []
        except json.JSONDecodeError:
            return []
    
    def set_ssh_keys_list(self, keys_list):
        """Set SSH keys from a Python list"""
        self.ssh_keys = json.dumps(keys_list)

class VPSAction(models.Model):
    """Track actions performed on VPS instances"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('start', 'Start'),
        ('stop', 'Stop'),
        ('restart', 'Restart'),
        ('rebuild', 'Rebuild'),
        ('resize', 'Resize'),
        ('backup', 'Backup'),
        ('restore', 'Restore'),
        ('suspend', 'Suspend'),
        ('unsuspend', 'Unsuspend'),
        ('terminate', 'Terminate'),
        ('password_reset', 'Password Reset'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    vps_instance = models.ForeignKey(VPSInstance, on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Action details
    initiated_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    
    # Contabo tracking
    contabo_task_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'VPS Action'
        verbose_name_plural = 'VPS Actions'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.vps_instance.hostname} - {self.get_action_display()} ({self.status})"
    
    @property
    def duration(self):
        """Calculate action duration if completed"""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None

class VPSUsageStats(models.Model):
    """Track VPS usage statistics for billing and monitoring"""
    vps_instance = models.ForeignKey(VPSInstance, on_delete=models.CASCADE, related_name='usage_stats')
    
    # Usage metrics
    cpu_usage_percent = models.FloatField(default=0)
    memory_usage_mb = models.IntegerField(default=0)
    disk_usage_gb = models.FloatField(default=0)
    bandwidth_used_gb = models.FloatField(default=0)
    
    # Network stats
    network_in_gb = models.FloatField(default=0)
    network_out_gb = models.FloatField(default=0)
    
    # Timestamp
    recorded_at = models.DateTimeField(auto_now_add=True)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    class Meta:
        verbose_name = 'VPS Usage Stats'
        verbose_name_plural = 'VPS Usage Stats'
        ordering = ['-recorded_at']
        unique_together = ['vps_instance', 'period_start']
        
    def __str__(self):
        return f"{self.vps_instance.hostname} - {self.recorded_at.date()}"

class VPSBackup(models.Model):
    """VPS backup management"""
    BACKUP_TYPE_CHOICES = [
        ('manual', 'Manual'),
        ('scheduled', 'Scheduled'),
        ('auto', 'Automatic'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('creating', 'Creating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    vps_instance = models.ForeignKey(VPSInstance, on_delete=models.CASCADE, related_name='backups')
    
    # Backup details
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # File information
    size_gb = models.FloatField(default=0)
    file_path = models.CharField(max_length=500, blank=True)
    
    # Contabo backup ID
    contabo_backup_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'VPS Backup'
        verbose_name_plural = 'VPS Backups'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.vps_instance.hostname} - {self.name}"
    
    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
