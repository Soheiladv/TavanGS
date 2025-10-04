"""
Users App Admin - User Management Administration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'full_name', 'user_type', 'company_name', 'is_email_verified',
        'is_phone_verified', 'two_factor_enabled', 'is_active', 'created_at'
    ]
    list_filter = [
        'user_type', 'is_active', 'is_staff', 'is_superuser', 'is_email_verified',
        'is_phone_verified', 'two_factor_enabled', 'created_at'
    ]
    search_fields = ['email', 'first_name', 'last_name', 'company_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'api_key']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('email', 'password', 'first_name', 'last_name')
        }),
        ('اطلاعات شغلی', {
            'fields': ('company_name', 'job_title', 'phone_number', 'bio', 'avatar')
        }),
        ('نوع کاربر و دسترسی', {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('امنیت', {
            'fields': ('is_email_verified', 'is_phone_verified', 'two_factor_enabled')
        }),
        ('تنظیمات', {
            'fields': ('language', 'timezone', 'theme')
        }),
        ('اعلان‌ها', {
            'fields': ('email_notifications', 'sms_notifications', 'marketing_emails')
        }),
        ('API', {
            'fields': ('api_key', 'api_calls_count', 'api_rate_limit'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('اطلاعات پایه', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
        ('اطلاعات شغلی', {
            'fields': ('company_name', 'job_title', 'phone_number')
        }),
        ('دسترسی', {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    
    actions = ['activate_users', 'deactivate_users', 'verify_emails', 'verify_phones']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'نام کامل'
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} کاربر فعال شد.')
    activate_users.short_description = 'فعال کردن کاربران انتخاب شده'
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} کاربر غیرفعال شد.')
    deactivate_users.short_description = 'غیرفعال کردن کاربران انتخاب شده'
    
    def verify_emails(self, request, queryset):
        queryset.update(is_email_verified=True)
        self.message_user(request, f'{queryset.count()} ایمیل تایید شد.')
    verify_emails.short_description = 'تایید ایمیل کاربران انتخاب شده'
    
    def verify_phones(self, request, queryset):
        queryset.update(is_phone_verified=True)
        self.message_user(request, f'{queryset.count()} شماره تلفن تایید شد.')
    verify_phones.short_description = 'تایید شماره تلفن کاربران انتخاب شده'