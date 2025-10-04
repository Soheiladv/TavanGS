import datetime
import logging
from django.utils.timezone import now
logger = logging.getLogger(__name__)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
import hashlib

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("نام استان"))
    code = models.CharField(max_length=2, unique=True, verbose_name=_("کد استان"), help_text=_("کد دو رقمی استان"))

    class Meta:
        verbose_name = _("استان")
        verbose_name_plural = _("استان‌ها")
        default_permissions = []
        permissions = [
            ("view_province", _("می‌تواند استان را مشاهده کند")),
            ("add_province", _("می‌تواند استان جدید اضافه کند")),
            ("change_province", _("می‌تواند استان را تغییر دهد")),
            ("delete_province", _("می‌تواند استان را حذف کند")),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name
class City(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام شهر"))
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities", verbose_name=_("استان"))
    is_capital = models.BooleanField(default=False, verbose_name=_("مرکز استان است؟"))

    class Meta:
        verbose_name = _("شهر")
        verbose_name_plural = _("شهرها")
        unique_together = ('name', 'province')
        default_permissions = []
        permissions = [
            ("view_city", _("می‌تواند شهر را مشاهده کند")),
            ("add_city", _("می‌تواند شهر جدید اضافه کند")),
            ("change_city", _("می‌تواند شهر را تغییر دهد")),
            ("delete_city", _("می‌تواند شهر را حذف کند")),
        ]
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.province.name}"

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("ایمیل باید وارد شود"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('سوپرکاربر باید is_staff=True باشد.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('سوپرکاربر باید is_superuser=True باشد.'))

        return self.create_user(username, email, password, **extra_fields)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    roles = models.ManyToManyField('Role', related_name="custom_users", verbose_name=_("نقش‌ها"), blank=True)
    groups = models.ManyToManyField('MyGroup', through='CustomUserGroup', related_name='accounts_groups_set',
                                    verbose_name=_('عضویت در گروه'), blank=True)

    objects = CustomUserManager()

    username = models.CharField(max_length=150, unique=True, verbose_name=_('نام کاربری'))
    email = models.EmailField(unique=True, verbose_name=_('ایمیل کاربر'))

    first_name = models.CharField(max_length=30, blank=True, verbose_name=_('نام کوچک'))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_('فامیلی'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعالیت'))
    is_staff = models.BooleanField(default=False, verbose_name=_('کارمندی؟'))
    created_at = models.DateTimeField(auto_now_add=True)

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='accounts_user_set',
        help_text='مجوزهای خاص برای این کاربر.',
        related_query_name='user',
    )

    def get_active_branch(self):
        active_post = self.userpost_set.filter(is_active=True).first()
        return active_post.post.branch if active_post else None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("کاربر سفارشی")
        verbose_name_plural = _("کاربران سفارشی")
        default_permissions = []
        permissions = [
            ("users_view_customuser", _("می‌تواند کاربران سفارشی را مشاهده کند")),
            ("users_add_customuser", _("می‌تواند کاربر سفارشی جدید اضافه کند")),
            ("users_change_customuser", _("می‌تواند کاربر سفارشی را تغییر دهد")),
            ("users_delete_customuser", _("می‌تواند کاربر سفارشی را حذف کند")),
        ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    def get_short_name(self):
        return self.first_name

    def get_all_permissions(self, obj=None):
        """
        برمی‌گردونه همه‌ی پرمیشن‌های کاربر به صورت lowercase
        تا تفاوت حروف بزرگ/کوچیک مشکلی ایجاد نکنه.
        """
        if not self.is_active:
            return set()
        if self.is_superuser:
            return {f"{p.content_type.app_label}.{p.codename}".lower() for p in Permission.objects.all()}

        perms = set()

        # 1. Permissions from roles directly assigned to the user
        for role in self.roles.all().prefetch_related('permissions__content_type'):
            perms.update(
                f"{p.content_type.app_label}.{p.codename}".lower()
                for p in role.permissions.all()
            )

        # 2. Permissions from roles within the user's groups
        for group in self.groups.all().prefetch_related('roles__permissions__content_type'):
            for role in group.roles.all():
                perms.update(
                    f"{p.content_type.app_label}.{p.codename}".lower()
                    for p in role.permissions.all()
                )

        # 3. Direct user permissions
        for p in self.user_permissions.all().select_related('content_type'):
            perms.add(f"{p.content_type.app_label}.{p.codename}".lower())

        return perms

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return perm.lower() in self.get_all_permissions(obj)

    def get_authorized_organizations(self):
        # Return empty queryset for now - can be implemented later
        return User.objects.none()

    @property
    def is_hq(self):
        if self.is_superuser:
            return True
        # Return False for now - can be implemented later
        return False

User = get_user_model()
class CustomProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile",
                                verbose_name=_("کاربر"))
    first_name = models.CharField(max_length=30, blank=True, verbose_name=_("نام"))
    last_name = models.CharField(max_length=30, blank=True, verbose_name=_("نام خانوادگی"))
    province = models.ForeignKey('Province', on_delete=models.SET_NULL, null=True, blank=True, related_name="profiles",
                                 verbose_name=_("استان"))
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True, related_name="profiles",
                             verbose_name=_("شهر"))
    phone_number = models.CharField(max_length=15, blank=True, verbose_name=_("شماره تلفن"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("تاریخ تولد"))
    address = models.TextField(blank=True, verbose_name=_("آدرس"))
    location = models.TextField(blank=True, verbose_name=_("موقعیت"))
    bio = models.TextField(blank=True, verbose_name=_("بیوگرافی"))
    zip_code = models.CharField(max_length=10, blank=True, verbose_name=_("کد پستی"))
    description = models.TextField(blank=True, verbose_name=_("توضیحات"))
    theme = models.CharField(max_length=20, default='default', choices=[])
    custom_theme_data = models.JSONField(null=True, blank=True, verbose_name=_("داده‌های تم سفارشی"))

    class Meta:
        verbose_name = _("پروفایل سفارشی")
        verbose_name_plural = _("پروفایل‌های سفارشی")
        default_permissions = []
        permissions = [
            ("users_view_userprofile", _("می‌تواند پروفایل کاربران را مشاهده کند")),
            ("users_add_userprofile", _("می‌تواند پروفایل کاربری اضافه کند")),
            ("users_update_userprofile", _("می‌تواند پروفایل کاربر را تغییر دهد")),
            ("users_delete_userprofile", _("می‌تواند پروفایل کاربر را غیرفعال کند")),
            ("users_search_userprofile", _("می‌تواند پروفایل کاربر را جستجو کند")),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.username}"
    
    @classmethod
    def get_theme_choices(cls):
        """دریافت choices تم‌ها به صورت پویا"""
        from .theme_config import get_theme_choices
        return get_theme_choices()
class Role(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("عنوان نقش"))
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name=_("مجوزها"), related_name='roles')
    description = models.TextField(max_length=400, blank=True, null=True, verbose_name=_("توضیحات نقش"))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                               verbose_name=_("نقش والدین"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))

    class Meta:
        verbose_name = _("نقش")
        verbose_name_plural = _("نقش‌ها")
        ordering = ["name"]
        default_permissions = []
        permissions = [
            ('Role_view', 'می‌تواند نقش‌ها را مشاهده کند'),
            ('Role_add', 'می‌تواند نقش جدید ایجاد کند'),
            ('Role_change', 'می‌تواند نقش‌ها را تغییر دهد'),
            ('Role_delete', 'می‌تواند نقش‌ها را حذف کند'),
            ('Role_assign_permissions', 'می‌تواند مجوزها را به نقش‌ها تخصیص دهد'),
        ]

    def __str__(self):
        return self.name

class MyGroup(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("نام گروه"))
    roles = models.ManyToManyField('Role', related_name='mygroups', blank=True, verbose_name=_("تعریف نقش"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ ویرایش"))

    class Meta:
        db_table = 'accounts_mygroups'
        default_permissions = []
        permissions = [
            ("MyGroup_can_view_group", "می‌تواند گروه‌ها را مشاهده کند"),
            ("MyGroup_can_add_group", "می‌تواند گروه جدید اضافه کند"),
            ("MyGroup_can_edit_group", "می‌تواند گروه را ویرایش کند"),
            ("MyGroup_can_delete_group", "می‌تواند گروه را حذف کند"),
        ]

        verbose_name = _("گروه")
        verbose_name_plural = _("گروه‌ها")
        ordering = ["name"]

    def __str__(self):
        return self.name
class CustomUserGroup(models.Model):
    customuser = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    mygroup = models.ForeignKey('MyGroup', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts_customuser_groups'
        verbose_name = 'افزودن کاربری'
        verbose_name_plural = 'افزودن کاربری'
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'افزودن'),
        ('read', 'نمایش'),
        ('update', 'بروزرسانی'),
        ('delete', 'حــذف'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('کاربر'))
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name=_('عملیات کاربری'))
    view_name = models.CharField(max_length=255, verbose_name=_('نام ویو'))
    path = models.CharField(max_length=255, verbose_name=_('مسیر درخواست'))
    method = models.CharField(max_length=10, verbose_name=_('متد HTTP'))
    model_name = models.CharField(max_length=255, verbose_name=_('نام مدل'))
    object_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('ابجکت'))
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_('زمان رخداد'))
    details = models.TextField(blank=True, verbose_name=_('ریزمشخصات'))
    changes = models.JSONField(null=True, blank=True, verbose_name=_('تغییرات'))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('آدرس IP'))
    browser = models.CharField(max_length=255, blank=True, verbose_name=_('بروزر'))
    status_code = models.IntegerField(null=True, blank=True, verbose_name=_('وضعیت کد'))
    related_object = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('شیء مرتبط'))

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"

    class Meta:
        db_table = 'accounts_audit_log'
        verbose_name = _("لاگ گیری از سیستم")
        verbose_name_plural = _("لاگ گیری از سیستم")
        ordering = ["-timestamp"]
        default_permissions = []
        permissions = [
            ('AuditLog_view', _('می‌تواند لاگ‌ها را مشاهده کند')),
            ('AuditLog_add', _('می‌تواند لاگ‌ها را اضافه کند')),
            ('AuditLog_update', _('می‌تواند لاگ‌ها را بروزرسانی کند')),
            ('AuditLog_delete', _('می‌تواند لاگ‌ها را حذف کند')),
        ]

