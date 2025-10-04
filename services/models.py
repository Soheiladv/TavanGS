"""
Services App Models - Service Showcase System
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class ServiceCategory(models.Model):
    """Service categories"""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, default='blue')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Service Categories'
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
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Visual elements
    icon = models.CharField(max_length=50, blank=True)
    banner_image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    # Service details
    features = models.JSONField(default=list, blank=True)
    process_steps = models.JSONField(default=list, blank=True)
    deliverables = models.JSONField(default=list, blank=True)
    
    # Pricing
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_currency = models.CharField(max_length=3, default='IRR')
    price_unit = models.CharField(max_length=50, default='پروژه')
    
    # Timeline
    estimated_duration = models.CharField(max_length=100, blank=True)
    
    # Contact and leads
    inquiry_count = models.PositiveIntegerField(default=0)
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
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
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='inquiries')
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    
    # Contact information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    
    # Inquiry details
    subject = models.CharField(max_length=200)
    message = models.TextField()
    budget_range = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    
    # Project details (JSON for flexibility)
    project_details = models.JSONField(default=dict, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.PositiveIntegerField(default=3)  # 1-5, higher = more priority
    
    # Response tracking
    response_sent = models.BooleanField(default=False)
    response_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Service Inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"