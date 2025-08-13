from django.shortcuts import render
from django.views.generic import TemplateView

class DashboardHomeView(TemplateView):
    template_name = 'dashboard/home.html'

class OverviewView(TemplateView):
    template_name = 'dashboard/overview.html'

class NotificationListView(TemplateView):
    template_name = 'dashboard/notifications.html'

class MarkNotificationReadView(TemplateView):
    template_name = 'dashboard/mark_notification_read.html'

class MarkAllNotificationsReadView(TemplateView):
    template_name = 'dashboard/mark_all_notifications_read.html'

class SupportTicketListView(TemplateView):
    template_name = 'dashboard/support.html'

class CreateSupportTicketView(TemplateView):
    template_name = 'dashboard/create_support_ticket.html'

class SupportTicketDetailView(TemplateView):
    template_name = 'dashboard/support_ticket_detail.html'

class ReplyToTicketView(TemplateView):
    template_name = 'dashboard/reply_to_ticket.html'

class CloseTicketView(TemplateView):
    template_name = 'dashboard/close_ticket.html'

class DashboardWidgetView(TemplateView):
    template_name = 'dashboard/widgets.html'

class UpdateWidgetView(TemplateView):
    template_name = 'dashboard/update_widget.html'

class DeleteWidgetView(TemplateView):
    template_name = 'dashboard/delete_widget.html'

class SystemStatusView(TemplateView):
    template_name = 'dashboard/system_status.html'

class AdminDashboardView(TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

class AdminUserListView(TemplateView):
    template_name = 'dashboard/admin_users.html'

class AdminUserDetailView(TemplateView):
    template_name = 'dashboard/admin_user_detail.html'

class AdminVPSListView(TemplateView):
    template_name = 'dashboard/admin_vps.html'

class AdminOrderListView(TemplateView):
    template_name = 'dashboard/admin_orders.html'

class AdminSupportView(TemplateView):
    template_name = 'dashboard/admin_support.html'

class AssignTicketView(TemplateView):
    template_name = 'dashboard/assign_ticket.html'

class AnalyticsView(TemplateView):
    template_name = 'dashboard/analytics.html'

class ReportsView(TemplateView):
    template_name = 'dashboard/reports.html'

class ExportReportView(TemplateView):
    template_name = 'dashboard/export_report.html'

class MaintenanceWindowListView(TemplateView):
    template_name = 'dashboard/maintenance.html'

class CreateMaintenanceWindowView(TemplateView):
    template_name = 'dashboard/create_maintenance.html'

class EditMaintenanceWindowView(TemplateView):
    template_name = 'dashboard/edit_maintenance.html'

class APIUsageLogView(TemplateView):
    template_name = 'dashboard/api_logs.html'

class DashboardStatsAjaxView(TemplateView):
    template_name = 'dashboard/ajax_stats.html'

class NotificationsAjaxView(TemplateView):
    template_name = 'dashboard/ajax_notifications.html'

class RecentActivityAjaxView(TemplateView):
    template_name = 'dashboard/ajax_recent_activity.html'