class ActiveUser(models.Model):
    MAX_ACTIVE_USERS = None
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='active_sessions',
        related_query_name='active_session',
        verbose_name=_("کاربر"),
        help_text=_("کاربری که این سشن به او تعلق دارد"),
    )
    session_key = models.CharField(
        max_length=40,
        unique=False,
        blank=False,
        null=False,
        verbose_name=_("کلید سشن"),
        help_text=_("شناسه یکتا برای سشن کاربر"),
        db_index=True,
    )
    login_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("زمان ورود"),
        help_text=_("زمان ورود کاربر به سیستم"),
        db_index=True,
    )
    hashed_count = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_("هش تعداد کاربران"),
        help_text=_("هش تعداد کاربران فعال برای امنیت بیشتر"),
    )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name=_("آخرین فعالیت"),
        help_text=_("آخرین زمان فعالیت کاربر"),
        db_index=True,
    )
    user_ip = models.GenericIPAddressField(
        protocol='both',
        unpack_ipv4=False,
        verbose_name=_("آی‌پی کاربر"),
        blank=True,
        null=True,
        help_text=_("آدرس IP کاربر در زمان ورود"),
    )
    user_agent = models.TextField(
        verbose_name=_("مرورگر/دستگاه کاربر"),
        blank=True,
        null=True,
        help_text=_("اطلاعات مرورگر یا دستگاه کاربر"),
        default='',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال"),
        help_text=_("آیا این سشن هنوز فعال است؟"),
    )
    logout_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("زمان خروج"),
        help_text=_("زمان خروج کاربر از سیستم، در صورت ثبت"),
    )

    class Meta:
        verbose_name = _("کاربر فعال")
        verbose_name_plural = _("کاربران فعال")
        default_permissions = []
        permissions = [
            ('activeuser_view', _('نمایش تعداد کاربر دارای مجوز برای کار در سیستم')),
            ('activeuser_add', _('افزودن تعداد کاربر دارای مجوز برای کار در سیستم')),
            ('activeuser_update', _('آپدیت تعداد کاربر دارای مجوز برای کار در سیستم')),
            ('activeuser_delete', _('حذف تعداد کاربر دارای مجوز برای کار در سیستم')),
        ]
        indexes = [
            models.Index(fields=['user'], name='idx_user'),
            models.Index(fields=['last_activity'], name='idx_last_activity'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='unique_user_session',
                violation_error_message=_("هر کاربر تنها می‌تواند یک سشن فعال داشته باشد.")            ),
            models.CheckConstraint(
                check=models.Q(login_time__lte=models.F('last_activity')),
                name='check_login_before_activity',
                violation_error_message=_("هر کاربر تنها می‌تواند یک سشن فعال داشته باشد.")            ),
        ]
        ordering = ['-last_activity', 'user']
        app_label = 'accounts'

    @classmethod
    def remove_inactive_users(cls):
        inactivity_threshold = now() - datetime.timedelta(minutes=30)
        inactive_users = cls.objects.filter(last_activity__lt=inactivity_threshold)
        if inactive_users.exists():
            for user in inactive_users:
                logger.info(f"حذف کاربر غیرفعال: {user.user.username} (آی‌پی: {user.user_ip})")
                from django.contrib.sessions.models import Session
                Session.objects.filter(session_key=user.session_key).delete()
                user.delete()
        else:
            logger.info("هیچ کاربر غیرفعالی برای حذف یافت نشد.")

    @classmethod
    def delete_expired_sessions(cls):
        from django.contrib.sessions.models import Session
        expired_sessions = Session.objects.filter(expire_date__lt=now())
        for session in expired_sessions:
            cls.objects.filter(session_key=session.session_key).delete()
            session.delete()

    def save(self, *args, **kwargs):
        active_count = ActiveUser.objects.filter(last_activity__gte=now() - datetime.timedelta(minutes=30)).count()
        self.last_activity = now()
        self.hashed_count = hashlib.sha256(str(active_count).encode()).hexdigest()
        super().save(*args, **kwargs)

    @classmethod
    def can_login(cls, session_key):
        active_count = cls.objects.filter(
            last_activity__gte=now() - datetime.timedelta(minutes=30)
        ).count()
        max_users = cls.get_max_active_users()
        logger.info(
            f"کاربران فعال: {cls.objects.filter(last_activity__gte=now() - datetime.timedelta(minutes=30)).values_list('user__username', flat=True)}")
        return active_count < max_users

    def __str__(self):
        return f"{self.user.username} - {self.session_key} - {self.login_time}"

    @classmethod
    def get_max_active_users(cls):
            expiry_date, max_users, _, _ = TimeLockModel.get_latest_lock()
            return max_users if max_users is not None else getattr(settings, 'MAX_ACTIVE_USERS', 2)

