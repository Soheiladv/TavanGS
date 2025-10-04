"""
Users App Models - Advanced Authentication System
Custom user model with RBAC, profiles, and security features
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User Model with enhanced features
    """
    
    USER_TYPES = [
        ('free', 'Free User'),
        ('premium', 'Premium User'),
        ('enterprise', 'Enterprise User'),
        ('beta', 'Beta Tester'),
        ('admin', 'Administrator'),
    ]
    
    # Replace username with email
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional fields
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='free')
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    
    # Security fields
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    
    # Profile fields
    company_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Preferences
    language = models.CharField(max_length=10, default='fa')
    timezone = models.CharField(max_length=50, default='Asia/Tehran')
    theme = models.CharField(
        max_length=10, 
        choices=[('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')], 
        default='light'
    )
    
    # Notifications preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=False)
    
    # API access
    api_key = models.UUIDField(default=uuid.uuid4, unique=True)
    api_calls_count = models.PositiveIntegerField(default=0)
    api_rate_limit = models.PositiveIntegerField(default=1000)  # per hour
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
        default_permissions = ()
        permissions = [
            ('User_view', 'می‌تواند کاربران را مشاهده کند'),
            ('User_add', 'می‌تواند کاربر جدید ایجاد کند'),
            ('User_change', 'می‌تواند کاربران را تغییر دهد'),
            ('User_delete', 'می‌تواند کاربران را حذف کند'),
            ('User_manage_permissions', 'می‌تواند مجوزهای کاربران را مدیریت کند'),
            ('User_reset_password', 'می‌تواند رمز عبور کاربران را ریست کند'),
            ('User_activate_deactivate', 'می‌تواند کاربران را فعال/غیرفعال کند'),
        ]
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Return full name or email if name is not set"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
    
    @property
    def is_premium(self):
        """Check if user has premium access"""
        return self.user_type in ['premium', 'enterprise', 'admin']
    
    def can_access_feature(self, feature_name):
        """Check if user can access specific feature"""
        feature_permissions = {
            'ai_features': ['premium', 'enterprise', 'admin'],
            'sandbox': ['free', 'premium', 'enterprise', 'admin'],
            'advanced_analytics': ['enterprise', 'admin'],
            'api_access': ['premium', 'enterprise', 'admin'],
        }
        
        allowed_types = feature_permissions.get(feature_name, [])
        return self.user_type in allowed_types