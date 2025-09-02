from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile
from vps.models import VPSInstance
import uuid

class Notification(models.Model):
    """System notifications for users"""
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('vps_created', 'VPS Created'),
        ('vps_suspended', 'VPS Suspended'),
        ('payment_due', 'Payment Due'),
        ('payment_received', 'Payment Received'),
        ('maintenance', 'Maintenance'),
        ('security', 'Security Alert'),
    ]
    
    # Notification details
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    
    # Notification settings
    is_read = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False, help_text="Show to all users")
    
    # Related objects
    vps_instance = models.ForeignKey(VPSInstance, on_delete=models.CASCADE, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        
    def __str__(self):
        user = self.user_profile.user.username if self.user_profile else 'Global'
        return f"{user} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

class SupportTicket(models.Model):
    """Customer support tickets"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_customer', 'Waiting for Customer'),
        ('waiting_admin', 'Waiting for Admin'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'General Inquiry'),
        ('technical', 'Technical Support'),
        ('billing', 'Billing'),
        ('vps_issue', 'VPS Issue'),
        ('feature_request', 'Feature Request'),
        ('bug_report', 'Bug Report'),
        ('abuse', 'Abuse Report'),
    ]
    
    # Ticket identification
    ticket_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    ticket_number = models.CharField(max_length=20, unique=True)
    
    # Customer information
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='support_tickets')
    
    # Ticket details
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Assignment
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    
    # Related objects
    vps_instance = models.ForeignKey(VPSInstance, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    class Meta:
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.subject}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Generate ticket number
            self.ticket_number = f"TK{timezone.now().strftime('%Y%m')}{str(self.ticket_id)[:6].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """Check if ticket response is overdue based on priority"""
        if self.status in ['resolved', 'closed']:
            return False
        
        hours_since_created = (timezone.now() - self.created_at).total_seconds() / 3600
        
        # SLA response times in hours
        sla_hours = {
            'urgent': 2,
            'high': 8,
            'medium': 24,
            'low': 48,
        }
        
        return hours_since_created > sla_hours.get(self.priority, 24)

class TicketReply(models.Model):
    """Replies to support tickets"""
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='replies')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    # Reply content
    message = models.TextField()
    
    # Settings
    is_internal = models.BooleanField(default=False, help_text="Internal note, not visible to customer")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ticket Reply'
        verbose_name_plural = 'Ticket Replies'
        ordering = ['created_at']
        
    def __str__(self):
        return f"Reply to {self.ticket.ticket_number} by {self.user_profile.user.username}"

class SystemStatus(models.Model):
    """System and service status tracking"""
    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('degraded', 'Degraded Performance'),
        ('partial_outage', 'Partial Outage'),
        ('major_outage', 'Major Outage'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    # Service information
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operational')
    
    # Status details
    incident_description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    notify_users = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'System Status'
        verbose_name_plural = 'System Status'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.service_name} - {self.get_status_display()}"

class DashboardWidget(models.Model):
    """Customizable dashboard widgets for users"""
    WIDGET_TYPE_CHOICES = [
        ('vps_overview', 'VPS Overview'),
        ('usage_stats', 'Usage Statistics'),
        ('billing_summary', 'Billing Summary'),
        ('recent_activity', 'Recent Activity'),
        ('notifications', 'Notifications'),
        ('support_tickets', 'Support Tickets'),
        ('system_status', 'System Status'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='dashboard_widgets')
    
    # Widget configuration
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    
    # Layout settings
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    width = models.IntegerField(default=6)  # Bootstrap grid columns
    height = models.IntegerField(default=4)  # Grid rows
    
    # Widget settings
    is_visible = models.BooleanField(default=True)
    refresh_interval = models.IntegerField(default=300, help_text="Refresh interval in seconds")
    
    # Configuration data
    config = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
        unique_together = ['user_profile', 'widget_type']
        ordering = ['position_y', 'position_x']
        
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.title}"

class APIUsageLog(models.Model):
    """Track API usage for monitoring and billing"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='api_usage_logs')
    
    # Request details
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    
    # Timing and usage
    response_time_ms = models.IntegerField()
    request_size_bytes = models.IntegerField(default=0)
    response_size_bytes = models.IntegerField(default=0)
    
    # Request metadata
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Timestamps
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'API Usage Log'
        verbose_name_plural = 'API Usage Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user_profile', '-timestamp']),
            models.Index(fields=['endpoint', '-timestamp']),
        ]
        
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.method} {self.endpoint}"

class MaintenanceWindow(models.Model):
    """Scheduled maintenance windows"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Maintenance details
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Affected services
    affected_services = models.CharField(max_length=500, help_text="Comma-separated list of affected services")
    
    # Scheduling
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Notifications
    notify_users = models.BooleanField(default=True)
    notification_sent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Maintenance Window'
        verbose_name_plural = 'Maintenance Windows'
        ordering = ['start_time']
        
    def __str__(self):
        return f"{self.title} - {self.start_time.date()}"
    
    @property
    def is_active(self):
        """Check if maintenance is currently active"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time and self.status == 'in_progress'
    
    @property
    def duration(self):
        """Get maintenance duration"""
        return self.end_time - self.start_time