from cryptography.fernet import Fernet, InvalidToken

try:
    cipher = settings.RCMS_SECRET_KEY_CIPHER
except AttributeError:
    logger.error("settings.RCMS_SECRET_KEY_CIPHER is not defined or is not a Fernet object. TimeLockModel will not function correctly.")
    cipher = Fernet(Fernet.generate_key())

class TimeLockModel(models.Model):
    lock_key = models.TextField(verbose_name="کلید قفل (رمزنگاری‌شده)")
    hash_value = models.CharField(max_length=64, verbose_name="هش مقدار تنظیم‌شده", unique=True)
    salt = models.CharField(max_length=32, verbose_name="مقدار تصادفی", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت فعال")
    organization_name = models.CharField(max_length=255, verbose_name="نام مجموعه",  default=_("پیش‌فرض") )

    def save(self, *args, **kwargs):
        import secrets
        if not self.salt:
            self.salt = secrets.token_hex(16)
        super().save(*args, **kwargs)

    @staticmethod
    def encrypt_value(value):
        return cipher.encrypt(str(value).encode()).decode()

    @staticmethod
    def decrypt_value(encrypted_value):
        try:
            if isinstance(encrypted_value, str):
                encrypted_value = encrypted_value.encode()
            decrypted = cipher.decrypt(encrypted_value).decode()
            return decrypted
        except InvalidToken:
            return None

    @staticmethod
    def create_lock_key(expiry_date: datetime.date, max_users: int, salt: str, organization_name: str = "") -> str:
        combined = f"{expiry_date.isoformat()}-{max_users}-{salt}-{organization_name}"
        return TimeLockModel.encrypt_value(combined)

    def get_decrypted_data(self):
        decrypted = self.decrypt_value(self.lock_key)
        if decrypted:
            try:
                parts = decrypted.split("-")
                if len(parts) < 4:
                    raise ValueError("فرمت مقدار رمزگشایی‌شده نادرست است")
                expiry_str = "-".join(parts[:3])
                max_users_str = parts[3]
                organization_name = "-".join(parts[4:]) if len(parts) > 4 else ""
                expiry_date = datetime.date.fromisoformat(expiry_str)
                max_users = int(max_users_str)
                return expiry_date, max_users, organization_name
            except (ValueError, TypeError) as e:
                logger.error(f"🔴 خطا در رمزگشایی کلید ID {self.id}: {e}")
                return None, None, None
        return None, None, None

    def get_decrypted_expiry_date(self):
        expiry_date, _, _ = self.get_decrypted_data()
        return expiry_date

    def get_decrypted_max_users(self):
        _, max_users, _ = self.get_decrypted_data()
        return max_users

    def get_decrypted_organization_name(self):
        _, _, organization_name = self.get_decrypted_data()
        return organization_name

    @staticmethod
    def get_latest_lock():
        latest_instance = TimeLockModel.objects.filter(is_active=True).order_by('-created_at').first()
        if not latest_instance:
            return None, None, None, None
        expiry_date, max_users, organization_name = latest_instance.get_decrypted_data()
        return expiry_date, max_users, latest_instance.hash_value, organization_name

    class Meta:
        verbose_name = "قفل سیستم"
        verbose_name_plural = "قفل سیستم"
        default_permissions = []
        permissions = [
            ("TimeLockModel_view", "نمایش قفل سیستم"),
            ("TimeLockModel_add", "افزودن قفل سیستم"),
            ("TimeLockModel_update", "ویرایش قفل سیستم"),
            ("TimeLockModel_delete", "حذف قفل سیستم"),
        ]
