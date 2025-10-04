"""
Computation Engine Admin - Computation Management Administration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import ComputationSession, ComputationTemplate, ComputationResult, ComputationMetrics


@admin.register(ComputationSession)
class ComputationSessionAdmin(admin.ModelAdmin):
    list_display = [
        'session_id_short', 'user', 'session_type', 'status_badge', 'progress_bar',
        'processing_time', 'created_at', 'priority'
    ]
    list_filter = [
        'session_type', 'status', 'priority', 'created_at', 'user'
    ]
    search_fields = ['session_id', 'user__email', 'product_name']
    readonly_fields = [
        'session_id', 'created_at', 'started_at', 'completed_at', 'processing_time_seconds',
        'memory_usage_mb', 'cpu_usage_percent', 'duration'
    ]
    
    fieldsets = (
        ('اطلاعات جلسه', {
            'fields': ('session_id', 'user', 'session_type', 'product_name')
        }),
        ('وضعیت و پیشرفت', {
            'fields': ('status', 'progress_percentage', 'priority')
        }),
        ('داده‌های ورودی و خروجی', {
            'fields': ('input_data', 'output_data'),
            'classes': ('collapse',)
        }),
        ('متریک‌های عملکرد', {
            'fields': ('processing_time_seconds', 'memory_usage_mb', 'cpu_usage_percent'),
            'classes': ('collapse',)
        }),
        ('مدیریت خطا', {
            'fields': ('error_message', 'error_code'),
            'classes': ('collapse',)
        }),
        ('تنظیمات', {
            'fields': ('configuration',),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'started_at', 'completed_at')
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_failed', 'cancel_sessions']
    
    def session_id_short(self, obj):
        return f"#{str(obj.session_id)[:8]}"
    session_id_short.short_description = 'شناسه جلسه'
    
    def status_badge(self, obj):
        status_classes = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'processing': 'bg-blue-100 text-blue-800',
            'completed': 'bg-green-100 text-green-800',
            'failed': 'bg-red-100 text-red-800',
            'cancelled': 'bg-gray-100 text-gray-800',
        }
        css_class = status_classes.get(obj.status, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 text-xs font-medium rounded-full {}">{}</span>',
            css_class,
            obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'
    
    def progress_bar(self, obj):
        if obj.status == 'completed':
            color = 'bg-green-500'
            width = '100%'
        elif obj.status == 'failed':
            color = 'bg-red-500'
            width = '100%'
        else:
            color = 'bg-blue-500'
            width = f'{obj.progress_percentage}%'
        
        return format_html(
            '<div class="w-full bg-gray-200 rounded-full h-2">'
            '<div class="{} h-2 rounded-full" style="width: {}"></div>'
            '</div>',
            color,
            width
        )
    progress_bar.short_description = 'پیشرفت'
    
    def processing_time(self, obj):
        if obj.processing_time_seconds:
            return f"{obj.processing_time_seconds:.2f}s"
        return "-"
    processing_time.short_description = 'زمان پردازش'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed', progress_percentage=100)
        self.message_user(request, f'{queryset.count()} جلسه به حالت تکمیل شده تغییر یافت.')
    mark_as_completed.short_description = 'تکمیل شده'
    
    def mark_as_failed(self, request, queryset):
        queryset.update(status='failed')
        self.message_user(request, f'{queryset.count()} جلسه به حالت ناموفق تغییر یافت.')
    mark_as_failed.short_description = 'ناموفق'
    
    def cancel_sessions(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'{queryset.count()} جلسه لغو شد.')
    cancel_sessions.short_description = 'لغو'


@admin.register(ComputationTemplate)
class ComputationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'session_type', 'required_user_type', 'estimated_time',
        'memory_requirement', 'usage_count', 'success_rate', 'is_active'
    ]
    list_filter = [
        'session_type', 'required_user_type', 'cpu_intensive', 'is_active', 'created_at'
    ]
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['usage_count', 'success_rate', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'description', 'session_type')
        }),
        ('پیکربندی', {
            'fields': ('input_schema', 'output_schema', 'default_config')
        }),
        ('نیازهای پردازش', {
            'fields': ('estimated_time_seconds', 'memory_requirement_mb', 'cpu_intensive')
        }),
        ('کنترل دسترسی', {
            'fields': ('required_user_type',)
        }),
        ('آمار استفاده', {
            'fields': ('usage_count', 'success_rate'),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_templates', 'deactivate_templates', 'reset_usage_stats']
    
    def estimated_time(self, obj):
        return f"{obj.estimated_time_seconds}s"
    estimated_time.short_description = 'زمان تخمینی'
    
    def memory_requirement(self, obj):
        return f"{obj.memory_requirement_mb}MB"
    memory_requirement.short_description = 'حافظه مورد نیاز'
    
    def activate_templates(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} قالب فعال شد.')
    activate_templates.short_description = 'فعال کردن قالب‌ها'
    
    def deactivate_templates(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} قالب غیرفعال شد.')
    deactivate_templates.short_description = 'غیرفعال کردن قالب‌ها'
    
    def reset_usage_stats(self, request, queryset):
        queryset.update(usage_count=0, success_rate=100.0)
        self.message_user(request, f'آمار استفاده {queryset.count()} قالب بازنشانی شد.')
    reset_usage_stats.short_description = 'بازنشانی آمار استفاده'


@admin.register(ComputationResult)
class ComputationResultAdmin(admin.ModelAdmin):
    list_display = [
        'input_hash_short', 'session_type', 'computation_time', 'access_count',
        'is_valid', 'expires_at', 'created_at'
    ]
    list_filter = [
        'session_type', 'is_valid', 'created_at', 'expires_at'
    ]
    search_fields = ['input_hash', 'session_type']
    readonly_fields = [
        'input_hash', 'created_at', 'last_accessed', 'access_count'
    ]
    
    fieldsets = (
        ('شناسه کش', {
            'fields': ('input_hash', 'session_type')
        }),
        ('داده‌های کش شده', {
            'fields': ('input_data', 'output_data', 'configuration'),
            'classes': ('collapse',)
        }),
        ('متریک‌ها', {
            'fields': ('computation_time', 'access_count', 'created_at', 'last_accessed')
        }),
        ('مدیریت کش', {
            'fields': ('expires_at', 'is_valid')
        }),
    )
    
    actions = ['invalidate_cache', 'extend_expiration']
    
    def input_hash_short(self, obj):
        return f"#{obj.input_hash[:8]}"
    input_hash_short.short_description = 'شناسه کش'
    
    def invalidate_cache(self, request, queryset):
        queryset.update(is_valid=False)
        self.message_user(request, f'{queryset.count()} کش نامعتبر شد.')
    invalidate_cache.short_description = 'نامعتبر کردن کش'
    
    def extend_expiration(self, request, queryset):
        from django.utils import timezone
        new_expiration = timezone.now() + timezone.timedelta(days=7)
        queryset.update(expires_at=new_expiration)
        self.message_user(request, f'تاریخ انقضای {queryset.count()} کش تمدید شد.')
    extend_expiration.short_description = 'تمدید تاریخ انقضای کش'


@admin.register(ComputationMetrics)
class ComputationMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_sessions', 'success_rate', 'average_processing_time',
        'cache_hit_rate', 'unique_users'
    ]
    list_filter = ['date', 'created_at']
    search_fields = ['date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('دوره زمانی', {
            'fields': ('date',)
        }),
        ('آمار جلسات', {
            'fields': ('total_sessions', 'completed_sessions', 'failed_sessions', 'cancelled_sessions')
        }),
        ('متریک‌های عملکرد', {
            'fields': ('average_processing_time', 'peak_processing_time', 'average_memory_usage', 'peak_memory_usage')
        }),
        ('آمار کش', {
            'fields': ('cache_hit_rate', 'cache_miss_count')
        }),
        ('آمار کاربران', {
            'fields': ('unique_users', 'free_user_sessions', 'premium_user_sessions')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def success_rate(self, obj):
        return f"{obj.success_rate:.1f}%"
    success_rate.short_description = 'نرخ موفقیت'
    
    def average_processing_time(self, obj):
        return f"{obj.average_processing_time:.2f}s"
    average_processing_time.short_description = 'زمان متوسط پردازش'
    
    def cache_hit_rate(self, obj):
        return f"{obj.cache_hit_rate:.1f}%"
    cache_hit_rate.short_description = 'نرخ ضربه کش'