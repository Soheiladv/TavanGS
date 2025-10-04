"""
Settings App Context Processors
Make site settings available in all templates
"""

from django.core.cache import cache
from .models import SiteSettings, FeatureFlag


def site_settings(request):
    """
    Add site settings to template context
    Uses caching for performance
    """
    
    # Try to get from cache first
    settings = cache.get('site_settings')
    
    if settings is None:
        try:
            settings_obj = SiteSettings.load()
            settings = {
                'site_settings': settings_obj,
                'company_name': settings_obj.company_name,
                'company_tagline': settings_obj.company_tagline,
                'site_title': settings_obj.site_title,
                'meta_description': settings_obj.meta_description,
                'theme_colors': settings_obj.theme_colors,
                'hero_config': settings_obj.get_hero_config(),
                'features_list': settings_obj.get_features_list(),
                'contact_info': {
                    'email': settings_obj.contact_email,
                    'phone': settings_obj.contact_phone,
                    'address': settings_obj.company_address,
                },
                'social_links': {
                    'linkedin': settings_obj.linkedin_url,
                    'twitter': settings_obj.twitter_url,
                    'github': settings_obj.github_url,
                    'instagram': settings_obj.instagram_url,
                },
                'feature_flags': {
                    'ai_features': settings_obj.enable_ai_features,
                    'sandbox': settings_obj.enable_sandbox,
                    'live_chat': settings_obj.enable_live_chat,
                    'newsletter': settings_obj.enable_newsletter,
                    'blog': settings_obj.enable_blog,
                },
                'maintenance_mode': settings_obj.maintenance_mode,
                'maintenance_message': settings_obj.maintenance_message,
            }
            
            # Cache for 5 minutes
            cache.set('site_settings', settings, 300)
            
        except Exception:
            # Fallback settings if database is not available
            settings = {
                'site_settings': None,
                'company_name': 'TakoTech',
                'company_tagline': 'پیشرو در فناوری و نوآوری',
                'site_title': 'TakoTech - راهکارهای هوشمند فناوری',
                'meta_description': 'شرکت تک یا فناوری، ارائه‌دهنده نرم‌افزارهای کاربردی',
                'theme_colors': {
                    'primary': '#2563eb',
                    'secondary': '#7c3aed',
                    'accent': '#f59e0b',
                },
                'hero_config': {
                    'title': 'راهکارهای هوشمند فناوری',
                    'subtitle': 'با TakoTech آینده را بسازید',
                },
                'features_list': [],
                'contact_info': {
                    'email': 'info@takotech.com',
                    'phone': '+98-21-12345678',
                    'address': 'تهران، ایران',
                },
                'social_links': {},
                'feature_flags': {
                    'ai_features': True,
                    'sandbox': True,
                    'live_chat': True,
                    'newsletter': True,
                    'blog': True,
                },
                'maintenance_mode': False,
                'maintenance_message': '',
            }
    
    return settings


def feature_flags(request):
    """
    Add active feature flags to template context
    """
    
    # Get user-specific feature flags
    user = request.user if hasattr(request, 'user') else None
    
    # Try to get from cache
    cache_key = f'feature_flags_{user.id if user and user.is_authenticated else "anonymous"}'
    flags = cache.get(cache_key)
    
    if flags is None:
        try:
            all_flags = FeatureFlag.objects.filter(is_active=True)
            flags = {}
            
            for flag in all_flags:
                flags[flag.name] = flag.is_enabled_for_user(user)
            
            # Cache for 1 minute (shorter cache for feature flags)
            cache.set(cache_key, flags, 60)
            
        except Exception:
            flags = {}
    
    return {'feature_flags': flags}


def user_preferences(request):
    """
    Add user-specific preferences to template context
    """
    
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {
            'user_preferences': {
                'theme': 'light',
                'language': 'fa',
                'timezone': 'Asia/Tehran',
            }
        }
    
    # Get user preferences from cache or database
    cache_key = f'user_preferences_{request.user.id}'
    preferences = cache.get(cache_key)
    
    if preferences is None:
        try:
            # Try to get from user profile (will be implemented in users app)
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                preferences = {
                    'theme': getattr(profile, 'theme', 'light'),
                    'language': getattr(profile, 'language', 'fa'),
                    'timezone': getattr(profile, 'timezone', 'Asia/Tehran'),
                    'notifications': getattr(profile, 'email_notifications', True),
                }
            else:
                preferences = {
                    'theme': 'light',
                    'language': 'fa',
                    'timezone': 'Asia/Tehran',
                    'notifications': True,
                }
            
            # Cache for 10 minutes
            cache.set(cache_key, preferences, 600)
            
        except Exception:
            preferences = {
                'theme': 'light',
                'language': 'fa',
                'timezone': 'Asia/Tehran',
                'notifications': True,
            }
    
    return {'user_preferences': preferences}
