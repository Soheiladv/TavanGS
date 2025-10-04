from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Service, ServiceCategory


class ServiceForm(forms.ModelForm):
    """فرم ایجاد و ویرایش سرویس"""
    
    class Meta:
        model = Service
        fields = [
            'name', 'slug', 'tagline', 'description', 'short_description',
            'category', 'status', 'icon', 'banner_image', 'features', 
            'process_steps', 'deliverables', 'starting_price', 'price_currency',
            'price_unit', 'estimated_duration', 'is_featured', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیح کوتاه'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شعار و عنوان کوتاه'}),
            'features': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'ویژگی‌ها را به صورت JSON وارد کنید'}),
            'process_steps': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'مراحل فرآیند را به صورت JSON وارد کنید'}),
            'deliverables': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'تحویلی‌ها را به صورت JSON وارد کنید'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام سرویس'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نامک'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً: 2-4 هفته'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام آیکون Font Awesome'}),
            'banner_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price_currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IRR'}),
            'price_unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'پروژه'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'name': _('نام سرویس'),
            'slug': _('نامک'),
            'tagline': _('شعار'),
            'description': _('توضیحات کامل'),
            'short_description': _('توضیح کوتاه'),
            'category': _('دسته‌بندی'),
            'status': _('وضعیت'),
            'icon': _('آیکون'),
            'banner_image': _('تصویر بنر'),
            'features': _('ویژگی‌ها'),
            'process_steps': _('مراحل فرآیند'),
            'deliverables': _('تحویلی‌ها'),
            'starting_price': _('قیمت شروع'),
            'price_currency': _('واحد پول'),
            'price_unit': _('واحد قیمت'),
            'estimated_duration': _('مدت زمان تخمینی'),
            'is_featured': _('ویژه'),
            'is_active': _('فعال')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({'pattern': '[a-z0-9-_]+', 'title': 'فقط حروف کوچک، اعداد، خط تیره و زیرخط'})


class ServiceCategoryForm(forms.ModelForm):
    """فرم ایجاد و ویرایش دسته‌بندی سرویس"""
    
    class Meta:
        model = ServiceCategory
        fields = [
            'name', 'slug', 'description', 'icon', 'color', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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