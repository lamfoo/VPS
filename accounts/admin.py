from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile, APIKey, ActivityLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'company_name', 'is_verified', 'created_at')
    list_filter = ('user_type', 'is_verified', 'email_notifications', 'sms_notifications', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'company_name', 'phone_number')
    readonly_fields = ('verification_token', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type', 'is_verified')
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'company_name')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Notification Settings', {
            'fields': ('email_notifications', 'sms_notifications')
        }),
        ('System Information', {
            'fields': ('verification_token', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'name', 'service', 'is_active', 'created_at', 'last_used')
    list_filter = ('service', 'is_active', 'created_at', 'last_used')
    search_fields = ('user_profile__user__username', 'name', 'service')
    readonly_fields = ('encrypted_key', 'encrypted_secret', 'created_at', 'updated_at', 'last_used')
    
    fieldsets = (
        ('API Key Information', {
            'fields': ('user_profile', 'name', 'service', 'is_active')
        }),
        ('Encrypted Data', {
            'fields': ('encrypted_key', 'encrypted_secret'),
            'classes': ('collapse',),
            'description': 'Encrypted credentials - cannot be viewed in plain text'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_used'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'action', 'description_short', 'ip_address', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user_profile__user__username', 'description', 'ip_address')
    readonly_fields = ('user_profile', 'action', 'description', 'ip_address', 'user_agent', 'metadata', 'created_at')
    date_hierarchy = 'created_at'
    
    def description_short(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_short.short_description = 'Description'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# Extend the default User admin to show profile information
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
