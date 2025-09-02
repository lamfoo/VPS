from django.shortcuts import render
from django.views.generic import TemplateView

class OrderListView(TemplateView):
    template_name = 'payments/orders.html'

class OrderDetailView(TemplateView):
    template_name = 'payments/order_detail.html'

class CancelOrderView(TemplateView):
    template_name = 'payments/cancel_order.html'

class CheckoutView(TemplateView):
    template_name = 'payments/checkout.html'

class PayPalPaymentView(TemplateView):
    template_name = 'payments/paypal_payment.html'

class TwoCheckoutPaymentView(TemplateView):
    template_name = 'payments/2checkout_payment.html'

class PayPalWebhookView(TemplateView):
    template_name = 'payments/paypal_webhook.html'

class TwoCheckoutWebhookView(TemplateView):
    template_name = 'payments/2checkout_webhook.html'

class PaymentSuccessView(TemplateView):
    template_name = 'payments/payment_success.html'

class PaymentCancelView(TemplateView):
    template_name = 'payments/payment_cancel.html'

class InvoiceListView(TemplateView):
    template_name = 'payments/invoices.html'

class InvoiceDetailView(TemplateView):
    template_name = 'payments/invoice_detail.html'

class DownloadInvoiceView(TemplateView):
    template_name = 'payments/download_invoice.html'

class PayInvoiceView(TemplateView):
    template_name = 'payments/pay_invoice.html'

class BillingView(TemplateView):
    template_name = 'payments/billing.html'

class BillingAddressListView(TemplateView):
    template_name = 'payments/billing_addresses.html'

class CreateBillingAddressView(TemplateView):
    template_name = 'payments/create_billing_address.html'

class EditBillingAddressView(TemplateView):
    template_name = 'payments/edit_billing_address.html'

class DeleteBillingAddressView(TemplateView):
    template_name = 'payments/delete_billing_address.html'

class SetDefaultBillingAddressView(TemplateView):
    template_name = 'payments/set_default_billing_address.html'

class ApplyCouponView(TemplateView):
    template_name = 'payments/apply_coupon.html'

class RemoveCouponView(TemplateView):
    template_name = 'payments/remove_coupon.html'

class PaymentHistoryView(TemplateView):
    template_name = 'payments/payment_history.html'

class PaymentDetailView(TemplateView):
    template_name = 'payments/payment_detail.html'

class RefundListView(TemplateView):
    template_name = 'payments/refunds.html'

class RequestRefundView(TemplateView):
    template_name = 'payments/request_refund.html'

class SubscriptionListView(TemplateView):
    template_name = 'payments/subscriptions.html'

class CancelSubscriptionView(TemplateView):
    template_name = 'payments/cancel_subscription.html'

class UpdateSubscriptionView(TemplateView):
    template_name = 'payments/update_subscription.html'

class CalculateTotalAjaxView(TemplateView):
    template_name = 'payments/ajax_calculate_total.html'

class ValidateCouponAjaxView(TemplateView):
    template_name = 'payments/ajax_validate_coupon.html'
