from django.contrib import admin
from .models import VisitorSession, PageVisit, ServiceUsage, ChatConversation, SecurityAlert

@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'user', 'first_visit', 'last_activity', 'page_views', 'is_active', 'country', 'city']
    list_filter = ['is_active', 'first_visit', 'last_activity', 'country']
    search_fields = ['ip_address', 'user__username', 'user_agent', 'country', 'city']
    readonly_fields = ['first_visit', 'last_activity', 'session_key']
    date_hierarchy = 'first_visit'
    ordering = ['-last_activity']
    
    def get_queryset(self, request):
        # Optimize queries by selecting related user data
        return super().get_queryset(request).select_related('user')

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['session', 'page_url', 'page_title', 'visit_time']
    list_filter = ['visit_time']
    search_fields = ['session__ip_address', 'page_url', 'page_title']
    date_hierarchy = 'visit_time'

@admin.register(ServiceUsage)
class ServiceUsageAdmin(admin.ModelAdmin):
    list_display = ['session', 'service_type', 'usage_time', 'operation']
    list_filter = ['usage_time', 'service_type']
    search_fields = ['session__ip_address', 'service_type']
    date_hierarchy = 'usage_time'

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ['session', 'user_message', 'timestamp', 'response_time']
    list_filter = ['timestamp']
    search_fields = ['session__ip_address', 'user_message', 'ai_response']
    date_hierarchy = 'timestamp'

@admin.register(SecurityAlert)
class SecurityAlertAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'alert_type', 'severity', 'timestamp', 'description']
    list_filter = ['timestamp', 'alert_type', 'severity']
    search_fields = ['ip_address', 'alert_type', 'description']
    date_hierarchy = 'timestamp'
