from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ProductVersion, DemoRequest, PricingRequest, SalesLead
from products.models import Product


class ProductVersionForm(forms.ModelForm):
    """فرم ایجاد و ویرایش نسخه محصول"""
    
    class Meta:
        model = ProductVersion
        fields = [
            'product', 'version_number', 'version_type', 'status', 'release_date',
            'changelog', 'release_notes', 'system_requirements', 'file_size_mb',
            'download_url', 'is_free', 'price', 'currency', 'has_trial', 'trial_days',
            'trial_download_url', 'is_featured', 'is_active'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'version_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 1.2.3'}),
            'version_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'release_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'changelog': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'release_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'system_requirements': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'ویژگی‌ها را به صورت JSON وارد کنید'}),
            'file_size_mb': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.1'}),
            'download_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IRR'}),
            'trial_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '365'}),
            'trial_download_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_trial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'product': _('محصول'),
            'version_number': _('شماره نسخه'),
            'version_type': _('نوع نسخه'),
            'status': _('وضعیت'),
            'release_date': _('تاریخ انتشار'),
            'changelog': _('لیست تغییرات'),
            'release_notes': _('یادداشت‌های انتشار'),
            'system_requirements': _('نیازهای سیستم'),
            'file_size_mb': _('حجم فایل (مگابایت)'),
            'download_url': _('لینک دانلود'),
            'is_free': _('رایگان'),
            'price': _('قیمت'),
            'currency': _('واحد پول'),
            'has_trial': _('نسخه آزمایشی'),
            'trial_days': _('روزهای آزمایشی'),
            'trial_download_url': _('لینک دانلود آزمایشی'),
            'is_featured': _('ویژه'),
            'is_active': _('فعال')
        }


class DemoRequestForm(forms.ModelForm):
    """فرم درخواست دمو"""
    
    class Meta:
        model = DemoRequest
        fields = [
            'product', 'full_name', 'email', 'phone', 'company', 'job_title',
            'preferred_date', 'preferred_time', 'demo_type', 'special_requirements'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل شما'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام شرکت'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'سمت شغلی شما'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preferred_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'زمان ترجیحی (مثلاً: صبح، عصر)'}),
            'demo_type': forms.Select(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'نیازهای خاص یا سوالات شما'})
        }
        labels = {
            'product': _('محصول مورد نظر'),
            'full_name': _('نام کامل'),
            'email': _('ایمیل'),
            'phone': _('شماره تلفن'),
            'company': _('شرکت'),
            'job_title': _('سمت'),
            'preferred_date': _('تاریخ ترجیحی'),
            'preferred_time': _('زمان ترجیحی'),
            'demo_type': _('نوع دمو'),
            'special_requirements': _('نیازهای خاص')
        }


class PricingRequestForm(forms.ModelForm):
    """فرم درخواست قیمت"""
    
    class Meta:
        model = PricingRequest
        fields = [
            'product', 'full_name', 'email', 'phone', 'company', 'job_title',
            'user_count', 'deployment_type', 'custom_requirements', 'budget_range', 'timeline'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل شما'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام شرکت'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'سمت شغلی شما'}),
            'user_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'تعداد کاربران'}),
            'deployment_type': forms.Select(attrs={'class': 'form-control'}),
            'custom_requirements': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'توضیحات نیازهای سفارشی پروژه'}),
            'budget_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'محدوده بودجه شما'}),
            'timeline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'زمان‌بندی مورد نظر'})
        }
        labels = {
            'product': _('محصول مورد نظر'),
            'full_name': _('نام کامل'),
            'email': _('ایمیل'),
            'phone': _('شماره تلفن'),
            'company': _('شرکت'),
            'job_title': _('سمت'),
            'user_count': _('تعداد کاربران'),
            'deployment_type': _('نوع استقرار'),
            'custom_requirements': _('نیازهای سفارشی'),
            'budget_range': _('محدوده بودجه'),
            'timeline': _('زمان‌بندی')
        }


class SalesLeadAdminForm(forms.ModelForm):
    """فرم مدیریت سرنخ‌های فروش (برای staff)"""
    
    class Meta:
        model = SalesLead
        fields = [
            'source', 'status', 'full_name', 'email', 'phone', 'company', 'job_title',
            'product_interest', 'estimated_value', 'currency', 'notes', 'assigned_to',
            'last_contact_date', 'next_follow_up'
        ]
        widgets = {
            'source': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'product_interest': forms.Select(attrs={'class': 'form-control'}),
            'estimated_value': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IRR'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'last_contact_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'next_follow_up': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }
        labels = {
            'source': _('منبع سرنخ'),
            'status': _('وضعیت'),
            'full_name': _('نام کامل'),
            'email': _('ایمیل'),
            'phone': _('شماره تلفن'),
            'company': _('شرکت'),
            'job_title': _('سمت'),
            'product_interest': _('محصول مورد علاقه'),
            'estimated_value': _('ارزش تخمینی'),
            'currency': _('واحد پول'),
            'notes': _('یادداشت‌ها'),
            'assigned_to': _('اختصاص داده شده به'),
            'last_contact_date': _('تاریخ آخرین تماس'),
            'next_follow_up': _('پی گیری بعدی')
        }
