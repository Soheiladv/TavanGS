# Jalali Date Utilities

This package provides reusable utilities for handling Jalali (Persian) dates in Django applications with a complete Persian date picker integration.

## Features

- **Persian Date Picker**: Full Persian calendar with time picker support
- **Automatic Conversion**: Convert Jalali dates to Gregorian and vice versa
- **Form Integration**: Easy integration with Django forms
- **Validation**: Built-in date format validation with visual feedback
- **JavaScript Support**: Client-side date picker with Persian calendar
- **Configurable**: Predefined configurations for common date fields
- **RTL Support**: Right-to-left layout support
- **Responsive Design**: Mobile-friendly date picker interface

## Installation

The utilities are already integrated into the project. Make sure you have the required dependencies:

```bash
pip install jdatetime
```

## Quick Start

### 1. Using JalaliDateField (Recommended)

```python
from utils.jalali_utils import JalaliDateField

class MyForm(forms.Form):
    published_date = JalaliDateField(
        label='تاریخ انتشار',
        required=False,
        widget_attrs={'placeholder': '1404/01/17 12:30'}
    )
```

### 2. Using Utility Functions in Existing Forms

```python
from utils.jalali_utils import clean_jalali_date_field, get_jalali_field_config

class NewsForm(forms.ModelForm):
    def clean_published_at(self):
        published_at = self.cleaned_data.get('published_at')
        config = get_jalali_field_config('published_at')
        return clean_jalali_date_field(
            published_at, 
            config['field_name'], 
            config['default_time']
        )
```

### 3. Using Widget Attributes

```python
from utils.jalali_utils import get_jalali_date_widget_attrs

class MyForm(forms.Form):
    expiry_date = forms.CharField(
        widget=forms.TextInput(attrs=get_jalali_date_widget_attrs(
            placeholder='1404/12/29 23:59'
        ))
    )
```

### 4. Direct Conversion Functions

```python
from utils.jalali_utils import convert_jalali_to_gregorian, convert_gregorian_to_jalali

# Convert Jalali to Gregorian
jalali_date = "1404/01/17 12:30"
gregorian_date = convert_jalali_to_gregorian(jalali_date)

# Convert Gregorian to Jalali
from datetime import datetime
gregorian_dt = datetime(2025, 4, 6, 12, 30)
jalali_str = convert_gregorian_to_jalali(gregorian_dt)
```

## Persian Date Picker Integration

The package includes a complete Persian date picker implementation:

### Features

- **Persian Calendar**: Full Persian calendar with month names in Persian
- **Time Picker**: Integrated time picker for date and time selection
- **Visual Feedback**: Color-coded validation (red: invalid, green: valid, yellow: typing)
- **Auto-formatting**: Automatic formatting as user types
- **Current Date**: Click to set current Jalali date
- **Keyboard Support**: Full keyboard navigation support
- **RTL Layout**: Right-to-left layout for Persian interface

### Usage in Templates

The JavaScript is automatically included in the base template. For date fields, add the `data-jdp` attribute:

```html
<input type="text" data-jdp placeholder="1404/01/17 12:30" class="form-control">
```

### JavaScript Functions

```javascript
// Set current Jalali date
setCurrentJalaliDate('field-id');

// Clear date field
clearJalaliDate('field-id');

// Validate date format
validateJalaliDate('1404/01/17 12:30');

// Initialize Persian date pickers
initializePersianDatePickers();
```

## Test Page

A test page is available at `/test-jalali/` to verify the Jalali date picker functionality:

- Test different date field types
- Validate date formats
- Test JavaScript functions
- See visual feedback in action

## Predefined Configurations

The package includes predefined configurations for common date fields:

- `published_at`: Publication date (default time: 00:00)
- `expires_at`: Expiration date (default time: 23:59)
- `birth_date`: Birth date (default time: 00:00)
- `expiry_date`: Expiry date (default time: 00:00)

## Date Formats

### Supported Input Formats

- `1404/01/17` (date only)
- `1404/01/17 12:30` (date with time)

### Output Formats

- Gregorian datetime objects for database storage
- Configurable Jalali string formats for display

## Error Handling

The utilities provide comprehensive error handling:

- **Format Validation**: Checks for proper Jalali date format
- **Range Validation**: Validates year, month, day, hour, minute ranges
- **User-Friendly Messages**: Persian error messages for better UX
- **Visual Feedback**: Color-coded borders for validation states

## Styling

The Persian date picker includes comprehensive styling:

- **Persian Fonts**: Uses Vazir font family for Persian text
- **RTL Support**: Right-to-left layout
- **Responsive Design**: Mobile-friendly interface
- **Dark Mode**: Automatic dark mode support
- **Custom Colors**: Configurable color scheme
- **Animations**: Smooth transitions and animations

## Examples

See `examples/jalali_usage_example.py` for comprehensive usage examples.

## Migration Guide

### Updating Existing Forms

1. **Import the utilities**:
   ```python
   from utils.jalali_utils import clean_jalali_date_field, get_jalali_field_config
   ```

2. **Update widget attributes**:
   ```python
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       config = get_jalali_field_config('published_at')
       self.fields['published_at'].widget.attrs.update(
           get_jalali_date_widget_attrs(placeholder=config['placeholder'])
       )
   ```

3. **Replace clean methods**:
   ```python
   def clean_published_at(self):
       published_at = self.cleaned_data.get('published_at')
       config = get_jalali_field_config('published_at')
       return clean_jalali_date_field(
           published_at, 
           config['field_name'], 
           config['default_time']
       )
   ```

### Updating Templates

Replace `type="date"` inputs with `data-jdp` attributes:

```html
<!-- Before -->
<input type="date" name="start_date" class="form-control">

<!-- After -->
<input type="text" name="start_date" class="form-control" data-jdp placeholder="1404/01/01">
```

## Dependencies

- `jdatetime`: For Jalali date conversion
- `persian-date`: For Persian date picker functionality
- `moment.js`: For JavaScript date handling
- `moment-jalaali`: For JavaScript Jalali support

## Browser Support

The JavaScript functionality works in all modern browsers that support:
- ES6 features
- CSS3 styling
- HTML5 form validation
- RTL layout support

## Troubleshooting

### Common Issues

1. **Date picker not showing**: Ensure `data-jdp` attribute is present
2. **Persian text not displaying**: Check if Vazir font is loaded
3. **Validation not working**: Ensure JavaScript files are loaded in correct order
4. **RTL layout issues**: Verify CSS direction properties are set correctly

### Debug Mode

Enable debug mode by adding to your template:

```html
<script>
    window.JALALI_DEBUG = true;
</script>
```

This will log additional information to the browser console.
