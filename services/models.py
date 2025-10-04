"""
Services App Models - Service Showcase System
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class ServiceCategory(models.Model):
    """Service categories"""
    
    name = models.CharField(max_length=100, verbose_name="نام")
    slug = models.SlugField(unique=True, blank=True, verbose_name="نامک")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    icon = models.CharField(max_length=50, blank=True, verbose_name="آیکون")
    color = models.CharField(max_length=20, default='blue', verbose_name="رنگ")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = 'دسته‌بندی خدمت'
        verbose_name_plural = 'دسته‌بندی‌های خدمات'
        default_permissions = ()
        permissions = [
            ('ServiceCategory_view', 'می‌تواند دسته‌بندی خدمات را مشاهده کند'),
            ('ServiceCategory_add', 'می‌تواند دسته‌بندی خدمت جدید ایجاد کند'),
            ('ServiceCategory_change', 'می‌تواند دسته‌بندی خدمات را تغییر دهد'),
            ('ServiceCategory_delete', 'می‌تواند دسته‌بندی خدمات را حذف کند'),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Main service model"""
    
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('coming_soon', 'به‌زودی'),
        ('limited', 'محدود'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نام")
    slug = models.SlugField(unique=True, blank=True, verbose_name="نامک")
    tagline = models.CharField(max_length=200, blank=True, verbose_name="شعار")
    description = models.TextField(verbose_name="توضیحات")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="توضیحات کوتاه")
    
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="وضعیت")
    
    # Visual elements
    icon = models.CharField(max_length=50, blank=True, verbose_name="آیکون")
    banner_image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="تصویر بنر")
    
    # Service details
    features = models.JSONField(default=list, blank=True, verbose_name="ویژگی‌ها")
    process_steps = models.JSONField(default=list, blank=True, verbose_name="مراحل فرآیند")
    deliverables = models.JSONField(default=list, blank=True, verbose_name="تحویلی‌ها")
    
    # Pricing
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="قیمت شروع")
    price_currency = models.CharField(max_length=3, default='IRR', verbose_name="واحد پول")
    price_unit = models.CharField(max_length=50, default='پروژه', verbose_name="واحد قیمت")
    
    # Timeline
    estimated_duration = models.CharField(max_length=100, blank=True, verbose_name="مدت زمان تخمینی")
    
    # Contact and leads
    inquiry_count = models.PositiveIntegerField(default=0, verbose_name="تعداد درخواست‌ها")
    
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'
        ordering = ['-is_featured', '-created_at']
        default_permissions = ()
        permissions = [
            ('Service_view', 'می‌تواند خدمات را مشاهده کند'),
            ('Service_add', 'می‌تواند خدمت جدید ایجاد کند'),
            ('Service_change', 'می‌تواند خدمات را تغییر دهد'),
            ('Service_delete', 'می‌تواند خدمات را حذف کند'),
            ('Service_feature', 'می‌تواند خدمات را ویژه کند'),
            ('Service_publish', 'می‌تواند خدمات را منتشر کند'),
            ('Service_analytics', 'می‌تواند آمار خدمات را مشاهده کند'),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceInquiry(models.Model):
    """Service inquiry/consultation requests"""
    
    INQUIRY_TYPES = [
        ('consultation', 'مشاوره'),
        ('quote', 'درخواست قیمت'),
        ('general', 'سوال عمومی'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('contacted', 'تماس گرفته شده'),
        ('in_progress', 'در حال بررسی'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='inquiries', verbose_name="خدمت")
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general', verbose_name="نوع درخواست")
    
    # Contact information
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, verbose_name="تلفن")
    company = models.CharField(max_length=100, blank=True, verbose_name="شرکت")
    
    # Inquiry details
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    budget_range = models.CharField(max_length=100, blank=True, verbose_name="محدوده بودجه")
    timeline = models.CharField(max_length=100, blank=True, verbose_name="زمان‌بندی")
    
    # Project details (JSON for flexibility)
    project_details = models.JSONField(default=dict, blank=True, verbose_name="جزئیات پروژه")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="وضعیت")
    priority = models.PositiveIntegerField(default=3, verbose_name="اولویت")  # 1-5, higher = more priority
    
    # Response tracking
    response_sent = models.BooleanField(default=False, verbose_name="پاسخ ارسال شده")
    response_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ پاسخ")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = 'درخواست خدمت'
        verbose_name_plural = 'درخواست‌های خدمات'
        ordering = ['-created_at']
        default_permissions = ()
        permissions = [
            ('ServiceInquiry_view', 'می‌تواند درخواست‌های خدمات را مشاهده کند'),
            ('ServiceInquiry_add', 'می‌تواند درخواست خدمت جدید ایجاد کند'),
            ('ServiceInquiry_change', 'می‌تواند درخواست‌های خدمات را تغییر دهد'),
            ('ServiceInquiry_delete', 'می‌تواند درخواست‌های خدمات را حذف کند'),
            ('ServiceInquiry_respond', 'می‌تواند به درخواست‌های خدمات پاسخ دهد'),
            ('ServiceInquiry_assign', 'می‌تواند درخواست‌های خدمات را واگذار کند'),
            ('ServiceInquiry_analytics', 'می‌تواند آمار درخواست‌های خدمات را مشاهده کند'),
        ]
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"