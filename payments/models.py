from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile
from vps.models import VPSPackage, VPSInstance
import uuid
from decimal import Decimal

class Order(models.Model):
    """Orders for VPS packages and services"""
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Order identification
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order_number = models.CharField(max_length=20, unique=True)
    
    # Customer information
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    
    # Order details
    vps_package = models.ForeignKey(VPSPackage, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # VPS configuration
    hostname = models.CharField(max_length=100)
    root_password = models.CharField(max_length=255, help_text="User-provided root password")
    ssh_keys = models.TextField(blank=True, help_text="SSH public keys")
    
    # Billing period
    billing_cycle = models.CharField(max_length=20, default='monthly')
    billing_start_date = models.DateField()
    billing_end_date = models.DateField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Order #{self.order_number} - {self.user_profile.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number
            self.order_number = f"VPS{timezone.now().strftime('%Y%m%d')}{str(self.order_id)[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_paid(self):
        return self.status in ['paid', 'processing', 'completed']

class Payment(models.Model):
    """Payment transactions for orders"""
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('2checkout', '2Checkout'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    # Payment identification
    payment_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    transaction_id = models.CharField(max_length=100, unique=True)
    
    # Related order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Gateway information
    gateway_transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    payer_email = models.EmailField(blank=True)
    payer_name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Payment {self.transaction_id} - ${self.amount}"
    
    @property
    def is_successful(self):
        return self.status == 'completed'

class Invoice(models.Model):
    """Invoices for orders and recurring billing"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Invoice identification
    invoice_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    invoice_number = models.CharField(max_length=20, unique=True)
    
    # Customer information
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='invoices')
    
    # Related order or VPS instance
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    vps_instance = models.ForeignKey(VPSInstance, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Invoice details
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Invoice status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    # Billing period (for recurring invoices)
    billing_period_start = models.DateField(null=True, blank=True)
    billing_period_end = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional information
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Invoice #{self.invoice_number} - ${self.total_amount}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number
            self.invoice_number = f"INV{timezone.now().strftime('%Y%m')}{str(self.invoice_id)[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        return self.status != 'paid' and self.due_date < timezone.now().date()

class Refund(models.Model):
    """Refund transactions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    REASON_CHOICES = [
        ('customer_request', 'Customer Request'),
        ('technical_issue', 'Technical Issue'),
        ('billing_error', 'Billing Error'),
        ('fraud', 'Fraud'),
        ('chargeback', 'Chargeback'),
        ('other', 'Other'),
    ]
    
    # Refund identification
    refund_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Related payment
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    
    # Refund details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField()
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Gateway information
    gateway_refund_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    processed_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Refund ${self.amount} for Payment {self.payment.transaction_id}"

class BillingAddress(models.Model):
    """Billing addresses for users"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='billing_addresses')
    
    # Address information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=100, blank=True)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    
    # Settings
    is_default = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Billing Address'
        verbose_name_plural = 'Billing Addresses'
        ordering = ['-is_default', '-created_at']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.country}"

class Coupon(models.Model):
    """Discount coupons and promotional codes"""
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    ]
    
    # Coupon identification
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Discount details
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Usage limits
    max_uses = models.IntegerField(null=True, blank=True, help_text="Leave blank for unlimited uses")
    max_uses_per_user = models.IntegerField(default=1)
    current_uses = models.IntegerField(default=0)
    
    # Validity period
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Restrictions
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    applicable_packages = models.ManyToManyField(VPSPackage, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.max_uses is None or self.current_uses < self.max_uses)
        )
    
    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount"""
        if not self.is_valid or order_amount < self.minimum_order_amount:
            return Decimal('0.00')
        
        if self.discount_type == 'percentage':
            return (order_amount * self.discount_value / 100).quantize(Decimal('0.01'))
        else:  # fixed_amount
            return min(self.discount_value, order_amount)

class CouponUsage(models.Model):
    """Track coupon usage by users"""
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Coupon Usage'
        verbose_name_plural = 'Coupon Usages'
        unique_together = ['coupon', 'order']
        ordering = ['-used_at']
        
    def __str__(self):
        return f"{self.coupon.code} used by {self.user_profile.user.username}"
