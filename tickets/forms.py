"""
Tickets App Forms - Support System Forms
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Ticket, TicketReply, TicketCategory


class TicketCreateForm(forms.ModelForm):
    """Form for creating new tickets"""
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'priority', 'contact_email', 'contact_phone']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'عنوان کوتاه و مفید برای مسئله خود'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 6,
                'placeholder': 'شرح کامل مسئله یا درخواست خود را بنویسید...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'ایمیل جایگزین برای دریافت پاسخ (اختیاری)'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'شماره تلفن برای تماس فوری (اختیاری)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter categories to only active ones
        self.fields['category'].queryset = TicketCategory.objects.filter(is_active=True)
        
        # Set default priority
        self.fields['priority'].initial = 2
        
        # Add help text
        self.fields['title'].help_text = 'عنوان کوتاه و مفید برای مسئله خود'
        self.fields['description'].help_text = 'شرح کامل مسئله یا درخواست خود را بنویسید'
        self.fields['category'].help_text = 'دسته‌بندی مناسب برای مسئله خود را انتخاب کنید'
        self.fields['priority'].help_text = 'اولویت مسئله خود را مشخص کنید'
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise ValidationError('عنوان باید حداقل 10 کاراکتر باشد.')
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 20:
            raise ValidationError('شرح مسئله باید حداقل 20 کاراکتر باشد.')
        return description


class TicketReplyForm(forms.ModelForm):
    """Form for replying to tickets"""
    
    class Meta:
        model = TicketReply
        fields = ['content', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 4,
                'placeholder': 'پاسخ خود را بنویسید...'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only staff can make private replies
        if not self.user or not self.user.is_staff:
            self.fields['is_private'].widget = forms.HiddenInput()
            self.fields['is_private'].initial = False
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 5:
            raise ValidationError('پاسخ باید حداقل 5 کاراکتر باشد.')
        return content


class TicketUpdateForm(forms.ModelForm):
    """Form for updating ticket status (staff only)"""
    
    class Meta:
        model = Ticket
        fields = ['status', 'priority', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter assigned_to to only staff users
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)


class TicketFilterForm(forms.Form):
    """Form for filtering tickets"""
    
    STATUS_CHOICES = [
        ('', 'همه وضعیت‌ها'),
        ('open', 'باز'),
        ('in_progress', 'در حال بررسی'),
        ('pending', 'در انتظار پاسخ مشتری'),
        ('resolved', 'حل شده'),
        ('closed', 'بسته'),
        ('cancelled', 'لغو شده'),
    ]
    
    PRIORITY_CHOICES = [
        ('', 'همه اولویت‌ها'),
        (1, 'کم'),
        (2, 'متوسط'),
        (3, 'بالا'),
        (4, 'فوری'),
        (5, 'بحرانی'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=TicketCategory.objects.filter(is_active=True),
        required=False,
        empty_label="همه دسته‌بندی‌ها",
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
        })
    )
    
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
        })
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'جستجو در عنوان و شرح تیکت‌ها...'
        })
    )


class TicketAttachmentForm(forms.Form):
    """Form for uploading ticket attachments"""
    
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'accept': '.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.zip,.rar'
        }),
        help_text="فایل‌های مجاز: PDF, DOC, DOCX, TXT, JPG, PNG, GIF, ZIP, RAR (حداکثر 10MB)"
    )
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('اندازه فایل نباید بیشتر از 10 مگابایت باشد.')
            
            # Check file type
            allowed_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/plain',
                'image/jpeg',
                'image/jpg',
                'image/png',
                'image/gif',
                'application/zip',
                'application/x-rar-compressed',
            ]
            
            if file.content_type not in allowed_types:
                raise ValidationError('نوع فایل مجاز نیست. لطفاً فایل معتبری انتخاب کنید.')
        
        return file


class TicketSatisfactionForm(forms.Form):
    """Form for customer satisfaction rating"""
    
    SATISFACTION_CHOICES = [
        (1, 'خیلی ضعیف'),
        (2, 'ضعیف'),
        (3, 'متوسط'),
        (4, 'خوب'),
        (5, 'عالی'),
    ]
    
    satisfaction = forms.ChoiceField(
        choices=SATISFACTION_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'space-y-2'
        }),
        help_text="لطفاً رضایت خود از خدمات پشتیبانی را ارزیابی کنید"
    )
    
    feedback = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'rows': 3,
            'placeholder': 'نظرات و پیشنهادات خود را بنویسید (اختیاری)...'
        }),
        help_text="نظرات و پیشنهادات خود را بنویسید"
    )
