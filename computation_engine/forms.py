from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ComputationTemplate, ComputationSession, ComputationResult, ComputationMetrics


class ComputationTemplateForm(forms.ModelForm):
    """فرم ایجاد و ویرایش قالب محاسباتی"""
    
    class Meta:
        model = ComputationTemplate
        fields = [
            'name', 'description', 'session_type', 'input_schema', 'output_schema',
            'default_config', 'estimated_time_seconds', 'memory_requirement_mb',
            'cpu_intensive', 'required_user_type', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام قالب محاسباتی'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'توضیحات قالب'}),
            'session_type': forms.Select(attrs={'class': 'form-control'}),
            'input_schema': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'JSON Schema برای ورودی'}),
            'output_schema': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'JSON Schema برای خروجی'}),
            'default_config': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'پیکربندی پیش‌فرض JSON'}),
            'estimated_time_seconds': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'memory_requirement_mb': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'cpu_intensive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'required_user_type': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'name': _('نام قالب'),
            'description': _('توضیحات'),
            'session_type': _('نوع جلسه'),
            'input_schema': _('اسکیمای ورودی'),
            'output_schema': _('اسکیمای خروجی'),
            'default_config': _('پیکربندی پیش‌فرض'),
            'estimated_time_seconds': _('زمان تخمینی (ثانیه)'),
            'memory_requirement_mb': _('نیاز حافظه (مگابایت)'),
            'cpu_intensive': _('محاسبات سنگین'),
            'required_user_type': _('نوع کاربر مورد نیاز'),
            'is_active': _('فعال')
        }


class ComputationSessionForm(forms.ModelForm):
    """فرم ایجاد جلسه محاسباتی"""
    
    class Meta:
        model = ComputationSession
        fields = [
            'session_type', 'product_name', 'input_data', 'configuration',
            'priority'
        ]
        widgets = {
            'session_type': forms.Select(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام محصول'}),
            'input_data': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'داده‌های ورودی JSON'}),
            'configuration': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'پیکربندی JSON'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'})
        }
        labels = {
            'session_type': _('نوع جلسه'),
            'product_name': _('نام محصول'),
            'input_data': _('داده‌های ورودی'),
            'configuration': _('پیکربندی'),
            'priority': _('اولویت')
        }


class ComputationResultForm(forms.ModelForm):
    """فرم مدیریت نتایج محاسباتی"""
    
    class Meta:
        model = ComputationResult
        fields = [
            'session_type', 'input_data', 'output_data', 'configuration',
            'computation_time', 'expires_at', 'is_valid'
        ]
        widgets = {
            'session_type': forms.Select(attrs={'class': 'form-control'}),
            'input_data': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'output_data': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'configuration': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'computation_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_valid': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'session_type': _('نوع جلسه'),
            'input_data': _('داده‌های ورودی'),
            'output_data': _('داده‌های خروجی'),
            'configuration': _('پیکربندی'),
            'computation_time': _('زمان محاسبه'),
            'expires_at': _('تاریخ انقضا'),
            'is_valid': _('معتبر')
        }


class ComputationMetricsForm(forms.ModelForm):
    """فرم مدیریت متریک‌های محاسباتی"""
    
    class Meta:
        model = ComputationMetrics
        fields = [
            'date', 'total_sessions', 'completed_sessions', 'failed_sessions',
            'cancelled_sessions', 'average_processing_time', 'peak_processing_time',
            'average_memory_usage', 'peak_memory_usage', 'cache_hit_rate',
            'cache_miss_count', 'unique_users', 'free_user_sessions',
            'premium_user_sessions'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_sessions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'completed_sessions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'failed_sessions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'cancelled_sessions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'average_processing_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peak_processing_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'average_memory_usage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peak_memory_usage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cache_hit_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'cache_miss_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unique_users': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'free_user_sessions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'premium_user_sessions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
        }
        labels = {
            'date': _('تاریخ'),
            'total_sessions': _('کل جلسات'),
            'completed_sessions': _('جلسات تکمیل شده'),
            'failed_sessions': _('جلسات ناموفق'),
            'cancelled_sessions': _('جلسات لغو شده'),
            'average_processing_time': _('زمان پردازش متوسط'),
            'peak_processing_time': _('زمان پردازش اوج'),
            'average_memory_usage': _('استفاده حافظه متوسط'),
            'peak_memory_usage': _('استفاده حافظه اوج'),
            'cache_hit_rate': _('نرخ ضربه کش'),
            'cache_miss_count': _('تعداد خطای کش'),
            'unique_users': _('کاربران منحصر به فرد'),
            'free_user_sessions': _('جلسات کاربران رایگان'),
            'premium_user_sessions': _('جلسات کاربران پریمیوم')
        }
