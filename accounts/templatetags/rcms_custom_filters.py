from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def to_persian_number(value):
    """تبدیل اعداد انگلیسی به فارسی"""
    if value is None:
        return ""
    
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    result = str(value)
    for en, fa in zip(english_digits, persian_digits):
        result = result.replace(en, fa)
    return result

@register.filter
def format_negative(value):
    """فرمت کردن اعداد منفی"""
    if value is None:
        return ""
    
    try:
        num = float(value)
        if num < 0:
            return f"({abs(num):,.0f})"
        else:
            return f"{num:,.0f}"
    except (ValueError, TypeError):
        return str(value)

@register.filter
def persian_date(value):
    """تبدیل تاریخ به فارسی"""
    if not value:
        return ""
    
    try:
        from django_jalali.templatetags.jalali_filters import to_jalali
        return to_jalali(value, '%Y/%m/%d')
    except:
        return str(value)

@register.filter
def persian_datetime(value):
    """تبدیل تاریخ و زمان به فارسی"""
    if not value:
        return ""
    
    try:
        from django_jalali.templatetags.jalali_filters import to_jalali
        return to_jalali(value, '%Y/%m/%d %H:%M')
    except:
        return str(value)

@register.filter
def format_currency(value):
    """فرمت کردن پول"""
    if value is None:
        return "۰ تومان"
    
    try:
        num = float(value)
        formatted = f"{num:,.0f}"
        # تبدیل به فارسی
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        for en, fa in zip(english_digits, persian_digits):
            formatted = formatted.replace(en, fa)
        return f"{formatted} تومان"
    except (ValueError, TypeError):
        return str(value)

@register.filter
def truncate_persian(value, length=50):
    """کوتاه کردن متن فارسی"""
    if not value:
        return ""
    
    if len(str(value)) <= length:
        return str(value)
    
    return str(value)[:length] + "..."

@register.filter
def highlight_search(text, search_term):
    """هایلایت کردن کلمات جستجو"""
    if not text or not search_term:
        return text
    
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    highlighted = pattern.sub(f'<mark>{search_term}</mark>', str(text))
    return mark_safe(highlighted)

@register.filter
def status_badge(status):
    """ایجاد badge برای وضعیت"""
    status_colors = {
        'active': 'success',
        'inactive': 'secondary',
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'completed': 'success',
        'cancelled': 'danger'
    }
    
    color = status_colors.get(status.lower(), 'secondary')
    return mark_safe(f'<span class="badge bg-{color}">{status}</span>')

@register.filter
def progress_bar(percentage):
    """ایجاد نوار پیشرفت"""
    if percentage is None:
        percentage = 0
    
    try:
        percent = int(float(percentage))
        if percent > 100:
            percent = 100
        elif percent < 0:
            percent = 0
    except (ValueError, TypeError):
        percent = 0
    
    color = 'success' if percent >= 80 else 'warning' if percent >= 50 else 'danger'
    
    return mark_safe(f'''
        <div class="progress" style="height: 20px;">
            <div class="progress-bar bg-{color}" role="progressbar" 
                 style="width: {percent}%" aria-valuenow="{percent}" 
                 aria-valuemin="0" aria-valuemax="100">
                {percent}%
            </div>
        </div>
    ''')

@register.filter
def file_size(value):
    """فرمت کردن اندازه فایل"""
    if not value:
        return "۰ بایت"
    
    try:
        size = int(value)
        for unit in ['بایت', 'کیلوبایت', 'مگابایت', 'گیگابایت']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} ترابایت"
    except (ValueError, TypeError):
        return str(value)

@register.filter
def boolean_icon(value):
    """آیکون برای مقادیر boolean"""
    if value:
        return mark_safe('<i class="fas fa-check text-success"></i>')
    else:
        return mark_safe('<i class="fas fa-times text-danger"></i>')

@register.filter
def user_avatar(user):
    """آواتار کاربر"""
    if not user:
        return mark_safe('<i class="fas fa-user-circle fa-2x text-muted"></i>')
    
    if hasattr(user, 'avatar') and user.avatar:
        return mark_safe(f'<img src="{user.avatar.url}" class="rounded-circle" width="40" height="40">')
    else:
        return mark_safe('<i class="fas fa-user-circle fa-2x text-primary"></i>')