"""
Products App Models - Expansive Product Catalog System
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()


class ProductCategory(models.Model):
    """Product categories for organization"""
    
    name = models.CharField(
        max_length=100,
        verbose_name="نام دسته‌بندی",
        help_text="نام دسته‌بندی محصولات"
    )
    slug = models.SlugField(
        unique=True, 
        blank=True,
        verbose_name="نامک URL",
        help_text="نامک برای استفاده در آدرس (خودکار تولید می‌شود)"
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
        help_text="نام آیکون FontAwesome (مثال: brain, shield)"
    )
    color = models.CharField(
        max_length=20, 
        default='blue',
        verbose_name="رنگ",
        help_text="رنگ دسته‌بندی برای نمایش"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
        help_text="آیا این دسته‌بندی فعال باشد؟"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'دسته‌بندی محصول'
        verbose_name_plural = 'دسته‌بندی‌های محصولات'
        default_permissions = ()
        permissions = [
            ('ProductCategory_view', 'می‌تواند دسته‌بندی محصولات را مشاهده کند'),
            ('ProductCategory_add', 'می‌تواند دسته‌بندی محصول جدید ایجاد کند'),
            ('ProductCategory_change', 'می‌تواند دسته‌بندی محصولات را تغییر دهد'),
            ('ProductCategory_delete', 'می‌تواند دسته‌بندی محصولات را حذف کند'),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Main product model for TakoTech software suite"""
    
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('beta', 'بتا'),
        ('coming_soon', 'به‌زودی'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=100,
        verbose_name="نام محصول",
        help_text="نام محصول (مثال: BudgetPro، SecureAI)"
    )
    slug = models.SlugField(
        unique=True, 
        blank=True,
        verbose_name="نامک URL",
        help_text="نامک برای استفاده در آدرس (خودکار تولید می‌شود)"
    )
    brand_prefix = models.CharField(
        max_length=20, 
        default='TakoTech',
        verbose_name="پیشوند برند",
        help_text="پیشوند نام برند (مثال: TakoTech)"
    )
    tagline = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="شعار محصول",
        help_text="شعار کوتاه و جذاب برای محصول"
    )
    description = models.TextField(
        verbose_name="توضیحات کامل",
        help_text="توضیحات کامل و جامع محصول"
    )
    short_description = models.CharField(
        max_length=300, 
        blank=True,
        verbose_name="توضیحات کوتاه",
        help_text="توضیحات کوتاه برای نمایش در فهرست‌ها"
    )
    
    # Classification
    category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.CASCADE,
        verbose_name="دسته‌بندی",
        help_text="دسته‌بندی محصول"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="وضعیت",
        help_text="وضعیت فعلی محصول"
    )
    
    # Visual Elements
    logo = models.ImageField(
        upload_to='products/logos/', 
        blank=True, 
        null=True,
        verbose_name="لوگو محصول",
        help_text="تصویر لوگو محصول (PNG یا JPG)"
    )
    banner_image = models.ImageField(
        upload_to='products/banners/', 
        blank=True, 
        null=True,
        verbose_name="تصویر بنر",
        help_text="تصویر بنر اصلی محصول"
    )
    
    # Features and specs (JSON for flexibility)
    features = models.JSONField(
        default=list, 
        blank=True,
        verbose_name="ویژگی‌ها",
        help_text="لیست ویژگی‌های محصول (JSON)"
    )
    technical_specs = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name="مشخصات فنی",
        help_text="مشخصات فنی محصول (JSON)"
    )
    
    # Pricing
    has_free_version = models.BooleanField(
        default=False,
        verbose_name="نسخه رایگان",
        help_text="آیا این محصول نسخه رایگان دارد؟"
    )
    has_trial = models.BooleanField(
        default=True,
        verbose_name="نسخه آزمایشی",
        help_text="آیا این محصول نسخه آزمایشی دارد؟"
    )
    trial_days = models.PositiveIntegerField(
        default=14,
        verbose_name="مدت آزمایشی (روز)",
        help_text="تعداد روزهای آزمایش رایگان"
    )
    
    # Analytics
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد بازدید",
        help_text="تعداد بازدیدهای محصول"
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد دانلود",
        help_text="تعداد دانلودهای محصول"
    )
    
    # Admin
    is_featured = models.BooleanField(
        default=False,
        verbose_name="محصول ویژه",
        help_text="آیا این محصول در بخش ویژه نمایش داده شود؟"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
        help_text="آیا این محصول فعال باشد؟"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="تاریخ بروزرسانی"
    )
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-is_featured', '-created_at']
        default_permissions = ()
        permissions = [
            ('Product_view', 'می‌تواند محصولات را مشاهده کند'),
            ('Product_add', 'می‌تواند محصول جدید ایجاد کند'),
            ('Product_change', 'می‌تواند محصولات را تغییر دهد'),
            ('Product_delete', 'می‌تواند محصولات را حذف کند'),
            ('Product_feature', 'می‌تواند محصولات را ویژه کند'),
            ('Product_publish', 'می‌تواند محصولات را منتشر کند'),
            ('Product_analytics', 'می‌تواند آمار محصولات را مشاهده کند'),
        ]
    
    def __str__(self):
        return f"{self.brand_prefix} {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand_prefix}-{self.name}")
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.brand_prefix} {self.name}"
    
    def increment_view_count(self):
        """افزایش تعداد بازدید محصول"""
        from django.db import models
        Product.objects.filter(pk=self.pk).update(
            view_count=models.F('view_count') + 1
        )
