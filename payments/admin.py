from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, Payment, Invoice, Refund, BillingAddress, Coupon, CouponUsage

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user_profile', 'vps_package', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'billing_cycle', 'created_at', 'vps_package')
    search_fields = ('order_number', 'user_profile__user__username', 'hostname')
    readonly_fields = ('order_id', 'order_number', 'created_at', 'updated_at', 'completed_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user_profile', 'status')
        }),
        ('VPS Configuration', {
            'fields': ('vps_package', 'quantity', 'hostname', 'billing_cycle')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Authentication', {
            'fields': ('root_password', 'ssh_keys'),
            'classes': ('collapse',)
        }),
        ('Billing Period', {
            'fields': ('billing_start_date', 'billing_end_date')
        }),
        ('System Information', {
            'fields': ('order_id', 'metadata', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user', 'vps_package')
    
    def status_colored(self, obj):
        colors = {
            'completed': 'green',
            'paid': 'blue',
            'pending': 'orange',
            'processing': 'purple',
            'failed': 'red',
            'cancelled': 'gray',
            'refunded': 'brown'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'currency', 'created_at')
    search_fields = ('transaction_id', 'gateway_transaction_id', 'order__order_number', 'payer_email')
    readonly_fields = ('payment_id', 'transaction_id', 'gateway_response', 'created_at', 'processed_at')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'payment_method', 'amount', 'currency', 'status')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'gateway_transaction_id')
        }),
        ('Payer Information', {
            'fields': ('payer_email', 'payer_name')
        }),
        ('Gateway Response', {
            'fields': ('gateway_response',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('payment_id', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order__user_profile__user')
    
    def status_colored(self, obj):
        colors = {
            'completed': 'green',
            'processing': 'blue',
            'pending': 'orange',
            'failed': 'red',
            'cancelled': 'gray',
            'refunded': 'brown',
            'partially_refunded': 'orange'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user_profile', 'total_amount', 'status', 'issue_date', 'due_date')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'user_profile__user__username', 'description')
    readonly_fields = ('invoice_id', 'invoice_number', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'user_profile', 'status', 'description')
        }),
        ('Related Objects', {
            'fields': ('order', 'vps_instance')
        }),
        ('Amounts', {
            'fields': ('amount', 'tax_amount', 'total_amount')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date', 'paid_date')
        }),
        ('Billing Period', {
            'fields': ('billing_period_start', 'billing_period_end')
        }),
        ('System Information', {
            'fields': ('invoice_id', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user')
    
    def status_colored(self, obj):
        colors = {
            'paid': 'green',
            'sent': 'blue',
            'draft': 'gray',
            'overdue': 'red',
            'cancelled': 'black'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Yes</span>')
        return 'No'
    is_overdue_display.short_description = 'Overdue'

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('payment', 'amount', 'reason', 'status', 'created_at')
    list_filter = ('reason', 'status', 'created_at')
    search_fields = ('payment__transaction_id', 'description', 'gateway_refund_id')
    readonly_fields = ('refund_id', 'gateway_response', 'created_at', 'processed_at')
    
    fieldsets = (
        ('Refund Information', {
            'fields': ('payment', 'amount', 'reason', 'status', 'description')
        }),
        ('Processing', {
            'fields': ('processed_by', 'gateway_refund_id')
        }),
        ('Gateway Response', {
            'fields': ('gateway_response',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('refund_id',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('payment__order__user_profile__user')

@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'first_name', 'last_name', 'city', 'country', 'is_default')
    list_filter = ('is_default', 'country', 'created_at')
    search_fields = ('user_profile__user__username', 'first_name', 'last_name', 'company', 'city')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user_profile', 'first_name', 'last_name', 'company')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Settings', {
            'fields': ('is_default',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_profile__user')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'discount_type', 'discount_value', 'current_uses', 'is_active', 'valid_until')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('current_uses', 'created_at', 'updated_at')
    filter_horizontal = ('applicable_packages',)
    
    fieldsets = (
        ('Coupon Information', {
            'fields': ('code', 'name', 'description', 'is_active')
        }),
        ('Discount Configuration', {
            'fields': ('discount_type', 'discount_value', 'minimum_order_amount')
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'max_uses_per_user', 'current_uses')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Package Restrictions', {
            'fields': ('applicable_packages',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def is_valid_display(self, obj):
        if obj.is_valid:
            return format_html('<span style="color: green;">Valid</span>')
        return format_html('<span style="color: red;">Invalid</span>')
    is_valid_display.short_description = 'Valid'

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user_profile', 'order', 'discount_amount', 'used_at')
    list_filter = ('used_at', 'coupon')
    search_fields = ('coupon__code', 'user_profile__user__username', 'order__order_number')
    readonly_fields = ('coupon', 'user_profile', 'order', 'discount_amount', 'used_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('coupon', 'user_profile__user', 'order')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
