"""
News App Signals - News Management Signals
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import News


@receiver(pre_save, sender=News)
def news_pre_save(sender, instance, **kwargs):
    """قبل از ذخیره خبر"""
    # اگر وضعیت به published تغییر کرد و published_at خالی است
    if instance.status == 'published' and not instance.published_at:
        instance.published_at = timezone.now()


@receiver(post_save, sender=News)
def news_post_save(sender, instance, created, **kwargs):
    """بعد از ذخیره خبر"""
    if created:
        # ارسال اعلان برای خبر جدید
        # اینجا می‌توانید اعلان‌ها را ارسال کنید
        pass
