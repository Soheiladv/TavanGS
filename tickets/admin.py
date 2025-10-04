"""
Tickets App Admin - Support System Administration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.utils import timezone

from .models import Ticket, TicketCategory, TicketReply, TicketAttachment


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'icon', 'response_time_hours', 'resolution_time_hours',
        'auto_assign_to', 'ticket_count', 'is_active'
    ]
    list_filter = ['is_active', 'auto_assign_to']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'slug', 'description', 'icon', 'color')
        }),
        ('تنظیمات SLA', {
            'fields': ('response_time_hours', 'resolution_time_hours')
        }),
        ('انتساب خودکار', {
            'fields': ('auto_assign_to',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def ticket_count(self, obj):
        return obj.tickets.count()
    ticket_count.short_description = 'تعداد تیکت‌ها'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_id_short', 'title', 'user', 'category', 'status', 'priority',
        'assigned_to', 'created_at', 'is_overdue', 'sla_breached'
    ]
    list_filter = [
        'status', 'priority', 'category', 'assigned_to', 'created_at', 'sla_breached'
    ]
    search_fields = ['title', 'description', 'user__email', 'ticket_id']
    list_editable = ['status', 'priority', 'assigned_to']
    readonly_fields = [
        'ticket_id', 'created_at', 'updated_at', 'first_response_at',
        'resolved_at', 'closed_at', 'is_overdue', 'resolution_time_minutes'
    ]
    
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('ticket_id', 'title', 'description', 'category', 'user')
        }),
        ('وضعیت و اولویت', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('اطلاعات تماس', {
            'fields': ('contact_email', 'contact_phone'),
            'classes': ('collapse',)
        }),
        ('اطلاعات فنی', {
            'fields': ('user_agent', 'ip_address'),
            'classes': ('collapse',)
        }),
        ('فایل‌ها و برچسب‌ها', {
            'fields': ('attachments', 'tags'),
            'classes': ('collapse',)
        }),
        ('هوش مصنوعی', {
            'fields': ('ai_category_suggestion', 'ai_priority_suggestion', 'ai_sentiment_score'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at', 'first_response_at', 'resolved_at', 'closed_at')
        }),
        ('متریک‌ها', {
            'fields': ('sla_breached', 'customer_satisfaction', 'resolution_time_minutes', 'is_overdue')
        }),
    )
    
    actions = ['mark_as_in_progress', 'mark_as_resolved', 'assign_to_me']
    
    def ticket_id_short(self, obj):
        return f"#{str(obj.ticket_id)[:8]}"
    ticket_id_short.short_description = 'شناسه'
    
    def status_badge(self, obj):
        status_classes = {
            'open': 'bg-blue-100 text-blue-800',
            'in_progress': 'bg-yellow-100 text-yellow-800',
            'pending': 'bg-orange-100 text-orange-800',
            'resolved': 'bg-green-100 text-green-800',
            'closed': 'bg-gray-100 text-gray-800',
            'cancelled': 'bg-red-100 text-red-800',
        }
        css_class = status_classes.get(obj.status, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 text-xs font-medium rounded-full {}">{}</span>',
            css_class,
            obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'
    
    def priority_badge(self, obj):
        priority_classes = {
            1: 'bg-green-100 text-green-800',
            2: 'bg-blue-100 text-blue-800',
            3: 'bg-yellow-100 text-yellow-800',
            4: 'bg-orange-100 text-orange-800',
            5: 'bg-red-100 text-red-800',
        }
        css_class = priority_classes.get(obj.priority, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 text-xs font-medium rounded-full {}">{}</span>',
            css_class,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'اولویت'
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f'{queryset.count()} تیکت به حالت در حال بررسی تغییر یافت.')
    mark_as_in_progress.short_description = 'در حال بررسی'
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, f'{queryset.count()} تیکت به حالت حل شده تغییر یافت.')
    mark_as_resolved.short_description = 'حل شده'
    
    def assign_to_me(self, request, queryset):
        queryset.update(assigned_to=request.user)
        self.message_user(request, f'{queryset.count()} تیکت به شما واگذار شد.')
    assign_to_me.short_description = 'واگذاری به من'


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'reply_type', 'content', 'is_private', 'created_at']


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0
    readonly_fields = ['created_at', 'file_size_human']
    fields = ['filename', 'file', 'file_size_human', 'is_safe', 'created_at']


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = [
        'ticket', 'user', 'reply_type', 'content_preview', 'is_private', 'created_at'
    ]
    list_filter = ['reply_type', 'is_private', 'created_at']
    search_fields = ['content', 'ticket__title', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات پاسخ', {
            'fields': ('ticket', 'user', 'reply_type', 'content')
        }),
        ('تنظیمات', {
            'fields': ('is_private', 'attachments')
        }),
        ('هوش مصنوعی', {
            'fields': ('ai_sentiment', 'ai_suggestions'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'پیش‌نمایش محتوا'


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = [
        'filename', 'ticket', 'file_size_human', 'content_type', 'is_safe', 'uploaded_by', 'created_at'
    ]
    list_filter = ['content_type', 'is_safe', 'created_at']
    search_fields = ['filename', 'ticket__title', 'uploaded_by__email']
    readonly_fields = ['created_at', 'file_size_human']
    
    fieldsets = (
        ('اطلاعات فایل', {
            'fields': ('ticket', 'reply', 'file', 'filename', 'file_size', 'content_type')
        }),
        ('امنیت', {
            'fields': ('is_safe',)
        }),
        ('اطلاعات آپلود', {
            'fields': ('uploaded_by', 'created_at')
        }),
    )