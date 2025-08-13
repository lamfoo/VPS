from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import VPSPackage, VPSInstance, VPSAction, VPSUsageStats, VPSBackup

@admin.register(VPSPackage)
class VPSPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpu_cores', 'ram_gb', 'storage_gb', 'monthly_price', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Package Information', {
            'fields': ('name', 'description', 'is_active', 'is_featured')
        }),
        ('Hardware Specifications', {
            'fields': ('cpu_cores', 'ram_gb', 'storage_gb', 'bandwidth_gb')
        }),
        ('Pricing', {
            'fields': ('monthly_price', 'setup_fee')
        }),
        ('Contabo Configuration', {
            'fields': ('contabo_image_id', 'contabo_product_id')
        }),
        ('Limits', {
            'fields': ('max_instances_per_user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request)

@admin.register(VPSInstance)
class VPSInstanceAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'user_profile', 'package', 'ip_address', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'auto_renewal', 'package', 'created_at')
    search_fields = ('hostname', 'user_profile__user__username', 'ip_address', 'contabo_instance_id')
    readonly_fields = ('instance_id', 'contabo_instance_id', 'created_at', 'updated_at', 'last_accessed')
    
    fieldsets = (
        ('Instance Information', {
            'fields': ('user_profile', 'package', 'hostname', 'status')
        }),
        ('Network Information', {
            'fields': ('ip_address',)
        }),
        ('Authentication', {
            'fields': ('root_password', 'ssh_keys'),
            'classes': ('collapse',)
        }),
        ('Billing Information', {
            'fields': ('monthly_cost', 'next_billing_date', 'is_paid', 'auto_renewal', 'expires_at')
        }),
        ('System IDs', {
            'fields': ('instance_id', 'contabo_instance_id'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_accessed'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user', 'package')
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user_profile.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user_profile.user.username)
    user_link.short_description = 'User'
    
    def status_colored(self, obj):
        colors = {
            'active': 'green',
            'pending': 'orange',
            'creating': 'blue',
            'suspended': 'red',
            'stopped': 'gray',
            'error': 'red',
            'terminated': 'black'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'

@admin.register(VPSAction)
class VPSActionAdmin(admin.ModelAdmin):
    list_display = ('vps_instance', 'action', 'status', 'initiated_by', 'created_at', 'duration_display')
    list_filter = ('action', 'status', 'created_at')
    search_fields = ('vps_instance__hostname', 'initiated_by__user__username', 'description')
    readonly_fields = ('vps_instance', 'action', 'initiated_by', 'created_at', 'started_at', 'completed_at', 'duration_display')
    
    fieldsets = (
        ('Action Information', {
            'fields': ('vps_instance', 'action', 'status', 'initiated_by')
        }),
        ('Details', {
            'fields': ('description', 'error_message')
        }),
        ('Contabo Tracking', {
            'fields': ('contabo_task_id',)
        }),
        ('Timing', {
            'fields': ('created_at', 'started_at', 'completed_at', 'duration_display'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        })
    )
    
    def duration_display(self, obj):
        if obj.duration:
            return str(obj.duration)
        return '-'
    duration_display.short_description = 'Duration'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vps_instance', 'initiated_by__user')
    
    def has_add_permission(self, request):
        return False

@admin.register(VPSUsageStats)
class VPSUsageStatsAdmin(admin.ModelAdmin):
    list_display = ('vps_instance', 'cpu_usage_percent', 'memory_usage_mb', 'disk_usage_gb', 'bandwidth_used_gb', 'recorded_at')
    list_filter = ('recorded_at', 'vps_instance__package')
    search_fields = ('vps_instance__hostname', 'vps_instance__user_profile__user__username')
    readonly_fields = ('vps_instance', 'recorded_at', 'period_start', 'period_end')
    date_hierarchy = 'recorded_at'
    
    fieldsets = (
        ('Instance', {
            'fields': ('vps_instance',)
        }),
        ('Usage Metrics', {
            'fields': ('cpu_usage_percent', 'memory_usage_mb', 'disk_usage_gb', 'bandwidth_used_gb')
        }),
        ('Network Stats', {
            'fields': ('network_in_gb', 'network_out_gb')
        }),
        ('Time Period', {
            'fields': ('recorded_at', 'period_start', 'period_end'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vps_instance__user_profile__user')
    
    def has_add_permission(self, request):
        return False

@admin.register(VPSBackup)
class VPSBackupAdmin(admin.ModelAdmin):
    list_display = ('vps_instance', 'name', 'backup_type', 'status', 'size_gb', 'created_at', 'expires_at')
    list_filter = ('backup_type', 'status', 'created_at', 'expires_at')
    search_fields = ('vps_instance__hostname', 'name', 'description')
    readonly_fields = ('contabo_backup_id', 'created_at', 'completed_at')
    
    fieldsets = (
        ('Backup Information', {
            'fields': ('vps_instance', 'name', 'description', 'backup_type', 'status')
        }),
        ('File Information', {
            'fields': ('size_gb', 'file_path')
        }),
        ('Contabo Information', {
            'fields': ('contabo_backup_id',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at', 'expires_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vps_instance__user_profile__user')
    
    def status_colored(self, obj):
        colors = {
            'completed': 'green',
            'pending': 'orange',
            'creating': 'blue',
            'failed': 'red',
            'expired': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'

# Custom admin site configuration
admin.site.site_header = 'VPS Reseller Admin'
admin.site.site_title = 'VPS Reseller Admin Portal'
admin.site.index_title = 'Welcome to VPS Reseller Administration'
