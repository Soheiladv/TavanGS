"""
News App Forms - News Management Forms
"""

from django import forms
from django.contrib.auth import get_user_model
from .models import News, NewsCategory, NewsComment, NewsTag

User = get_user_model()


class NewsForm(forms.ModelForm):
    """فرم ایجاد و ویرایش خبر"""
    
    class Meta:
        model = News
        fields = [
            'title', 'summary', 'content', 'category', 'featured_image',
            'meta_title', 'meta_description', 'meta_keywords',
            'status', 'priority', 'is_featured', 'is_pinned',
            'published_at', 'expires_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان خبر را وارد کنید'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'خلاصه کوتاه از خبر'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'محتوا کامل خبر'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان برای موتورهای جستجو'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'توضیحات برای موتورهای جستجو'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کلمات کلیدی (با کاما جدا کنید)'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # تنظیم برچسب‌های فارسی
        self.fields['title'].label = 'عنوان'
        self.fields['summary'].label = 'خلاصه'
        self.fields['content'].label = 'محتوا'
        self.fields['category'].label = 'دسته‌بندی'
        self.fields['featured_image'].label = 'تصویر شاخص'
        self.fields['meta_title'].label = 'عنوان متا'
        self.fields['meta_description'].label = 'توضیحات متا'
        self.fields['meta_keywords'].label = 'کلمات کلیدی'
        self.fields['status'].label = 'وضعیت'
        self.fields['priority'].label = 'اولویت'
        self.fields['is_featured'].label = 'ویژه'
        self.fields['is_pinned'].label = 'سنجاق شده'
        self.fields['published_at'].label = 'تاریخ انتشار'
        self.fields['expires_at'].label = 'تاریخ انقضا'
        
        # تنظیم help text
        self.fields['summary'].help_text = 'خلاصه کوتاه که در فهرست اخبار نمایش داده می‌شود'
        self.fields['meta_title'].help_text = 'عنوانی که در نتایج جستجو نمایش داده می‌شود'
        self.fields['meta_description'].help_text = 'توضیحاتی که در نتایج جستجو نمایش داده می‌شود'
        self.fields['meta_keywords'].help_text = 'کلمات کلیدی مرتبط با خبر'
        self.fields['is_featured'].help_text = 'خبرهای ویژه در بالای فهرست نمایش داده می‌شوند'
        self.fields['is_pinned'].help_text = 'خبرهای سنجاق شده همیشه در بالای فهرست نمایش داده می‌شوند'
        self.fields['expires_at'].help_text = 'تاریخ انقضای خبر (اختیاری)'


class NewsCategoryForm(forms.ModelForm):
    """فرم ایجاد و ویرایش دسته‌بندی"""
    
    class Meta:
        model = NewsCategory
        fields = ['name', 'description', 'color', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام دسته‌بندی'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'توضیحات دسته‌بندی'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام آیکون (مثال: fas fa-newspaper)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # تنظیم برچسب‌های فارسی
        self.fields['name'].label = 'نام'
        self.fields['description'].label = 'توضیحات'
        self.fields['color'].label = 'رنگ'
        self.fields['icon'].label = 'آیکون'
        self.fields['is_active'].label = 'فعال'
        
        # تنظیم help text
        self.fields['icon'].help_text = 'نام کلاس آیکون از Font Awesome'
        self.fields['color'].help_text = 'رنگ نمایش دسته‌بندی'


class NewsCommentForm(forms.ModelForm):
    """فرم افزودن نظر"""
    
    class Meta:
        model = NewsComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'نظر'
        self.fields['content'].help_text = 'نظر خود را در مورد این خبر بنویسید'


class NewsSearchForm(forms.Form):
    """فرم جستجوی اخبار"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو در اخبار...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=NewsCategory.objects.filter(is_active=True),
        required=False,
        empty_label="همه دسته‌بندی‌ها",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].label = 'جستجو'
        self.fields['category'].label = 'دسته‌بندی'
        self.fields['date_from'].label = 'از تاریخ'
        self.fields['date_to'].label = 'تا تاریخ'
