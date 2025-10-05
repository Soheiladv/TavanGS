"""
Jalali Date Utilities
Reusable functions for Jalali (Persian) date conversion and validation
"""

import jdatetime
from datetime import datetime
from django import forms
from django.utils.translation import gettext_lazy as _


def convert_jalali_to_gregorian(jalali_date_string, default_time='00:00'):
    """
    Convert Jalali date string to Gregorian datetime object
    
    Args:
        jalali_date_string (str): Jalali date in format '1404/01/17' or '1404/01/17 12:30'
        default_time (str): Default time if not provided in format 'HH:MM'
    
    Returns:
        datetime: Gregorian datetime object
        
    Raises:
        ValueError: If date format is invalid
    """
    if not jalali_date_string:
        return None
        
    try:
        # Split date and time parts
        parts = jalali_date_string.strip().split(' ')
        date_part = parts[0]
        time_part = parts[1] if len(parts) > 1 else default_time
        
        # Parse date components
        year, month, day = map(int, date_part.split('/'))
        
        # Parse time components
        hour, minute = map(int, time_part.split(':'))
        
        # Create Jalali datetime and convert to Gregorian
        jalali_date = jdatetime.datetime(year, month, day, hour, minute)
        return jalali_date.togregorian()
        
    except (ValueError, IndexError) as e:
        raise ValueError(f'فرمت تاریخ صحیح نیست. از فرمت 1404/01/17 12:30 استفاده کنید. خطا: {str(e)}')


def convert_gregorian_to_jalali(gregorian_date, format_string='%Y/%m/%d %H:%M'):
    """
    Convert Gregorian datetime to Jalali date string
    
    Args:
        gregorian_date (datetime): Gregorian datetime object
        format_string (str): Output format string
        
    Returns:
        str: Jalali date string
    """
    if not gregorian_date:
        return None
        
    try:
        jalali_date = jdatetime.datetime.fromgregorian(datetime=gregorian_date)
        return jalali_date.strftime(format_string)
    except Exception as e:
        raise ValueError(f'خطا در تبدیل تاریخ: {str(e)}')


def validate_jalali_date_format(date_string):
    """
    Validate Jalali date format
    
    Args:
        date_string (str): Date string to validate
        
    Returns:
        bool: True if format is valid, False otherwise
    """
    if not date_string:
        return True  # Empty dates are considered valid
        
    try:
        # Try to parse the date
        convert_jalali_to_gregorian(date_string)
        return True
    except ValueError:
        return False


def get_jalali_date_widget_attrs(placeholder='1404/01/17 12:30', css_class='form-control'):
    """
    Get standard widget attributes for Jalali date fields
    
    Args:
        placeholder (str): Placeholder text
        css_class (str): CSS class for styling
        
    Returns:
        dict: Widget attributes
    """
    return {
        'class': css_class,
        'data-jdp': '',
        'placeholder': placeholder
    }


class JalaliDateField(forms.CharField):
    """
    Custom form field for Jalali date input with automatic conversion
    """
    
    def __init__(self, *args, **kwargs):
        # Set default widget attributes
        widget_attrs = kwargs.pop('widget_attrs', {})
        default_attrs = get_jalali_date_widget_attrs()
        default_attrs.update(widget_attrs)
        
        kwargs.setdefault('widget', forms.TextInput(attrs=default_attrs))
        super().__init__(*args, **kwargs)
    
    def clean(self, value):
        """
        Clean and convert Jalali date to Gregorian
        """
        value = super().clean(value)
        if not value:
            return None
            
        try:
            return convert_jalali_to_gregorian(value)
        except ValueError as e:
            raise forms.ValidationError(str(e))


def clean_jalali_date_field(date_value, field_name='تاریخ', default_time='00:00'):
    """
    Generic clean method for Jalali date fields in forms
    
    Args:
        date_value: The date value from cleaned_data
        field_name (str): Name of the field for error messages
        default_time (str): Default time if not provided
        
    Returns:
        datetime: Converted Gregorian datetime
        
    Raises:
        forms.ValidationError: If date format is invalid
    """
    if not date_value:
        return None
        
    try:
        return convert_jalali_to_gregorian(date_value, default_time)
    except ValueError as e:
        raise forms.ValidationError(f'{field_name}: {str(e)}')


# Common date field configurations
JALALI_DATE_CONFIGS = {
    'published_at': {
        'placeholder': '1404/01/17 12:30',
        'default_time': '00:00',
        'field_name': 'تاریخ انتشار'
    },
    'expires_at': {
        'placeholder': '1404/12/29 23:59',
        'default_time': '23:59',
        'field_name': 'تاریخ انقضا'
    },
    'birth_date': {
        'placeholder': '1404/01/17',
        'default_time': '00:00',
        'field_name': 'تاریخ تولد'
    },
    'expiry_date': {
        'placeholder': '1404/01/17',
        'default_time': '00:00',
        'field_name': 'تاریخ انقضا'
    }
}


def get_jalali_field_config(field_type):
    """
    Get configuration for common Jalali date fields
    
    Args:
        field_type (str): Type of field (published_at, expires_at, etc.)
        
    Returns:
        dict: Field configuration
    """
    return JALALI_DATE_CONFIGS.get(field_type, {
        'placeholder': '1404/01/17 12:30',
        'default_time': '00:00',
        'field_name': 'تاریخ'
    })
