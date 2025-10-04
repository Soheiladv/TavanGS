"""
Tickets App Models - Advanced Support System
سیستم پیشرفته پشتیبانی با قابلیت‌های هوش مصنوعی
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()


class TicketCategory(models.Model):
    """
    دسته‌بندی تیکت‌ها
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name="نام دسته‌بندی",
        help_text="نام دسته‌بندی تیکت‌ها"
    )
    
    slug = models.SlugField(
        unique=True, 
        blank=True,
        verbose_name="نامک URL",
        help_text="نامک برای استفاده در آدرس"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
        help_text="توضیحات کامل درباره دسته‌بندی"
    )
    
    icon = models.CharField(
        max_length=50, 
        blank=True,
        verbose_name="آیکون",
        help_text="نام آیکون FontAwesome"
    )
    
    color = models.CharField(
        max_length=20, 
        default='blue',
        verbose_name="رنگ",
        help_text="رنگ دسته‌بندی برای نمایش"
    )
    
    # SLA Settings
    response_time_hours = models.PositiveIntegerField(
        default=24,
        verbose_name="زمان پاسخ (ساعت)",
        help_text="حداکثر زمان پاسخ به ساعت"
    )
    
    resolution_time_hours = models.PositiveIntegerField(
        default=72,
        verbose_name="زمان حل مسئله (ساعت)",
        help_text="حداکثر زمان حل مسئله به ساعت"
    )
    
    # Auto-assignment
    auto_assign_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="انتساب خودکار به",
        help_text="کاربری که تیکت‌های این دسته به او واگذار شود",
        related_name='auto_assigned_categories'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
        help_text="آیا این دسته‌بندی فعال باشد؟"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "دسته‌بندی تیکت"
        verbose_name_plural = "دسته‌بندی‌های تیکت"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Ticket(models.Model):
    """
    مدل اصلی تیکت پشتیبانی
    """
    
    PRIORITY_CHOICES = [
        (1, 'کم'),
        (2, 'متوسط'),
        (3, 'بالا'),
        (4, 'فوری'),
        (5, 'بحرانی'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('in_progress', 'در حال بررسی'),
        ('pending', 'در انتظار پاسخ مشتری'),
        ('resolved', 'حل شده'),
        ('closed', 'بسته'),
        ('cancelled', 'لغو شده'),
    ]
    
    # شناسه منحصر به فرد
    ticket_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name="شناسه تیکت",
        help_text="شناسه منحصر به فرد تیکت"
    )
    
    # اطلاعات پایه
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان تیکت",
        help_text="عنوان کوتاه و مفید برای تیکت"
    )
    
    description = models.TextField(
        verbose_name="شرح مسئله",
        help_text="شرح کامل مسئله یا درخواست"
    )
    
    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.CASCADE,
        verbose_name="دسته‌بندی",
        help_text="دسته‌بندی تیکت",
        related_name='tickets'
    )
    
    # کاربر و انتساب
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر",
        help_text="کاربری که تیکت را ایجاد کرده",
        related_name='created_tickets'
    )
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="واگذار شده به",
        help_text="کارشناسی که تیکت به او واگذار شده",
        related_name='assigned_tickets'
    )
    
    # وضعیت و اولویت
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name="وضعیت",
        help_text="وضعیت فعلی تیکت"
    )
    
    priority = models.PositiveIntegerField(
        choices=PRIORITY_CHOICES,
        default=2,
        verbose_name="اولویت",
        help_text="اولویت تیکت"
    )
    
    # اطلاعات تماس
    contact_email = models.EmailField(
        blank=True,
        verbose_name="ایمیل تماس",
        help_text="ایمیل جایگزین برای پاسخ"
    )
    
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="تلفن تماس",
        help_text="شماره تلفن برای تماس فوری"
    )
    
    # اطلاعات فنی
    user_agent = models.TextField(
        blank=True,
        verbose_name="اطلاعات مرورگر",
        help_text="اطلاعات فنی مرورگر کاربر"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="آدرس IP",
        help_text="آدرس IP کاربر"
    )
    
    # فایل‌های پیوست
    attachments = models.JSONField(
        default=list,
        blank=True,
        verbose_name="فایل‌های پیوست",
        help_text="لیست فایل‌های پیوست شده"
    )
    
    # تگ‌ها و برچسب‌ها
    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name="برچسب‌ها",
        help_text="برچسب‌هایی برای دسته‌بندی بهتر"
    )
    
    # هوش مصنوعی
    ai_category_suggestion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="پیشنهاد دسته‌بندی AI",
        help_text="دسته‌بندی پیشنهادی توسط هوش مصنوعی"
    )
    
    ai_priority_suggestion = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="پیشنهاد اولویت AI",
        help_text="اولویت پیشنهادی توسط هوش مصنوعی"
    )
    
    ai_sentiment_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name="امتیاز احساسات AI",
        help_text="امتیاز احساسات متن (منفی تا مثبت)"
    )
    
    # زمان‌بندی
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    first_response_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان اولین پاسخ")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان حل مسئله")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="زمان بستن")
    
    # SLA و متریک‌ها
    sla_breached = models.BooleanField(
        default=False,
        verbose_name="نقض SLA",
        help_text="آیا SLA نقض شده است؟"
    )
    
    customer_satisfaction = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="رضایت مشتری",
        help_text="امتیاز رضایت مشتری (1-5)"
    )
    
    resolution_time_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="زمان حل (دقیقه)",
        help_text="زمان صرف شده برای حل مسئله"
    )
    
    class Meta:
        verbose_name = "تیکت پشتیبانی"
        verbose_name_plural = "تیکت‌های پشتیبانی"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"#{str(self.ticket_id)[:8]} - {self.title}"
    
    @property
    def is_overdue(self):
        """بررسی آیا تیکت از زمان تعیین شده عقب افتاده"""
        if self.status in ['resolved', 'closed', 'cancelled']:
            return False
        
        from django.utils import timezone
        now = timezone.now()
        
        # بررسی زمان پاسخ
        if not self.first_response_at:
            response_deadline = self.created_at + timezone.timedelta(
                hours=self.category.response_time_hours
            )
            if now > response_deadline:
                return True
        
        # بررسی زمان حل مسئله
        resolution_deadline = self.created_at + timezone.timedelta(
            hours=self.category.resolution_time_hours
        )
        return now > resolution_deadline
    
    def get_priority_display_class(self):
        """کلاس CSS برای نمایش اولویت"""
        priority_classes = {
            1: 'text-green-600',
            2: 'text-blue-600',
            3: 'text-yellow-600',
            4: 'text-orange-600',
            5: 'text-red-600',
        }
        return priority_classes.get(self.priority, 'text-gray-600')
    
    def get_status_display_class(self):
        """کلاس CSS برای نمایش وضعیت"""
        status_classes = {
            'open': 'bg-blue-100 text-blue-800',
            'in_progress': 'bg-yellow-100 text-yellow-800',
            'pending': 'bg-orange-100 text-orange-800',
            'resolved': 'bg-green-100 text-green-800',
            'closed': 'bg-gray-100 text-gray-800',
            'cancelled': 'bg-red-100 text-red-800',
        }
        return status_classes.get(self.status, 'bg-gray-100 text-gray-800')


