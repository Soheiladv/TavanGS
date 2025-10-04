"""
Sales App Models - Product Versions, Downloads, and Lead Generation
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from products.models import Product
import uuid

User = get_user_model()


class ProductVersion(models.Model):
    """
    Product version management for different software releases
    """
    
    VERSION_TYPES = [
        ('major', 'Major Release'),
        ('minor', 'Minor Update'),
        ('patch', 'Patch/Bug Fix'),
        ('beta', 'Beta Release'),
        ('alpha', 'Alpha Release'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deprecated', 'Deprecated'),
        ('coming_soon', 'Coming Soon'),
        ('beta', 'Beta Testing'),
    ]
    
    # Version identification
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=20, verbose_name="شماره نسخه")
    version_type = models.CharField(max_length=10, choices=VERSION_TYPES, default='minor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Version details
    release_date = models.DateTimeField(verbose_name="تاریخ انتشار")
    changelog = models.TextField(verbose_name="لیست تغییرات")
    release_notes = models.TextField(blank=True, verbose_name="یادداشت‌های انتشار")
    
    # Technical specifications
    system_requirements = models.JSONField(default=dict, blank=True)
    file_size_mb = models.PositiveIntegerField(null=True, blank=True)
    download_url = models.URLField(blank=True, verbose_name="لینک دانلود")
    
    # Pricing and availability
    is_free = models.BooleanField(default=False, verbose_name="رایگان")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='IRR')
    
    # Trial and demo
    has_trial = models.BooleanField(default=False, verbose_name="نسخه آزمایشی")
    trial_days = models.PositiveIntegerField(default=30, verbose_name="روزهای آزمایشی")
    trial_download_url = models.URLField(blank=True, verbose_name="لینک دانلود آزمایشی")
    
    # Statistics
    download_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دانلود")
    trial_count = models.PositiveIntegerField(default=0, verbose_name="تعداد آزمایش")
    
    # Metadata
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-release_date', '-version_number']
        unique_together = ['product', 'version_number']
        verbose_name = "نسخه محصول"
        verbose_name_plural = "نسخه‌های محصول"
    
    def __str__(self):
        return f"{self.product.full_name} v{self.version_number}"
    
    @property
    def full_version_name(self):
        """Return full version name with product prefix"""
        return f"{self.product.brand_prefix} {self.product.name} v{self.version_number}"
    
    @property
    def is_latest(self):
        """Check if this is the latest version"""
        latest = ProductVersion.objects.filter(
            product=self.product, 
            is_active=True
        ).order_by('-release_date').first()
        return self == latest


class DownloadSession(models.Model):
    """
    Track download sessions for analytics and security
    """
    
    DOWNLOAD_TYPES = [
        ('full', 'Full Download'),
        ('trial', 'Trial Download'),
        ('demo', 'Demo Download'),
    ]
    
    # Session identification
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    
    # Download details
    download_type = models.CharField(max_length=10, choices=DOWNLOAD_TYPES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Status tracking
    is_completed = models.BooleanField(default=False)
    download_size_bytes = models.BigIntegerField(null=True, blank=True)
    download_duration_seconds = models.FloatField(null=True, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = "جلسه دانلود"
        verbose_name_plural = "جلسات دانلود"


class DemoRequest(models.Model):
    """
    Demo request management for lead generation
    """
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('scheduled', 'زمان‌بندی شده'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]
    
    # Request identification
    request_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Contact information
    full_name = models.CharField(max_length=100, verbose_name="نام کامل")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن")
    company = models.CharField(max_length=100, blank=True, verbose_name="شرکت")
    job_title = models.CharField(max_length=100, blank=True, verbose_name="سمت")
    
    # Demo details
    preferred_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ ترجیحی")
    preferred_time = models.CharField(max_length=50, blank=True, verbose_name="زمان ترجیحی")
    demo_type = models.CharField(max_length=50, default='online', verbose_name="نوع دمو")
    special_requirements = models.TextField(blank=True, verbose_name="نیازهای خاص")
    
    # Status and follow-up
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_demos')
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "درخواست دمو"
        verbose_name_plural = "درخواست‌های دمو"
    
    def __str__(self):
        return f"Demo Request: {self.product.name} - {self.full_name}"


class PricingRequest(models.Model):
    """
    Custom pricing request management
    """
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('quoted', 'قیمت‌گذاری شده'),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده'),
    ]
    
    # Request identification
    request_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Contact information
    full_name = models.CharField(max_length=100, verbose_name="نام کامل")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن")
    company = models.CharField(max_length=100, verbose_name="شرکت")
    job_title = models.CharField(max_length=100, blank=True, verbose_name="سمت")
    
    # Requirements
    user_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="تعداد کاربر")
    deployment_type = models.CharField(max_length=50, default='cloud', verbose_name="نوع استقرار")
    custom_requirements = models.TextField(verbose_name="نیازهای سفارشی")
    budget_range = models.CharField(max_length=50, blank=True, verbose_name="محدوده بودجه")
    timeline = models.CharField(max_length=100, blank=True, verbose_name="زمان‌بندی")
    
    # Response
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='IRR')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_quotes')
    response_notes = models.TextField(blank=True, verbose_name="یادداشت‌های پاسخ")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "درخواست قیمت"
        verbose_name_plural = "درخواست‌های قیمت"
    
    def __str__(self):
        return f"Pricing Request: {self.product.name} - {self.company}"


class SalesLead(models.Model):
    """
    Unified lead management for all sales activities
    """
    
    LEAD_SOURCES = [
        ('website', 'وب‌سایت'),
        ('demo_request', 'درخواست دمو'),
        ('pricing_request', 'درخواست قیمت'),
        ('trial_download', 'دانلود آزمایشی'),
        ('contact_form', 'فرم تماس'),
        ('referral', 'معرفی'),
        ('social_media', 'شبکه‌های اجتماعی'),
    ]
    
    LEAD_STATUS = [
        ('new', 'جدید'),
        ('contacted', 'تماس گرفته شده'),
        ('qualified', 'صلاحیت‌دار'),
        ('proposal', 'پیشنهاد'),
        ('negotiation', 'مذاکره'),
        ('closed_won', 'بسته شده - موفق'),
        ('closed_lost', 'بسته شده - ناموفق'),
    ]
    
    # Lead identification
    lead_id = models.UUIDField(default=uuid.uuid4, unique=True)
    source = models.CharField(max_length=20, choices=LEAD_SOURCES)
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default='new')
    
    # Contact information
    full_name = models.CharField(max_length=100, verbose_name="نام کامل")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن")
    company = models.CharField(max_length=100, blank=True, verbose_name="شرکت")
    job_title = models.CharField(max_length=100, blank=True, verbose_name="سمت")
    
    # Lead details
    product_interest = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='IRR')
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")
    
    # Assignment and follow-up
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')
    last_contact_date = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "سرنخ فروش"
        verbose_name_plural = "سرنخ‌های فروش"
    
    def __str__(self):
        return f"Lead: {self.full_name} - {self.company}"