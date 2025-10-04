"""
Settings App Models - Central Configuration System
Singleton pattern for site-wide settings management
"""

from django.db import models
from django.core.validators import URLValidator, RegexValidator
from django.core.exceptions import ValidationError
import json
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SingletonModel(models.Model):
    """Abstract base class for singleton models"""
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    """
    Central site settings model - Singleton pattern
    Independent configuration management for all apps
    """
    
    # Company Information
    company_name = models.CharField(
        max_length=100, 
        default="TakoTech",
        verbose_name="نام شرکت",
        help_text="نام شرکت که در سرتیتر سایت نمایش داده می‌شود"
    )
    company_tagline = models.CharField(
        max_length=200, 
        default="پیشرو در فناوری و نوآوری",
        verbose_name="شعار شرکت",
        help_text="شعار کوتاه شرکت"
    )
    company_description = models.TextField(
        default="شرکت تک یا فناوری، ارائه‌دهنده راهکارهای هوشمند فناوری اطلاعات",
        verbose_name="توضیحات شرکت",
        help_text="توضیحات کامل درباره شرکت"
    )
    
    # Contact Information
    contact_email = models.EmailField(
        default="info@takotech.com",
        verbose_name="ایمیل تماس",
        help_text="آدرس ایمیل اصلی شرکت"
    )
    contact_phone = models.CharField(
        max_length=20, 
        default="+98-21-12345678",
        verbose_name="تلفن تماس",
        help_text="شماره تلفن اصلی شرکت"
    )
    company_address = models.TextField(
        default="تهران، ایران",
        verbose_name="آدرس شرکت",
        help_text="آدرس کامل شرکت"
    )
    
    # Social Media Links
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    
    # SEO Settings
    site_title = models.CharField(max_length=100, default="TakoTech - راهکارهای هوشمند فناوری")
    meta_description = models.TextField(
        max_length=160, 
        default="شرکت تک یا فناوری، ارائه‌دهنده نرم‌افزارهای کاربردی، خدمات IT و راهکارهای هوش مصنوعی"
    )
    meta_keywords = models.TextField(default="فناوری,نرم‌افزار,هوش مصنوعی,امنیت سایبری,توسعه نرم‌افزار")
    
    # Theme and UI Settings
    primary_color = models.CharField(
        max_length=7, 
        default="#2563eb",
        verbose_name="رنگ اصلی",
        help_text="رنگ اصلی سایت (هگز کد)",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'کد هگز معتبر وارد کنید')]
    )
    secondary_color = models.CharField(
        max_length=7, 
        default="#7c3aed",
        verbose_name="رنگ فرعی",
        help_text="رنگ فرعی سایت (هگز کد)",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'کد هگز معتبر وارد کنید')]
    )
    accent_color = models.CharField(
        max_length=7, 
        default="#f59e0b",
        verbose_name="رنگ تاکیدی",
        help_text="رنگ تاکیدی سایت (هگز کد)",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'کد هگز معتبر وارد کنید')]
    )
    
    # Template and Layout Settings
    template_theme = models.CharField(
        max_length=50,
        default="modern",
        verbose_name="قالب سایت",
        help_text="نام قالب انتخابی برای سایت",
        choices=[
            ('modern', 'مدرن'),
            ('classic', 'کلاسیک'),
            ('minimal', 'مینیمال'),
            ('corporate', 'شرکتی'),
            ('creative', 'خلاقانه'),
        ]
    )
    
    layout_direction = models.CharField(
        max_length=3,
        default="rtl",
        verbose_name="جهت چیدمان",
        help_text="جهت چیدمان عناصر سایت",
        choices=[
            ('rtl', 'راست به چپ'),
            ('ltr', 'چپ به راست'),
        ]
    )
    
    font_family = models.CharField(
        max_length=100,
        default="Vazir, Tahoma, sans-serif",
        verbose_name="فونت اصلی",
        help_text="فونت اصلی سایت"
    )
    
    header_style = models.CharField(
        max_length=20,
        default="fixed",
        verbose_name="نوع هدر",
        help_text="نحوه نمایش هدر سایت",
        choices=[
            ('fixed', 'ثابت'),
            ('sticky', 'چسبان'),
            ('static', 'استاتیک'),
        ]
    )
    
    footer_style = models.CharField(
        max_length=20,
        default="full",
        verbose_name="نوع فوتر",
        help_text="نحوه نمایش فوتر سایت",
        choices=[
            ('full', 'کامل'),
            ('minimal', 'مینیمال'),
            ('compact', 'فشرده'),
        ]
    )
    
    # Feature Toggles
    enable_ai_features = models.BooleanField(default=True)
    enable_sandbox = models.BooleanField(default=True)
    enable_live_chat = models.BooleanField(default=True)
    enable_newsletter = models.BooleanField(default=True)
    enable_blog = models.BooleanField(default=True)
    
    # API Configuration
    api_rate_limit = models.IntegerField(default=1000, help_text="Requests per hour per user")
    max_file_upload_size = models.IntegerField(default=10, help_text="Maximum file size in MB")
    
    # Analytics and Tracking
    google_analytics_id = models.CharField(max_length=20, blank=True, null=True)
    google_tag_manager_id = models.CharField(max_length=20, blank=True, null=True)
    facebook_pixel_id = models.CharField(max_length=20, blank=True, null=True)
    
    # Email Configuration
    smtp_host = models.CharField(max_length=100, default="smtp.gmail.com")
    smtp_port = models.IntegerField(default=587)
    smtp_use_tls = models.BooleanField(default=True)
    
    # Maintenance Mode
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(
        default="سایت در حال بروزرسانی است. لطفاً بعداً مراجعه کنید.",
        blank=True
    )
    
    # Custom CSS/JS
    custom_css = models.TextField(blank=True, help_text="Custom CSS code")
    custom_js = models.TextField(blank=True, help_text="Custom JavaScript code")
    
    # JSON Configuration Fields
    hero_section_config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Hero section configuration (title, subtitle, CTA buttons, etc.)"
    )
    
    features_config = models.JSONField(
        default=list,
        blank=True,
        help_text="Main features configuration"
    )
    
    testimonials_config = models.JSONField(
        default=list,
        blank=True,
        help_text="Customer testimonials configuration"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"
        default_permissions = ()
        permissions = [
            ('SiteSettings_view', 'می‌تواند تنظیمات سایت را مشاهده کند'),
            ('SiteSettings_change', 'می‌تواند تنظیمات سایت را تغییر دهد'),
            ('SiteSettings_manage', 'می‌تواند تنظیمات سایت را مدیریت کند'),
        ]
    
    def __str__(self):
        return f"{self.company_name} Settings"
    
    def clean(self):
        """Validate settings"""
        super().clean()
        
        # Validate JSON fields
        if self.hero_section_config and not isinstance(self.hero_section_config, dict):
            raise ValidationError("Hero section config must be a valid JSON object")
        
        if self.features_config and not isinstance(self.features_config, list):
            raise ValidationError("Features config must be a valid JSON array")
            
        if self.testimonials_config and not isinstance(self.testimonials_config, list):
            raise ValidationError("Testimonials config must be a valid JSON array")
    
    @property
    def theme_colors(self):
        """Return theme colors as dictionary"""
        return {
            'primary': self.primary_color,
            'secondary': self.secondary_color,
            'accent': self.accent_color,
        }
    
    def get_hero_config(self):
        """Get hero section configuration with defaults"""
        default_config = {
            'title': 'راهکارهای هوشمند فناوری',
            'subtitle': 'با TakoTech آینده را بسازید',
            'cta_primary': 'مشاهده محصولات',
            'cta_secondary': 'درخواست مشاوره',
            'background_type': 'gradient',
            'show_stats': True,
        }
        
        if self.hero_section_config:
            default_config.update(self.hero_section_config)
        
        return default_config
    
    def get_features_list(self):
        """Get features list with defaults"""
        default_features = [
            {
                'title': 'هوش مصنوعی پیشرفته',
                'description': 'راهکارهای AI برای بهبود عملکرد کسب‌وکار',
                'icon': 'brain',
                'color': 'blue'
            },
            {
                'title': 'امنیت سایبری',
                'description': 'حفاظت کامل از داده‌ها و سیستم‌های شما',
                'icon': 'shield',
                'color': 'green'
            },
            {
                'title': 'توسعه نرم‌افزار',
                'description': 'نرم‌افزارهای سفارشی متناسب با نیازهای شما',
                'icon': 'code',
                'color': 'purple'
            }
        ]
        
        return self.features_config if self.features_config else default_features


class APIConfiguration(models.Model):
    """
    API Keys and external service configurations
    Separate model for security reasons
    """
    
    # AI/ML Services
    openai_api_key = models.CharField(max_length=200, blank=True, null=True)
    huggingface_api_key = models.CharField(max_length=200, blank=True, null=True)
    
    # Payment Gateways
    zarinpal_merchant_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_publishable_key = models.CharField(max_length=200, blank=True, null=True)
    stripe_secret_key = models.CharField(max_length=200, blank=True, null=True)
    
    # Social Auth Keys
    google_client_id = models.CharField(max_length=200, blank=True, null=True)
    google_client_secret = models.CharField(max_length=200, blank=True, null=True)
    github_client_id = models.CharField(max_length=200, blank=True, null=True)
    github_client_secret = models.CharField(max_length=200, blank=True, null=True)
    
    # External APIs
    recaptcha_site_key = models.CharField(max_length=100, blank=True, null=True)
    recaptcha_secret_key = models.CharField(max_length=100, blank=True, null=True)
    
    # Communication Services
    telegram_bot_token = models.CharField(max_length=200, blank=True, null=True)
    slack_webhook_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "تنظیمات API"
        verbose_name_plural = "تنظیمات‌های API"
        default_permissions = ()
        permissions = [
            ('APIConfiguration_view', 'می‌تواند تنظیمات API را مشاهده کند'),
            ('APIConfiguration_change', 'می‌تواند تنظیمات API را تغییر دهد'),
            ('APIConfiguration_manage', 'می‌تواند تنظیمات API را مدیریت کند'),
        ]
    
    def __str__(self):
        return "API Configuration"


class FeatureFlag(models.Model):
    """
    Feature flags for A/B testing and gradual rollouts
    """
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    
    # A/B Testing
    percentage = models.IntegerField(
        default=0, 
        help_text="Percentage of users who see this feature (0-100)"
    )
    
    # User Targeting
    target_user_types = models.JSONField(
        default=list,
        blank=True,
        help_text="List of user types to target (e.g., ['premium', 'beta'])"
    )
    
    # Date Range
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پرچم ویژگی"
        verbose_name_plural = "پرچم‌های ویژگی"
        ordering = ['name']
        default_permissions = ()
        permissions = [
            ('FeatureFlag_view', 'می‌تواند پرچم‌های ویژگی را مشاهده کند'),
            ('FeatureFlag_add', 'می‌تواند پرچم ویژگی جدید ایجاد کند'),
            ('FeatureFlag_change', 'می‌تواند پرچم‌های ویژگی را تغییر دهد'),
            ('FeatureFlag_delete', 'می‌تواند پرچم‌های ویژگی را حذف کند'),
            ('FeatureFlag_toggle', 'می‌تواند پرچم‌های ویژگی را فعال/غیرفعال کند'),
        ]
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
    def is_enabled_for_user(self, user=None):
        """Check if feature is enabled for specific user"""
        if not self.is_active:
            return False
        
        # Check date range
        from django.utils import timezone
        now = timezone.now()
        
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        # Check percentage rollout
        if self.percentage == 0:
            return False
        
        if self.percentage == 100:
            return True
        
        # Simple hash-based percentage check
        if user and user.is_authenticated:
            user_hash = hash(f"{user.id}{self.name}") % 100
            return user_hash < self.percentage
        
        return False


class SiteTemplate(models.Model):
    """
    Dynamic template management system
    """
    
    TEMPLATE_TYPES = [
        ('homepage', 'صفحه اصلی'),
        ('product_list', 'فهرست محصولات'),
        ('product_detail', 'جزئیات محصول'),
        ('service_list', 'فهرست خدمات'),
        ('service_detail', 'جزئیات خدمات'),
        ('about', 'درباره ما'),
        ('contact', 'تماس با ما'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name="نام قالب",
        help_text="نام قالب برای شناسایی"
    )
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        verbose_name="نوع قالب",
        help_text="نوع صفحه‌ای که این قالب برای آن استفاده می‌شود"
    )
    
    # Template Structure
    header_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="تنظیمات هدر",
        help_text="تنظیمات JSON برای هدر"
    )
    
    hero_section_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="تنظیمات بخش اصلی",
        help_text="تنظیمات JSON برای بخش hero"
    )
    
    content_sections = models.JSONField(
        default=list,
        blank=True,
        verbose_name="بخش‌های محتوا",
        help_text="لیست بخش‌های محتوا به صورت JSON"
    )
    
    footer_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="تنظیمات فوتر",
        help_text="تنظیمات JSON برای فوتر"
    )
    
    # Styling
    custom_css = models.TextField(
        blank=True,
        verbose_name="CSS سفارشی",
        help_text="کدهای CSS سفارشی برای این قالب"
    )
    
    custom_js = models.TextField(
        blank=True,
        verbose_name="JavaScript سفارشی",
        help_text="کدهای JavaScript سفارشی برای این قالب"
    )
    
    # Layout Settings
    layout_grid = models.CharField(
        max_length=20,
        default="12-col",
        verbose_name="نوع گرید",
        help_text="نوع گرید برای چیدمان",
        choices=[
            ('12-col', '12 ستونی'),
            ('16-col', '16 ستونی'),
            ('flexbox', 'Flexbox'),
            ('css-grid', 'CSS Grid'),
        ]
    )
    
    responsive_breakpoints = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="نقاط شکست ریسپانسیو",
        help_text="تنظیمات نقاط شکست برای طراحی ریسپانسیو"
    )
    
    # Status and Management
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
        help_text="آیا این قالب فعال باشد؟"
    )
    
    is_default = models.BooleanField(
        default=False,
        verbose_name="پیش‌فرض",
        help_text="آیا این قالب به عنوان پیش‌فرض استفاده شود؟"
    )
    
    version = models.CharField(
        max_length=10,
        default="1.0.0",
        verbose_name="نسخه",
        help_text="نسخه قالب"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "قالب سایت"
        verbose_name_plural = "قالب‌های سایت"
        ordering = ['-is_default', 'template_type', 'name']
        default_permissions = ()
        permissions = [
            ('SiteTemplate_view', 'می‌تواند قالب‌های سایت را مشاهده کند'),
            ('SiteTemplate_add', 'می‌تواند قالب سایت جدید ایجاد کند'),
            ('SiteTemplate_change', 'می‌تواند قالب‌های سایت را تغییر دهد'),
            ('SiteTemplate_delete', 'می‌تواند قالب‌های سایت را حذف کند'),
            ('SiteTemplate_activate', 'می‌تواند قالب‌های سایت را فعال کند'),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def save(self, *args, **kwargs):
        # Ensure only one default template per type
        if self.is_default:
            SiteTemplate.objects.filter(
                template_type=self.template_type,
                is_default=True
            ).exclude(id=self.id).update(is_default=False)
        
        super().save(*args, **kwargs)


class FontSettings(models.Model):
    """مدل مدیریت فونت‌های سیستم"""

    FONT_FORMATS = [
        ('ttf', 'TrueType Font (.ttf)'),
        ('woff', 'Web Open Font Format (.woff)'),
        ('woff2', 'Web Open Font Format 2 (.woff2)'),
        ('eot', 'Embedded OpenType (.eot)'),
        ('otf', 'OpenType Font (.otf)'),
    ]

    FONT_WEIGHTS = [
        (100, 'Thin'),
        (200, 'Extra Light'),
        (300, 'Light'),
        (400, 'Regular'),
        (500, 'Medium'),
        (600, 'Semi Bold'),
        (700, 'Bold'),
        (800, 'Extra Bold'),
        (900, 'Black'),
    ]

    name = models.CharField(max_length=100, verbose_name=_("نام فونت"))
    family_name = models.CharField(
        max_length=100,
        verbose_name=_("نام خانواده فونت"),
        help_text=_("نام CSS font-family"),
    )
    font_file = models.FileField(upload_to='fonts/', verbose_name=_("فایل فونت"))
    font_format = models.CharField(max_length=10, choices=FONT_FORMATS, verbose_name=_("فرمت فونت"))
    font_weight = models.IntegerField(choices=FONT_WEIGHTS, default=400, verbose_name=_("وزن فونت"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))
    is_default = models.BooleanField(default=False, verbose_name=_("فونت پیش‌فرض"))
    is_rtl_support = models.BooleanField(default=True, verbose_name=_("پشتیبانی از راست به چپ"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))

    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("حجم فایل (بایت)"))
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ آپلود"))
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("آپلود شده توسط"),
    )

    class Meta:
        verbose_name = _("تنظیمات فونت")
        verbose_name_plural = _("تنظیمات فونت‌ها")
        ordering = ['-is_default', '-is_active', 'name']
        default_permissions = ()
        permissions = [
            ('FontSettings_view', 'می‌تواند تنظیمات فونت‌ها را مشاهده کند'),
            ('FontSettings_add', 'می‌تواند تنظیمات فونت جدید ایجاد کند'),
            ('FontSettings_change', 'می‌تواند تنظیمات فونت‌ها را تغییر دهد'),
            ('FontSettings_delete', 'می‌تواند تنظیمات فونت‌ها را حذف کند'),
            ('FontSettings_activate', 'می‌تواند تنظیمات فونت‌ها را فعال کند'),
        ]

    def __str__(self):
        status = "فعال" if self.is_active else "غیرفعال"
        default = " (پیش‌فرض)" if self.is_default else ""
        return f"{self.name} - {self.get_font_weight_display()}{default} [{status}]"

    def save(self, *args, **kwargs):
        if self.is_default:
            FontSettings.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        if self.font_file and hasattr(self.font_file, 'size'):
            self.file_size = self.font_file.size
        super().save(*args, **kwargs)

    @property
    def file_size_formatted(self):
        if not self.file_size:
            return "نامشخص"
        if self.file_size < 1024:
            return f"{self.file_size} بایت"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} کیلوبایت"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} مگابایت"

    @classmethod
    def get_default_font(cls):
        return cls.objects.filter(is_default=True, is_active=True).first()

    @classmethod
    def get_active_fonts(cls):
        return cls.objects.filter(is_active=True).order_by('-is_default', 'name')

    def get_css_font_face(self):
        if not self.font_file:
            return ""
        format_map = {
            'ttf': 'truetype',
            'woff': 'woff',
            'woff2': 'woff2',
            'eot': 'embedded-opentype',
            'otf': 'opentype',
        }
        css_format = format_map.get(self.font_format, self.font_format)
        return f"""@font-face {{
    font-family: '{self.family_name}';
    src: url('{self.font_file.url}') format('{css_format}');
    font-weight: {self.font_weight};
    font-style: normal;
    font-display: swap;
}}"""