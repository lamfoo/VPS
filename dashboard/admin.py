from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Notification, SupportTicket, TicketReply, SystemStatus,
    DashboardWidget, APIUsageLog, MaintenanceWindow
)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_profile', 'notification_type', 'is_read', 'is_global', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_global', 'created_at')
    search_fields = ('title', 'message', 'user_profile__user__username')
    readonly_fields = ('created_at', 'read_at')
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('user_profile', 'title', 'message', 'notification_type')
        }),
        ('Settings', {
            'fields': ('is_read', 'is_global', 'expires_at')
        }),
        ('Related Objects', {
            'fields': ('vps_instance',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user', 'vps_instance')
    
    def notification_type_colored(self, obj):
        colors = {
            'info': 'blue',
            'success': 'green',
            'warning': 'orange',
            'error': 'red',
            'vps_created': 'green',
            'vps_suspended': 'red',
            'payment_due': 'orange',
            'payment_received': 'green',
            'maintenance': 'purple',
            'security': 'red'
        }
        color = colors.get(obj.notification_type, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_notification_type_display())
    notification_type_colored.short_description = 'Type'

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'user_profile', 'subject', 'category', 'priority', 'status', 'created_at')
    list_filter = ('category', 'priority', 'status', 'created_at', 'assigned_to')
    search_fields = ('ticket_number', 'subject', 'user_profile__user__username', 'description')
    readonly_fields = ('ticket_id', 'ticket_number', 'created_at', 'updated_at', 'resolved_at', 'closed_at')
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('ticket_number', 'user_profile', 'subject', 'description')
        }),
        ('Classification', {
            'fields': ('category', 'priority', 'status', 'assigned_to')
        }),
        ('Related Objects', {
            'fields': ('vps_instance',)
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('System Information', {
            'fields': ('ticket_id',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at', 'closed_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user_profile__user', 'assigned_to__user', 'vps_instance'
        )
    
    def priority_colored(self, obj):
        colors = {
            'low': 'green',
            'medium': 'blue',
            'high': 'orange',
            'urgent': 'red'
        }
        color = colors.get(obj.priority, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_priority_display())
    priority_colored.short_description = 'Priority'
    
    def status_colored(self, obj):
        colors = {
            'open': 'red',
            'in_progress': 'blue',
            'waiting_customer': 'orange',
            'waiting_admin': 'purple',
            'resolved': 'green',
            'closed': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">OVERDUE</span>')
        return 'No'
    is_overdue_display.short_description = 'Overdue'

@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user_profile', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('ticket__ticket_number', 'user_profile__user__username', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Reply Information', {
            'fields': ('ticket', 'user_profile', 'message', 'is_internal')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('ticket', 'user_profile__user')

@admin.register(SystemStatus)
class SystemStatusAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'status', 'is_active', 'notify_users', 'created_at')
    list_filter = ('status', 'is_active', 'notify_users', 'created_at')
    search_fields = ('service_name', 'description', 'incident_description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Service Information', {
            'fields': ('service_name', 'description', 'status')
        }),
        ('Incident Details', {
            'fields': ('incident_description',)
        }),
        ('Settings', {
            'fields': ('is_active', 'notify_users')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        })
    )
    
    def status_colored(self, obj):
        colors = {
            'operational': 'green',
            'degraded': 'orange',
            'partial_outage': 'red',
            'major_outage': 'darkred',
            'maintenance': 'blue'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'widget_type', 'title', 'is_visible', 'position_x', 'position_y')
    list_filter = ('widget_type', 'is_visible', 'created_at')
    search_fields = ('user_profile__user__username', 'title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Widget Information', {
            'fields': ('user_profile', 'widget_type', 'title', 'is_visible')
        }),
        ('Layout Settings', {
            'fields': ('position_x', 'position_y', 'width', 'height')
        }),
        ('Configuration', {
            'fields': ('refresh_interval', 'config')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user')

@admin.register(APIUsageLog)
class APIUsageLogAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'method', 'endpoint', 'status_code', 'response_time_ms', 'timestamp')
    list_filter = ('method', 'status_code', 'timestamp')
    search_fields = ('user_profile__user__username', 'endpoint', 'ip_address')
    readonly_fields = ('user_profile', 'endpoint', 'method', 'status_code', 'response_time_ms', 
                      'request_size_bytes', 'response_size_bytes', 'ip_address', 'user_agent', 
                      'timestamp', 'metadata')
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user_profile', 'endpoint', 'method', 'status_code')
        }),
        ('Performance Metrics', {
            'fields': ('response_time_ms', 'request_size_bytes', 'response_size_bytes')
        }),
        ('Client Information', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def status_code_colored(self, obj):
        if 200 <= obj.status_code < 300:
            color = 'green'
        elif 300 <= obj.status_code < 400:
            color = 'blue'
        elif 400 <= obj.status_code < 500:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {};">{}</span>', color, obj.status_code)
    status_code_colored.short_description = 'Status Code'

@admin.register(MaintenanceWindow)
class MaintenanceWindowAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_time', 'end_time', 'notify_users', 'notification_sent')
    list_filter = ('status', 'notify_users', 'notification_sent', 'start_time')
    search_fields = ('title', 'description', 'affected_services')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Maintenance Information', {
            'fields': ('title', 'description', 'status', 'affected_services')
        }),
        ('Scheduling', {
            'fields': ('start_time', 'end_time')
        }),
        ('Notifications', {
            'fields': ('notify_users', 'notification_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def status_colored(self, obj):
        colors = {
            'scheduled': 'blue',
            'in_progress': 'orange',
            'completed': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: orange; font-weight: bold;">ACTIVE</span>')
        return 'No'
    is_active_display.short_description = 'Active'
    
    def duration_display(self, obj):
        return str(obj.duration)
    duration_display.short_description = 'Duration'
