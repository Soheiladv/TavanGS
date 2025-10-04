"""
Users App Forms - User Profile and Preferences Forms
"""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile with CustomUser and CustomProfile integration"""
    
    # Additional fields for profile
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'شماره تلفن خود را وارد کنید'
        })
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'درباره خود بنویسید...',
            'rows': 4
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'آدرس خود را وارد کنید',
            'rows': 3
        })
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'type': 'date'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'نام خود را وارد کنید'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'نام خانوادگی خود را وارد کنید'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'ایمیل خود را وارد کنید'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'نام کاربری خود را وارد کنید'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load profile data if user has a profile
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            self.fields['phone_number'].initial = profile.phone_number
            self.fields['bio'].initial = profile.bio
            self.fields['address'].initial = profile.address
            self.fields['birth_date'].initial = profile.birth_date
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already taken by another user
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError('این ایمیل قبلاً استفاده شده است.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check if username is already taken by another user
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise ValidationError('این نام کاربری قبلاً استفاده شده است.')
        return username
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Basic phone number validation
            if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                raise ValidationError('شماره تلفن باید شامل اعداد باشد.')
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if commit:
            # Get or create profile
            profile, created = user.profile.get_or_create()
            
            # Update profile fields
            profile.phone_number = self.cleaned_data.get('phone_number', '')
            profile.bio = self.cleaned_data.get('bio', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.birth_date = self.cleaned_data.get('birth_date')
            profile.save()
        
        return user


class UserPreferencesForm(forms.ModelForm):
    """Form for editing user preferences with theme and profile integration"""
    
    # Theme preference
    theme = forms.ChoiceField(
        choices=[
            ('default', 'پیش‌فرض'),
            ('dark', 'تیره'),
            ('light', 'روشن'),
            ('blue', 'آبی'),
            ('green', 'سبز'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
        })
    )
    
    # Notification preferences
    email_notifications = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
        })
    )
    
    sms_notifications = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
        })
    )
    
    marketing_emails = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
        })
    )
    
    class Meta:
        model = User
        fields = ['is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load profile data if user has a profile
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            self.fields['theme'].initial = profile.theme
            # Add more profile-based preferences as needed
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if commit and hasattr(user, 'profile'):
            # Update profile theme
            profile = user.profile
            profile.theme = self.cleaned_data.get('theme', 'default')
            profile.save()
        
        return user


class PasswordChangeForm(forms.Form):
    """Form for changing password"""
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'رمز عبور فعلی'
        }),
        label='رمز عبور فعلی'
    )
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'رمز عبور جدید'
        }),
        label='رمز عبور جدید',
        min_length=8
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'تایید رمز عبور جدید'
        }),
        label='تایید رمز عبور جدید'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError('رمز عبور جدید و تایید آن مطابقت ندارند.')
        
        return cleaned_data
    
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            # Password strength validation
            if len(new_password) < 8:
                raise ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد.')
            
            if not any(c.isdigit() for c in new_password):
                raise ValidationError('رمز عبور باید شامل حداقل یک عدد باشد.')
            
            if not any(c.isalpha() for c in new_password):
                raise ValidationError('رمز عبور باید شامل حداقل یک حرف باشد.')
        
        return new_password


class EmailChangeForm(forms.Form):
    """Form for changing email address"""
    
    new_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'ایمیل جدید'
        }),
        label='ایمیل جدید'
    )
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'رمز عبور فعلی'
        }),
        label='رمز عبور فعلی'
    )


class AccountDeletionForm(forms.Form):
    """Form for account deletion confirmation"""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'رمز عبور فعلی'
        }),
        label='رمز عبور فعلی',
        help_text='برای تایید حذف حساب، رمز عبور فعلی خود را وارد کنید'
    )
    
    confirmation = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'
        }),
        label='تایید حذف حساب',
        help_text='با تیک زدن این گزینه، تایید می‌کنم که می‌خواهم حساب کاربری خود را حذف کنم'
    )
    
    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if not confirmation:
            raise ValidationError('برای حذف حساب باید این گزینه را تایید کنید.')
        return confirmation


class TwoFactorSetupForm(forms.Form):
    """Form for setting up two-factor authentication"""
    
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'شماره تلفن همراه'
        }),
        label='شماره تلفن همراه',
        help_text='شماره تلفن همراه خود را برای دریافت کد تایید وارد کنید'
    )
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Basic phone number validation
            if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                raise ValidationError('شماره تلفن باید شامل اعداد باشد.')
            
            if len(phone.replace('+', '').replace('-', '').replace(' ', '')) < 10:
                raise ValidationError('شماره تلفن باید حداقل 10 رقم باشد.')
        
        return phone


class TwoFactorVerifyForm(forms.Form):
    """Form for verifying two-factor authentication code"""
    
    verification_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-center text-2xl tracking-widest',
            'placeholder': '000000',
            'maxlength': '6'
        }),
        label='کد تایید',
        max_length=6,
        min_length=6,
        help_text='کد 6 رقمی ارسال شده به تلفن همراه خود را وارد کنید'
    )
    
    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        if code:
            if not code.isdigit():
                raise ValidationError('کد تایید باید شامل اعداد باشد.')
        return code
