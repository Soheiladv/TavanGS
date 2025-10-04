from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product, ProductCategory


class ProductForm(forms.ModelForm):
    """فرم ایجاد و ویرایش محصول"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'brand_prefix', 'tagline', 'description', 'short_description',
            'category', 'status', 'logo', 'banner_image', 'features', 'technical_specs',
            'has_free_version', 'has_trial', 'trial_days', 'is_featured', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیح کوتاه'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شعار محصول'}),
            'features': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'ویژگی‌ها را به صورت JSON وارد کنید'}),
            'technical_specs': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'مشخصات فنی را به صورت JSON وارد کنید'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام محصول'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نامک'}),
            'brand_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TakoTech'}),
            'trial_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '365'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'banner_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'has_free_version': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_trial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'name': _('نام محصول'),
            'slug': _('نامک'),
            'brand_prefix': _('پیشوند برند'),
            'tagline': _('شعار'),
            'description': _('توضیحات کامل'),
            'short_description': _('توضیح کوتاه'),
            'category': _('دسته‌بندی'),
            'status': _('وضعیت'),
            'logo': _('لوگو محصول'),
            'banner_image': _('تصویر بنر'),
            'features': _('ویژگی‌ها'),
            'technical_specs': _('مشخصات فنی'),
            'has_free_version': _('نسخه رایگان'),
            'has_trial': _('نسخه آزمایشی'),
            'trial_days': _('مدت آزمایشی (روز)'),
            'is_featured': _('ویژه'),
            'is_active': _('فعال')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({'pattern': '[a-z0-9-_]+', 'title': 'فقط حروف کوچک، اعداد، خط تیره و زیرخط'})
        
        # تنظیم مقدار پیش‌فرض برای brand_prefix
        if not self.instance.pk:
            self.fields['brand_prefix'].initial = 'TakoTech'


class ProductCategoryForm(forms.ModelForm):
    """فرم ایجاد و ویرایش دسته‌بندی محصول"""
    
    class Meta:
        model = ProductCategory
        fields = [
            'name', 'slug', 'description', 'icon', 'color', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام دسته‌بندی'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نامک'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام آیکون Font Awesome'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'blue, green, red, ...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'name': _('نام دسته‌بندی'),
            'slug': _('نامک'),
            'description': _('توضیحات'),
            'icon': _('آیکون'),
            'color': _('رنگ'),
            'is_active': _('فعال')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({'pattern': '[a-z0-9-_]+', 'title': 'فقط حروف کوچک، اعداد، خط تیره و زیرخط'})
