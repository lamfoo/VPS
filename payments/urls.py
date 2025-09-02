from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Order Management
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<uuid:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<uuid:order_id>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
    
    # Payment Processing
    path('checkout/<uuid:order_id>/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/paypal/', views.PayPalPaymentView.as_view(), name='paypal_payment'),
    path('payment/2checkout/', views.TwoCheckoutPaymentView.as_view(), name='2checkout_payment'),
    
    # Payment Callbacks and Webhooks
    path('webhooks/paypal/', views.PayPalWebhookView.as_view(), name='paypal_webhook'),
    path('webhooks/2checkout/', views.TwoCheckoutWebhookView.as_view(), name='2checkout_webhook'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
    
    # Invoice Management
    path('invoices/', views.InvoiceListView.as_view(), name='invoices'),
    path('invoices/<uuid:invoice_id>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<uuid:invoice_id>/download/', views.DownloadInvoiceView.as_view(), name='download_invoice'),
    path('invoices/<uuid:invoice_id>/pay/', views.PayInvoiceView.as_view(), name='pay_invoice'),
    
    # Billing and Account Management
    path('billing/', views.BillingView.as_view(), name='billing'),
    path('billing/addresses/', views.BillingAddressListView.as_view(), name='billing_addresses'),
    path('billing/addresses/create/', views.CreateBillingAddressView.as_view(), name='create_billing_address'),
    path('billing/addresses/<int:pk>/edit/', views.EditBillingAddressView.as_view(), name='edit_billing_address'),
    path('billing/addresses/<int:pk>/delete/', views.DeleteBillingAddressView.as_view(), name='delete_billing_address'),
    path('billing/addresses/<int:pk>/set-default/', views.SetDefaultBillingAddressView.as_view(), name='set_default_billing_address'),
    
    # Coupon and Discount Management
    path('coupons/apply/', views.ApplyCouponView.as_view(), name='apply_coupon'),
    path('coupons/remove/', views.RemoveCouponView.as_view(), name='remove_coupon'),
    
    # Payment History and Refunds
    path('payments/', views.PaymentHistoryView.as_view(), name='payment_history'),
    path('payments/<uuid:payment_id>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('refunds/', views.RefundListView.as_view(), name='refunds'),
    path('refunds/request/', views.RequestRefundView.as_view(), name='request_refund'),
    
    # Subscription and Recurring Billing
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscriptions'),
    path('subscriptions/<int:pk>/cancel/', views.CancelSubscriptionView.as_view(), name='cancel_subscription'),
    path('subscriptions/<int:pk>/update/', views.UpdateSubscriptionView.as_view(), name='update_subscription'),
    
    # AJAX endpoints
    path('ajax/calculate-total/', views.CalculateTotalAjaxView.as_view(), name='ajax_calculate_total'),
    path('ajax/validate-coupon/', views.ValidateCouponAjaxView.as_view(), name='ajax_validate_coupon'),
]