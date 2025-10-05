"""
News App Models - News and Articles Management
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class NewsCategory(models.Model):
    """دسته‌بندی اخبار"""
    
    name = models.CharField(max_length=100, verbose_name="نام")
    slug = models.SlugField(unique=True, blank=False, verbose_name="نامک")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    color = models.CharField(max_length=20, default='#3b82f6', verbose_name="رنگ")
    icon = models.CharField(max_length=50, blank=True, verbose_name="آیکون")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = 'دسته‌بندی خبر'
        verbose_name_plural = 'دسته‌بندی‌های اخبار'
        ordering = ['name']
        default_permissions = ()
        permissions = [
            ('NewsCategory_view', 'می‌تواند دسته‌بندی اخبار را مشاهده کند'),
            ('NewsCategory_add', 'می‌تواند دسته‌بندی خبر جدید ایجاد کند'),
            ('NewsCategory_change', 'می‌تواند دسته‌بندی اخبار را تغییر دهد'),
            ('NewsCategory_delete', 'می‌تواند دسته‌بندی اخبار را حذف کند'),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class News(models.Model):
    """مدل اخبار"""
    
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('archived', 'آرشیو شده'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'پایین'),
        ('normal', 'عادی'),
        ('high', 'بالا'),
        ('urgent', 'فوری'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, blank=True, verbose_name="نامک")
    summary = models.TextField(max_length=500, verbose_name="خلاصه")
    content = models.TextField(verbose_name="محتوا")
    
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name="دسته‌بندی")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    
    # Media
    featured_image = models.ImageField(upload_to='news/images/', blank=True, null=True, verbose_name="تصویر شاخص")
    gallery = models.JSONField(default=list, blank=True, verbose_name="گالری تصاویر")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="عنوان متا")
    meta_description = models.TextField(max_length=300, blank=True, verbose_name="توضیحات متا")
    meta_keywords = models.CharField(max_length=500, blank=True, verbose_name="کلمات کلیدی")
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name="اولویت")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_pinned = models.BooleanField(default=False, verbose_name="سنجاق شده")
    
    # Publishing
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضا")
    
    # Statistics
    view_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    like_count = models.PositiveIntegerField(default=0, verbose_name="تعداد لایک")
    share_count = models.PositiveIntegerField(default=0, verbose_name="تعداد اشتراک")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'
        ordering = ['-is_pinned', '-published_at', '-created_at']
        default_permissions = ()
        permissions = [
            ('News_view', 'می‌تواند اخبار را مشاهده کند'),
            ('News_add', 'می‌تواند خبر جدید ایجاد کند'),
            ('News_change', 'می‌تواند اخبار را تغییر دهد'),
            ('News_delete', 'می‌تواند اخبار را حذف کند'),
            ('News_publish', 'می‌تواند اخبار را منتشر کند'),
            ('News_feature', 'می‌تواند اخبار را ویژه کند'),
            ('News_analytics', 'می‌تواند آمار اخبار را مشاهده کند'),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increment_view_count(self):
        """افزایش تعداد بازدید"""
        from django.db import models
        News.objects.filter(pk=self.pk).update(
            view_count=models.F('view_count') + 1
        )
    
    @property
    def is_published(self):
        """آیا خبر منتشر شده است؟"""
        return self.status == 'published' and self.published_at is not None
    
    @property
    def is_expired(self):
        """آیا خبر منقضی شده است؟"""
        if not self.expires_at:
            return False
        from django.utils import timezone
        return timezone.now() > self.expires_at


class NewsComment(models.Model):
    """نظرات اخبار"""
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name="خبر")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="پاسخ به")
    
    content = models.TextField(verbose_name="محتوا")
    is_approved = models.BooleanField(default=True, verbose_name="تأیید شده")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = 'نظر خبر'
        verbose_name_plural = 'نظرات اخبار'
        ordering = ['-created_at']
        default_permissions = ()
        permissions = [
            ('NewsComment_view', 'می‌تواند نظرات اخبار را مشاهده کند'),
            ('NewsComment_add', 'می‌تواند نظر جدید ایجاد کند'),
            ('NewsComment_change', 'می‌تواند نظرات را تغییر دهد'),
            ('NewsComment_delete', 'می‌تواند نظرات را حذف کند'),
            ('NewsComment_moderate', 'می‌تواند نظرات را مدیریت کند'),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.news.title[:50]}"


class NewsTag(models.Model):
    """تگ‌های اخبار"""
    
    name = models.CharField(max_length=50, unique=True, verbose_name="نام")
    slug = models.SlugField(unique=True, blank=True, verbose_name="نامک")
    color = models.CharField(max_length=20, default='#6b7280', verbose_name="رنگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = 'تگ خبر'
        verbose_name_plural = 'تگ‌های اخبار'
        ordering = ['name']
        default_permissions = ()
        permissions = [
            ('NewsTag_view', 'می‌تواند تگ‌های اخبار را مشاهده کند'),
            ('NewsTag_add', 'می‌تواند تگ جدید ایجاد کند'),
            ('NewsTag_change', 'می‌تواند تگ‌ها را تغییر دهد'),
            ('NewsTag_delete', 'می‌تواند تگ‌ها را حذف کند'),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NewsTagRelation(models.Model):
    """رابطه اخبار و تگ‌ها"""
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name="خبر")
    tag = models.ForeignKey(NewsTag, on_delete=models.CASCADE, verbose_name="تگ")
    
    class Meta:
        verbose_name = 'رابطه خبر و تگ'
        verbose_name_plural = 'رابطه‌های خبر و تگ'
        unique_together = ['news', 'tag']
        default_permissions = ()
    
    def __str__(self):
        return f"{self.news.title} - {self.tag.name}"