class TicketReply(models.Model):
    """
    پاسخ‌های تیکت
    """
    
    REPLY_TYPES = [
        ('customer', 'مشتری'),
        ('staff', 'کارشناس'),
        ('system', 'سیستم'),
        ('ai', 'هوش مصنوعی'),
    ]
    
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name="تیکت",
        related_name='replies'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر",
        help_text="کاربری که پاسخ را ارسال کرده"
    )
    
    reply_type = models.CharField(
        max_length=20,
        choices=REPLY_TYPES,
        default='customer',
        verbose_name="نوع پاسخ",
        help_text="نوع پاسخ‌دهنده"
    )
    
    content = models.TextField(
        verbose_name="متن پاسخ",
        help_text="متن پاسخ"
    )
    
    attachments = models.JSONField(
        default=list,
        blank=True,
        verbose_name="فایل‌های پیوست",
        help_text="فایل‌های پیوست شده به پاسخ"
    )
    
    is_private = models.BooleanField(
        default=False,
        verbose_name="خصوصی",
        help_text="آیا این پاسخ فقط برای کارشناسان قابل مشاهده باشد؟"
    )
    
    # AI Analysis
    ai_sentiment = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="احساسات AI",
        help_text="تحلیل احساسات توسط AI"
    )
    
    ai_suggestions = models.JSONField(
        default=list,
        blank=True,
        verbose_name="پیشنهادات AI",
        help_text="پیشنهادات هوش مصنوعی"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "پاسخ تیکت"
        verbose_name_plural = "پاسخ‌های تیکت"
        ordering = ['created_at']
    
    def __str__(self):
        return f"پاسخ {self.ticket.title} - {self.user.get_full_name()}"


class TicketAttachment(models.Model):
    """
    فایل‌های پیوست تیکت
    """
    
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name="تیکت",
        related_name='ticket_attachments'
    )
    
    reply = models.ForeignKey(
        TicketReply,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="پاسخ",
        related_name='reply_attachments'
    )
    
    file = models.FileField(
        upload_to='tickets/attachments/',
        verbose_name="فایل",
        help_text="فایل پیوست"
    )
    
    filename = models.CharField(
        max_length=255,
        verbose_name="نام فایل",
        help_text="نام اصلی فایل"
    )
    
    file_size = models.PositiveIntegerField(
        verbose_name="اندازه فایل",
        help_text="اندازه فایل به بایت"
    )
    
    content_type = models.CharField(
        max_length=100,
        verbose_name="نوع فایل",
        help_text="نوع MIME فایل"
    )
    
    is_safe = models.BooleanField(
        default=True,
        verbose_name="امن",
        help_text="آیا فایل امنیت بررسی شده است؟"
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="آپلود شده توسط"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")
    
    class Meta:
        verbose_name = "فایل پیوست"
        verbose_name_plural = "فایل‌های پیوست"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.filename
    
    @property
    def file_size_human(self):
        """نمایش اندازه فایل به صورت خوانا"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"