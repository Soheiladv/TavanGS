"""
Example usage of Jalali Date Utilities
This file demonstrates how to use the new utility functions in forms
"""

from django import forms
from utils.jalali_utils import (
    JalaliDateField, 
    clean_jalali_date_field, 
    get_jalali_field_config,
    get_jalali_date_widget_attrs
)


class ExampleForm(forms.Form):
    """
    Example form showing different ways to use Jalali date utilities
    """
    
    # Method 1: Using JalaliDateField (recommended for new forms)
    published_date = JalaliDateField(
        label='تاریخ انتشار',
        required=False,
        widget_attrs={'placeholder': '1404/01/17 12:30'}
    )
    
    # Method 2: Using regular CharField with custom widget attributes
    expiry_date = forms.CharField(
        label='تاریخ انقضا',
        required=False,
        widget=forms.TextInput(attrs=get_jalali_date_widget_attrs(
            placeholder='1404/12/29 23:59'
        ))
    )
    
    # Method 3: Using configuration-based approach
    birth_date = forms.CharField(
        label='تاریخ تولد',
        required=False,
        widget=forms.TextInput(attrs=get_jalali_date_widget_attrs(
            placeholder=get_jalali_field_config('birth_date')['placeholder']
        ))
    )
    
    def clean_expiry_date(self):
        """Clean method using utility function"""
        expiry_date = self.cleaned_data.get('expiry_date')
        config = get_jalali_field_config('expiry_date')
        return clean_jalali_date_field(
            expiry_date, 
            config['field_name'], 
            config['default_time']
        )
    
    def clean_birth_date(self):
        """Clean method using utility function"""
        birth_date = self.cleaned_data.get('birth_date')
        config = get_jalali_field_config('birth_date')
        return clean_jalali_date_field(
            birth_date, 
            config['field_name'], 
            config['default_time']
        )


# Example of updating existing forms
class ExistingFormUpdate(forms.ModelForm):
    """
    Example of how to update existing forms to use the utility functions
    """
    
    class Meta:
        # Replace with your actual model
        # model = YourModel
        fields = ['some_field']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update widget attributes for existing fields
        if 'published_at' in self.fields:
            config = get_jalali_field_config('published_at')
            self.fields['published_at'].widget.attrs.update(
                get_jalali_date_widget_attrs(
                    placeholder=config['placeholder']
                )
            )
    
    def clean_published_at(self):
        """Replace existing clean method with utility function"""
        published_at = self.cleaned_data.get('published_at')
        config = get_jalali_field_config('published_at')
        return clean_jalali_date_field(
            published_at, 
            config['field_name'], 
            config['default_time']
        )


# Example of using the utility functions in views or other parts of the code
def example_view_function():
    """
    Example of using utility functions outside of forms
    """
    from utils.jalali_utils import convert_jalali_to_gregorian, convert_gregorian_to_jalali
    
    # Convert Jalali date string to Gregorian datetime
    jalali_date = "1404/01/17 12:30"
    gregorian_date = convert_jalali_to_gregorian(jalali_date)
    print(f"Gregorian date: {gregorian_date}")
    
    # Convert Gregorian datetime to Jalali date string
    from datetime import datetime
    gregorian_dt = datetime(2025, 4, 6, 12, 30)
    jalali_str = convert_gregorian_to_jalali(gregorian_dt)
    print(f"Jalali date: {jalali_str}")
    
    # Validate Jalali date format
    from utils.jalali_utils import validate_jalali_date_format
    is_valid = validate_jalali_date_format("1404/01/17 12:30")
    print(f"Is valid: {is_valid}")
