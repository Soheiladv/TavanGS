"""
Sales App Admin - Product Versions, Downloads, and Lead Management
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    ProductVersion, DownloadSession, DemoRequest, 
    PricingRequest, SalesLead
)


@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = [
        'full_version_name', 'product', 'version_number', 'version_type',
        'status', 'release_date', 'download_count', 'trial_count',
        'is_free', 'price_display', 'is_featured', 'is_active'
    ]
    list_filter = [
        'version_type', 'status', 'is_free', 'is_featured', 
        'is_active', 'product__category', 'release_date'
    ]
    search_fields = ['version_number', 'product__name', 'changelog']
    list_editable = ['status', 'is_featured', 'is_active']
    readonly_fields = ['download_count', 'trial_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات نسخه', {
            'fields': ('product', 'version_number', 'version_type', 'status')
        }),
        ('جزئیات انتشار', {
            'fields': ('release_date', 'changelog', 'release_notes')
        }),
        ('مشخصات فنی', {
            'fields': ('system_requirements', 'file_size_mb', 'download_url')
        }),
        ('قیمت‌گذاری', {
            'fields': ('is_free', 'price', 'currency')
        }),
        ('نسخه آزمایشی', {
            'fields': ('has_trial', 'trial_days', 'trial_download_url')
        }),
        ('آمار', {
            'fields': ('download_count', 'trial_count'),
            'classes': ('collapse',)
        }),
        ('تنظیمات', {
            'fields': ('is_featured', 'is_active')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        if obj.is_free:
            return format_html('<span style="color: green;">رایگان</span>')
        elif obj.price:
            return f"{obj.price:,.0f} {obj.currency}"
        return '-'
    price_display.short_description = 'قیمت'
    
    def full_version_name(self, obj):
        return obj.full_version_name
    full_version_name.short_description = 'نام کامل نسخه'


@admin.register(DownloadSession)
class DownloadSessionAdmin(admin.ModelAdmin):
    list_display = [
        'session_id', 'user', 'product_version', 'download_type',
        'ip_address', 'is_completed', 'started_at', 'completed_at'
    ]
    list_filter = [
        'download_type', 'is_completed', 'started_at', 'product_version__product'
    ]
    search_fields = ['session_id', 'user__email', 'ip_address']
    readonly_fields = ['session_id', 'started_at', 'completed_at']
    
    fieldsets = (
        ('اطلاعات جلسه', {
            'fields': ('session_id', 'user', 'product_version', 'download_type')
        }),
        ('جزئیات دانلود', {
            'fields': ('ip_address', 'user_agent', 'is_completed')
        }),
        ('آمار عملکرد', {
            'fields': ('download_size_bytes', 'download_duration_seconds'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('started_at', 'completed_at')
        }),
    )


@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'company', 'product', 'status', 'preferred_date',
        'demo_type', 'assigned_to', 'created_at'
    ]
    list_filter = [
        'status', 'demo_type', 'assigned_to', 'product', 'created_at'
    ]
    search_fields = ['full_name', 'email', 'company', 'product__name']
    list_editable = ['status', 'assigned_to']
    readonly_fields = ['request_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات درخواست', {
            'fields': ('request_id', 'user', 'product', 'status')
        }),
        ('اطلاعات تماس', {
            'fields': ('full_name', 'email', 'phone', 'company', 'job_title')
        }),
        ('جزئیات دمو', {
            'fields': ('preferred_date', 'preferred_time', 'demo_type', 'special_requirements')
        }),
        ('مدیریت', {
            'fields': ('assigned_to', 'notes', 'scheduled_at')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_scheduled', 'mark_as_completed']
    
    def mark_as_scheduled(self, request, queryset):
        queryset.update(status='scheduled')
        self.message_user(request, f'{queryset.count()} درخواست دمو به حالت زمان‌بندی شده تغییر یافت.')
    mark_as_scheduled.short_description = 'زمان‌بندی شده'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f'{queryset.count()} درخواست دمو به حالت تکمیل شده تغییر یافت.')
    mark_as_completed.short_description = 'تکمیل شده'


@admin.register(PricingRequest)
class PricingRequestAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'company', 'product', 'status', 'user_count',
        'deployment_type', 'quoted_price', 'assigned_to', 'created_at'
    ]
    list_filter = [
        'status', 'deployment_type', 'assigned_to', 'product', 'created_at'
    ]
    search_fields = ['full_name', 'email', 'company', 'product__name']
    list_editable = ['status', 'assigned_to']
    readonly_fields = ['request_id', 'created_at', 'updated_at', 'responded_at']
    
    fieldsets = (
        ('اطلاعات درخواست', {
            'fields': ('request_id', 'user', 'product', 'status')
        }),
        ('اطلاعات تماس', {
            'fields': ('full_name', 'email', 'phone', 'company', 'job_title')
        }),
        ('نیازهای پروژه', {
            'fields': ('user_count', 'deployment_type', 'custom_requirements', 'budget_range', 'timeline')
        }),
        ('پاسخ', {
            'fields': ('quoted_price', 'currency', 'assigned_to', 'response_notes', 'responded_at')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_quoted', 'mark_as_accepted']
    
    def mark_as_quoted(self, request, queryset):
        queryset.update(status='quoted')
        self.message_user(request, f'{queryset.count()} درخواست قیمت به حالت قیمت‌گذاری شده تغییر یافت.')
    mark_as_quoted.short_description = 'قیمت‌گذاری شده'
    
    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
        self.message_user(request, f'{queryset.count()} درخواست قیمت به حالت پذیرفته شده تغییر یافت.')
    mark_as_accepted.short_description = 'پذیرفته شده'


@admin.register(SalesLead)
class SalesLeadAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'company', 'source', 'status', 'product_interest',
        'estimated_value', 'assigned_to', 'last_contact_date', 'created_at'
    ]
    list_filter = [
        'source', 'status', 'assigned_to', 'product_interest', 'created_at'
    ]
    search_fields = ['full_name', 'email', 'company', 'product_interest__name']
    list_editable = ['status', 'assigned_to']
    readonly_fields = ['lead_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات سرنخ', {
            'fields': ('lead_id', 'source', 'status')
        }),
        ('اطلاعات تماس', {
            'fields': ('full_name', 'email', 'phone', 'company', 'job_title')
        }),
        ('جزئیات پروژه', {
            'fields': ('product_interest', 'estimated_value', 'currency', 'notes')
        }),
        ('مدیریت', {
            'fields': ('assigned_to', 'last_contact_date', 'next_follow_up')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_contacted', 'mark_as_qualified', 'mark_as_closed_won']
    
    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
        self.message_user(request, f'{queryset.count()} سرنخ به حالت تماس گرفته شده تغییر یافت.')
    mark_as_contacted.short_description = 'تماس گرفته شده'
    
    def mark_as_qualified(self, request, queryset):
        queryset.update(status='qualified')
        self.message_user(request, f'{queryset.count()} سرنخ به حالت صلاحیت‌دار تغییر یافت.')
    mark_as_qualified.short_description = 'صلاحیت‌دار'
    
    def mark_as_closed_won(self, request, queryset):
        queryset.update(status='closed_won')
        self.message_user(request, f'{queryset.count()} سرنخ به حالت بسته شده - موفق تغییر یافت.')
    mark_as_closed_won.short_description = 'بسته شده - موفق'