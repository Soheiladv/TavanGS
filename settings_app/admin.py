"""
Settings App Admin Configuration
Enhanced admin interface for site configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
import json

from .models import SiteSettings, APIConfiguration, FeatureFlag, FontSettings


class SiteSettingsAdminForm(ModelForm):
    """Custom form for SiteSettings with JSON validation"""
    
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'company_description': Textarea(attrs={'rows': 4}),
            'meta_description': Textarea(attrs={'rows': 3}),
            'maintenance_message': Textarea(attrs={'rows': 3}),
            'custom_css': Textarea(attrs={'rows': 10, 'class': 'code-editor'}),
            'custom_js': Textarea(attrs={'rows': 10, 'class': 'code-editor'}),
            'hero_section_config': Textarea(attrs={'rows': 8, 'class': 'json-editor'}),
            'features_config': Textarea(attrs={'rows': 8, 'class': 'json-editor'}),
            'testimonials_config': Textarea(attrs={'rows': 8, 'class': 'json-editor'}),
        }
    
    def clean_hero_section_config(self):
        """Validate hero section JSON"""
        data = self.cleaned_data['hero_section_config']
        if data and not isinstance(data, dict):
            try:
                json.loads(str(data))
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON format for hero section config")
        return data
    
    def clean_features_config(self):
        """Validate features JSON"""
        data = self.cleaned_data['features_config']
        if data and not isinstance(data, list):
            try:
                json.loads(str(data))
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON format for features config")
        return data


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Enhanced admin interface for site settings"""
    
    form = SiteSettingsAdminForm
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'company_tagline', 'company_description'),
            'classes': ('wide',)
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'company_address'),
            'classes': ('wide',)
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url', 'github_url', 'instagram_url'),
            'classes': ('wide', 'collapse')
        }),
        ('SEO Settings', {
            'fields': ('site_title', 'meta_description', 'meta_keywords'),
            'classes': ('wide',)
        }),
        ('Theme Colors', {
            'fields': ('primary_color', 'secondary_color', 'accent_color'),
            'classes': ('wide',)
        }),
        ('Feature Toggles', {
            'fields': (
                'enable_ai_features', 'enable_sandbox', 'enable_live_chat',
                'enable_newsletter', 'enable_blog'
            ),
            'classes': ('wide',)
        }),
        ('API & Performance', {
            'fields': ('api_rate_limit', 'max_file_upload_size'),
            'classes': ('wide', 'collapse')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'google_tag_manager_id', 'facebook_pixel_id'),
            'classes': ('wide', 'collapse')
        }),
        ('Email Settings', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_use_tls'),
            'classes': ('wide', 'collapse')
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'classes': ('wide',)
        }),
        ('Custom Code', {
            'fields': ('custom_css', 'custom_js'),
            'classes': ('wide', 'collapse')
        }),
        ('Content Configuration', {
            'fields': ('hero_section_config', 'features_config', 'testimonials_config'),
            'classes': ('wide', 'collapse')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        """Only allow one instance of settings"""
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False
    
    def color_preview(self, obj):
        """Show color preview in admin"""
        return format_html(
            '<div style="display: flex; gap: 10px;">'
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>'
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>'
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>'
            '</div>',
            obj.primary_color, obj.secondary_color, obj.accent_color
        )
    color_preview.short_description = 'Theme Colors'
    
    def feature_status(self, obj):
        """Show feature status"""
        features = []
        if obj.enable_ai_features:
            features.append('<span style="color: green;">AI ✓</span>')
        if obj.enable_sandbox:
            features.append('<span style="color: green;">Sandbox ✓</span>')
        if obj.enable_live_chat:
            features.append('<span style="color: green;">Chat ✓</span>')
        
        return format_html(' | '.join(features) if features else 'No features enabled')
    feature_status.short_description = 'Active Features'
    
    list_display = ['company_name', 'color_preview', 'feature_status', 'maintenance_mode', 'updated_at']
    
    class Media:
        css = {
            'all': ('admin/css/site_settings.css',)
        }
        js = ('admin/js/json_editor.js',)


@admin.register(APIConfiguration)
class APIConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for API configurations"""
    
    fieldsets = (
        ('AI/ML Services', {
            'fields': ('openai_api_key', 'huggingface_api_key'),
            'classes': ('wide',)
        }),
        ('Payment Gateways', {
            'fields': ('zarinpal_merchant_id', 'stripe_publishable_key', 'stripe_secret_key'),
            'classes': ('wide', 'collapse')
        }),
        ('Social Authentication', {
            'fields': ('google_client_id', 'google_client_secret', 'github_client_id', 'github_client_secret'),
            'classes': ('wide', 'collapse')
        }),
        ('Security & Validation', {
            'fields': ('recaptcha_site_key', 'recaptcha_secret_key'),
            'classes': ('wide', 'collapse')
        }),
        ('Communication', {
            'fields': ('telegram_bot_token', 'slack_webhook_url'),
            'classes': ('wide', 'collapse')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_form(self, request, obj=None, **kwargs):
        """Make sensitive fields use password input"""
        form = super().get_form(request, obj, **kwargs)
        
        # Make API keys use password input
        sensitive_fields = [
            'openai_api_key', 'huggingface_api_key', 'stripe_secret_key',
            'google_client_secret', 'github_client_secret', 'recaptcha_secret_key',
            'telegram_bot_token'
        ]
        
        for field_name in sensitive_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget.attrs['type'] = 'password'
        
        return form
    
    def has_add_permission(self, request):
        """Only allow one instance of API config"""
        return not APIConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of API config"""
        return False


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    """Admin interface for feature flags"""
    
    list_display = [
        'name', 'is_active', 'percentage', 'date_range_status', 
        'target_users_count', 'updated_at'
    ]
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active'),
            'classes': ('wide',)
        }),
        ('Rollout Configuration', {
            'fields': ('percentage', 'target_user_types'),
            'classes': ('wide',)
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date'),
            'classes': ('wide', 'collapse')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def date_range_status(self, obj):
        """Show date range status"""
        from django.utils import timezone
        now = timezone.now()
        
        if obj.start_date and obj.end_date:
            if now < obj.start_date:
                return format_html('<span style="color: orange;">Scheduled</span>')
            elif now > obj.end_date:
                return format_html('<span style="color: red;">Expired</span>')
            else:
                return format_html('<span style="color: green;">Active</span>')
        elif obj.start_date and now < obj.start_date:
            return format_html('<span style="color: orange;">Scheduled</span>')
        elif obj.end_date and now > obj.end_date:
            return format_html('<span style="color: red;">Expired</span>')
        else:
            return format_html('<span style="color: blue;">No Limits</span>')
    
    date_range_status.short_description = 'Date Status'
    
    def target_users_count(self, obj):
        """Show target user types count"""
        if obj.target_user_types:
            return len(obj.target_user_types)
        return 0
    
    target_users_count.short_description = 'Target Types'
    
    actions = ['enable_flags', 'disable_flags', 'set_100_percent', 'set_0_percent']
    
    def enable_flags(self, request, queryset):
        """Enable selected feature flags"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} feature flags enabled.')
    enable_flags.short_description = 'Enable selected flags'
    
    def disable_flags(self, request, queryset):
        """Disable selected feature flags"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} feature flags disabled.')
    disable_flags.short_description = 'Disable selected flags'
    
    def set_100_percent(self, request, queryset):
        """Set rollout to 100%"""
        count = queryset.update(percentage=100)
        self.message_user(request, f'{count} feature flags set to 100% rollout.')
    set_100_percent.short_description = 'Set to 100% rollout'
    
    def set_0_percent(self, request, queryset):
        """Set rollout to 0%"""
        count = queryset.update(percentage=0)
        self.message_user(request, f'{count} feature flags set to 0% rollout.')
    set_0_percent.short_description = 'Set to 0% rollout'


@admin.register(FontSettings)
class FontSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'family_name', 'font_format', 'font_weight', 'is_default', 'is_active', 'file_size_formatted', 'upload_date']
    list_filter = ['is_active', 'is_default', 'font_format', 'font_weight']
    search_fields = ['name', 'family_name', 'description']
    readonly_fields = ['file_size', 'upload_date']