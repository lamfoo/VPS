from django.shortcuts import render
from django.views.generic import TemplateView, ListView

class PackageListView(ListView):
    template_name = 'vps/packages.html'
    context_object_name = 'packages'
    
    def get_queryset(self):
        return []

class PackageDetailView(TemplateView):
    template_name = 'vps/package_detail.html'

class OrderPackageView(TemplateView):
    template_name = 'vps/order_package.html'

class VPSListView(TemplateView):
    template_name = 'vps/list.html'

class VPSDetailView(TemplateView):
    template_name = 'vps/detail.html'

class VPSConsoleView(TemplateView):
    template_name = 'vps/console.html'

class VPSStatsView(TemplateView):
    template_name = 'vps/stats.html'

class StartVPSView(TemplateView):
    template_name = 'vps/start.html'

class StopVPSView(TemplateView):
    template_name = 'vps/stop.html'

class RestartVPSView(TemplateView):
    template_name = 'vps/restart.html'

class RebuildVPSView(TemplateView):
    template_name = 'vps/rebuild.html'

class ResizeVPSView(TemplateView):
    template_name = 'vps/resize.html'

class DeleteVPSView(TemplateView):
    template_name = 'vps/delete.html'

class ResetPasswordView(TemplateView):
    template_name = 'vps/reset_password.html'

class ManageSSHKeysView(TemplateView):
    template_name = 'vps/ssh_keys.html'

class BackupListView(TemplateView):
    template_name = 'vps/backups.html'

class CreateBackupView(TemplateView):
    template_name = 'vps/create_backup.html'

class RestoreBackupView(TemplateView):
    template_name = 'vps/restore_backup.html'

class DeleteBackupView(TemplateView):
    template_name = 'vps/delete_backup.html'

class UsageStatsView(TemplateView):
    template_name = 'vps/usage_stats.html'

class ActionHistoryView(TemplateView):
    template_name = 'vps/action_history.html'

class VPSStatusAjaxView(TemplateView):
    template_name = 'vps/ajax_status.html'

class VPSStatsAjaxView(TemplateView):
    template_name = 'vps/ajax_stats.html'
