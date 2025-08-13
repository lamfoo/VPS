from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main Dashboard
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('overview/', views.OverviewView.as_view(), name='overview'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/mark-read/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('notifications/mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark_all_notifications_read'),
    
    # Support System
    path('support/', views.SupportTicketListView.as_view(), name='support'),
    path('support/create/', views.CreateSupportTicketView.as_view(), name='create_support_ticket'),
    path('support/<uuid:ticket_id>/', views.SupportTicketDetailView.as_view(), name='support_ticket_detail'),
    path('support/<uuid:ticket_id>/reply/', views.ReplyToTicketView.as_view(), name='reply_to_ticket'),
    path('support/<uuid:ticket_id>/close/', views.CloseTicketView.as_view(), name='close_ticket'),
    
    # Dashboard Widgets
    path('widgets/', views.DashboardWidgetView.as_view(), name='widgets'),
    path('widgets/update/', views.UpdateWidgetView.as_view(), name='update_widget'),
    path('widgets/<int:pk>/delete/', views.DeleteWidgetView.as_view(), name='delete_widget'),
    
    # System Status
    path('status/', views.SystemStatusView.as_view(), name='system_status'),
    
    # Admin Dashboard (for admin users only)
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/users/', views.AdminUserListView.as_view(), name='admin_users'),
    path('admin/users/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin/vps/', views.AdminVPSListView.as_view(), name='admin_vps'),
    path('admin/orders/', views.AdminOrderListView.as_view(), name='admin_orders'),
    path('admin/support/', views.AdminSupportView.as_view(), name='admin_support'),
    path('admin/support/<uuid:ticket_id>/assign/', views.AssignTicketView.as_view(), name='assign_ticket'),
    
    # Analytics and Reports
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('reports/export/', views.ExportReportView.as_view(), name='export_report'),
    
    # Maintenance Windows
    path('maintenance/', views.MaintenanceWindowListView.as_view(), name='maintenance'),
    path('maintenance/create/', views.CreateMaintenanceWindowView.as_view(), name='create_maintenance'),
    path('maintenance/<int:pk>/edit/', views.EditMaintenanceWindowView.as_view(), name='edit_maintenance'),
    
    # API Usage Logs
    path('api-logs/', views.APIUsageLogView.as_view(), name='api_logs'),
    
    # AJAX endpoints
    path('ajax/stats/', views.DashboardStatsAjaxView.as_view(), name='ajax_stats'),
    path('ajax/notifications/', views.NotificationsAjaxView.as_view(), name='ajax_notifications'),
    path('ajax/recent-activity/', views.RecentActivityAjaxView.as_view(), name='ajax_recent_activity'),
]