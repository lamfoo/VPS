from django.urls import path
from . import views

app_name = 'vps'

urlpatterns = [
    # VPS Packages
    path('packages/', views.PackageListView.as_view(), name='packages'),
    path('packages/<int:pk>/', views.PackageDetailView.as_view(), name='package_detail'),
    path('packages/<int:pk>/order/', views.OrderPackageView.as_view(), name='order_package'),
    
    # VPS Instance Management
    path('', views.VPSListView.as_view(), name='list'),
    path('<uuid:instance_id>/', views.VPSDetailView.as_view(), name='detail'),
    path('<uuid:instance_id>/console/', views.VPSConsoleView.as_view(), name='console'),
    path('<uuid:instance_id>/stats/', views.VPSStatsView.as_view(), name='stats'),
    
    # VPS Actions
    path('<uuid:instance_id>/start/', views.StartVPSView.as_view(), name='start'),
    path('<uuid:instance_id>/stop/', views.StopVPSView.as_view(), name='stop'),
    path('<uuid:instance_id>/restart/', views.RestartVPSView.as_view(), name='restart'),
    path('<uuid:instance_id>/rebuild/', views.RebuildVPSView.as_view(), name='rebuild'),
    path('<uuid:instance_id>/resize/', views.ResizeVPSView.as_view(), name='resize'),
    path('<uuid:instance_id>/delete/', views.DeleteVPSView.as_view(), name='delete'),
    
    # Password and SSH Management
    path('<uuid:instance_id>/reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('<uuid:instance_id>/ssh-keys/', views.ManageSSHKeysView.as_view(), name='ssh_keys'),
    
    # Backup Management
    path('<uuid:instance_id>/backups/', views.BackupListView.as_view(), name='backups'),
    path('<uuid:instance_id>/backups/create/', views.CreateBackupView.as_view(), name='create_backup'),
    path('<uuid:instance_id>/backups/<int:backup_id>/restore/', views.RestoreBackupView.as_view(), name='restore_backup'),
    path('<uuid:instance_id>/backups/<int:backup_id>/delete/', views.DeleteBackupView.as_view(), name='delete_backup'),
    
    # Usage and Monitoring
    path('<uuid:instance_id>/usage/', views.UsageStatsView.as_view(), name='usage_stats'),
    path('<uuid:instance_id>/actions/', views.ActionHistoryView.as_view(), name='action_history'),
    
    # AJAX endpoints for dynamic updates
    path('ajax/status/<uuid:instance_id>/', views.VPSStatusAjaxView.as_view(), name='ajax_status'),
    path('ajax/stats/<uuid:instance_id>/', views.VPSStatsAjaxView.as_view(), name='ajax_stats'),
]